from scribe import Scribe

from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

if __name__ == "__main__":
    episode_title = 'Episode 1: An Exodus Shaped Reality'
    series_title = 'The Exodus Way'
    bp = Scribe(episode_title, series_title)

    # bp.api_key = os.getenv("ASSEMBLY_API_KEY")

    # speaker_map = {'A': 'John Collins',
    #                'B': 'Tim Mackie'}

    # bp.transcribe('BP_An_Exodus_Shaped_Reality.mp3', verbose=True)
    # bp.add_speaker_labels(speaker_map)
    # bp.save_as_pdf('Episode1.pdf')
    # bp.save_as_json('Episode1.json')

    # bp.add_to_index()
    # bp.save_database('vector_db')
    bp.load_database('vector_db')
    results = bp.search('The way through the desert is the way to God')