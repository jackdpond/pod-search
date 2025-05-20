from scribe2 import Episode, Index

from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

if __name__ == "__main__":
    # episode_title = 'Episode 1: An Exodus Shaped Reality'
    # series_title = 'The Exodus Way'
    # bp = Episode(episode_title, series_title)

    # bp.api_key = os.getenv("ASSEMBLY_API_KEY")

    # speaker_map = {'A': 'John Collins',
    #                'B': 'Tim Mackie'}

    # bp.transcribe('audio_files/BP_An_Exodus_Shaped_Reality.mp3', verbose=True)
    # bp.add_speaker_labels(speaker_map)
    # bp.save_as_pdf('transcripts/Episode1.pdf')
    # bp.save_as_json('transcripts/Episode1.json')

    db = Index()
    # db.add_episode(bp)
    # db.save_database('database/vector_db')
    db.load_database('database/vector_db')
    results = db.search('The way through the desert is the way to God')