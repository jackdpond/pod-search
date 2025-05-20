import assemblyai as aai
import json

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
import faiss
from openai import OpenAI
import numpy as np

from dotenv import load_dotenv

load_dotenv()

def ms2hms(ms):
    seconds = ms // 1000
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02}:{minutes:02}:{secs:02}"

class Scribe:

    def __init__(self, episode_title, series_title, dimension=1536, embedding_model='text-embedding-3-small'):
        self.assembly_api_key = 0
        self.episode_title = episode_title
        self.series_title = series_title

        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.utterances = []

        self.client = OpenAI()
        self.embedding_model = embedding_model


    def transcribe(self, audio_file, speaker_labels=True, speakers_expected=2, speaker_map={'A': 'A', 'B': 'B', 'C': 'C'}, verbose=False):
        aai.settings.api_key = self.api_key
        aai.settings.http_timeout = 120.0

        config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best, 
                                         speaker_labels=speaker_labels, 
                                         speakers_expected=speakers_expected)

        transcriber = aai.Transcriber(config=config).transcribe(audio_file)

        if transcriber.status == "error":
            raise RuntimeError(f"Transcription failed: {transcriber.error}")
        
        transcript = list()
        for utterance in transcriber.utterances:
            transcript.append({"speaker": speaker_map[utterance.speaker],
                          "text": utterance.text,
                          "start": ms2hms(utterance.start),
                          "end": ms2hms(utterance.end)})
            
        self.transcript = transcript

        if verbose:
            for utterance in transcriber.utterances:
                print(f"{utterance.speaker}: {utterance.text}")

    def add_speaker_labels(self, speaker_map={'A': 'A', 'B': 'B', 'C': 'C'}):
        for utterance in self.transcript:
            utterance['speaker'] = speaker_map[utterance['speaker']]
        
    def save_as_json(self, destination):    
        with open(destination, "w") as file:
            json.dump(self.transcript, file, indent=4)

        print("Saved as .json!")


    def save_as_pdf(self, destination):
        # Set up the PDF file
        filename = destination
        document = SimpleDocTemplate(filename, pagesize=letter)

        # Create a custom style for text
        styles = getSampleStyleSheet()

        style_heading = ParagraphStyle(
            'HeadingStyle',
            parent=styles['Heading2'],
            fontName='Times-Roman',
            fontSize=16,
            alignment=1
        )

        style_title = ParagraphStyle(
            'TitleStyle',
            parent=styles['Title'],
            fontName='Times-Roman',
            fontSize=24,
            alignment=1
        )

        # Custom style for normal text with a serif font (Times New Roman)
        style_normal = ParagraphStyle(
            'NormalStyle', 
            parent=styles['Normal'],
            fontName='Times-Roman',  # Using Times New Roman
            fontSize=12,
            spaceBefore=5,
            spaceAfter=5,
            firstLineIndent=0,  # First line of the paragraph won't be indented
            leftIndent=15  # Indentation for following lines
        )

        # Custom style for speaker names (no bold, same size)
        style_speaker = ParagraphStyle(
            'SpeakerStyle',
            parent=styles['Normal'],
            fontName='Times-Roman',
            fontSize=12,
            spaceBefore=5,
            spaceAfter=5,
            firstLineIndent=0  # Speaker name is on the same line as dialogue
        )

        # Create a list of paragraph objects to add to the PDF
        content = []

        # Title
        content.append(Paragraph(self.episode_title, style_title))
        content.append(Paragraph(self.series_title, style_heading))

        # Loop through each item in the "interview" list
        for entry in self.transcript:
            speaker = entry["speaker"]
            text = entry["text"]
            
            # Add the speaker's name on the same line as the dialogue
            dialog = f"<b>{speaker}:</b> {text}"
            
            # Add the combined speaker and text paragraph
            content.append(Paragraph(dialog, style_normal))
            content.append(Paragraph("", style_normal))

        # Build the PDF
        document.build(content)

        print(f"PDF created: {filename}")

    def add_batch_embeddings(self, texts, batch_size=100):
        for i in range(0, len(texts), batch_size):
            batch = texts[i: i+batch_size]
            response = self.client.embeddings.create(input=batch, model=self.embedding_model)
            batch_embeddings = np.array([item.embedding for item in response.data]).astype('float32')
            self.index.add(batch_embeddings)

        print('Created and added embeddings to index')

    def add_to_index(self, batch_size = 100):
        documents = [{'text': utterance['text'],
                            'start': utterance['start'],
                            'end': utterance['end'],
                            'series': self.series_title,
                            'episode': self.episode_title}
                            for utterance in self.transcript]
        self.utterances.extend(documents)

        texts = [doc['text'] for doc in documents]
        self.add_batch_embeddings(texts, batch_size)

        print("Index and utterances initialized.")

    def search(self, query, k=5, verbose=True):
        query_embedding = self.client.embeddings.create(input=query, model=self.embedding_model).data[0].embedding
        print('Query embedding obtained')
        query_vector = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query_vector, k)
        
        print('Search completed')

        results = []
        for distance, idx in zip(distances[0], indices[0]):
            result = self.utterances[idx].copy()
            result['similarity score'] = 1 / (1 + distance)
            results.append(result)

            if verbose:
                print(f'{result['series']}: {result['episode']} at {result['start']}')
                print(f'{result['text']}')
                print(f'Similarity: {result['similarity score']}')
                print('-------------------------------------------------------------------------------')

        return results
    
    def save_database(self, filename):
        """Save FAISS index and documents to disk"""
        faiss.write_index(self.index, f"{filename}.index")

        print(f'FAISS index saved to {filename}.index')

        with open(f"{filename}.json", 'w') as f:
            json.dump(self.utterances, f)

        print(f'Text, metadata saved to {filename}.json')

    def load_database(self, filename: str):
        """Load FAISS index and documents from disk"""
        self.index = faiss.read_index(f"{filename}.index")
        with open(f"{filename}.json", 'r') as f:
            self.utterances = json.load(f)

        print(f'Loaded Vector Database from {filename}.index and {filename}.index')