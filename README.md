# Introducing pod-search
### A tool to automatically transcribe, index, and semantic-search your favorite podcast.
This project was born from a specific frustration I had with *my* favorite podcast, from The BibleProject. While they have begun to transcribe their podcasts, I still struggled to find the lines and ideas that I wanted to revisit or share. pod-search uses Assembly AI's automatic transcription API and Facebook's faiss-cpu package to transcribe, embed, and index podcast episodes in order to be able to easily search semantically for the moments you want to revisit.

## Disclaimer
This project is very much still in development, and I am actively adding methods and documentation to make this project easier to use.

## Using pod-search
I am planning to turn this into an easier-to-use package, but for now users will need to clone this repo in order to use it.
### Installation
#### MacOS / Unix
```bash
cd Documents                                              # Navigate to Documents folder
mkdir pod-search                                          # Make a new folder called WordTree_Game
cd pod-search                                             # Navigate into the new folder
git clone git@github.com:jackdpond/pod-search.git         # Clone this git repository
python3 -m venv venv                                      # Create a virtual environment
source venv/bin/activate                                  # Activate virtual environment
pip install -r requirements.txt                           # Install dependencies
```
#### Windows
```bash
cd Documents                                              # Navigate to Documents folder
mkdir pod-search                                          # Make a new folder called WordTree_Game
cd pod-search                                             # Navigate into the new folder
git clone git@github.com:jackdpond/pod-search.git         # Clone this git repository
python3 -m venv venv                                      # Create a virtual environment
.\venv\Scripts\activate                                   # Activate virtual environment
pip install -r requirements.txt                           # Install dependencies
```
### Creating a searchable index
The `Index()` object will be created using `Episode()` objects, each of which will have attributes `series_name` and `episode_name`. That way, when we search, the results appear with a series/season name, episode name, and a time stamp.

The `Index()` object has a method `.add_episode()` which can be used to add individual episodes via file path or url. This can be used as follows:
```python
from scribe import Index

index = Index()
index.add_episode(episode_title: str, series_title: str, audio_file_path: str)
# or
index.add_episode(episode_title: str, series_title: str, audio_url: str)
```

However, the easier method is to use `Index.add_series()`, which allows the user to add an entire podcast series or season by setting up the file tree in a particular way. `.add_series()` accepts either a file directory or a .txt file listing urls.
##### Directory method
```
pod-search/
├── README.md
├── requirements.txt
├── .gitignore
├── scripts/
│ └── transcripts/
│ └── database/
│ └── <Podcast_Title_Here>/
│   ├── <Episode_1_Title>.mp3
│   ├── <Episode_2_Title>.mp3
│   ├── <Episode_3_Title>.mp3
│ ├── search.py
│ ├── experiment.py
│ ├── scribe.py
```

##### Urls list method
```
pod-search/
├── README.md
├── requirements.txt
├── .gitignore
├── scripts/
│ └── transcripts/
│ └── database/
│ ├── <Podcast_Title_Here>.txt
│ ├── search.py
│ ├── experiment.py
│ ├── scribe.py
```
Where the <Podcast_Title_Here>.txt contains one podcast episode title along with its corresponding url per line, separated by a comma, like so:
```txt
Episode 1,https://episode1.url-ish-text-here.112233
Episode 2,https://episode2.url-ish-text-here.445566
Episode 3,https://episode3.url-ish-text-here.778899
```

Once the file tree is set up after the preferred manner, the `Index.add_series()` method is used like so:
```python
from scribe import Index

index = Index()

index.add_series(directory_path: str)
# or
index.add_series(urls_list_path: str)
```
This will take a few minutes to run. Once it is finished, you will have a vector database that is ready to search!

### Search
The search.py script is for searching the index. Because it is an index of sentence embeddings, you will be able to search semantically, not using keywords.

```bash
cd scripts/
python3 search.py 'Type your own query here!' --filename <path/to/vector/database> --k-nearest-neighbors <how many results to display>
```

## Use of AI in this project
While I am not opposed to using AI to code and develop, I decided to use AI minimally to build this tool. I used ChatGPT for advice while choosing to use an AI transcription service and a vector database package, ultimately deciding on Assembly AI and FAISS, respectively.

For the code itself, I wrote and organized without AI, with the exception of the function `Episode.save_as_pdf()`, which uses a somewhat complicated package with which I am unfamiliar. I looked up documentation and consulted Stack Overflow when I had questions--which was often.

I am both grateful and excited for the opportunities AI-coding or vibe-coding has created and will create, I still plan to develop my own coding skills, which include a rote knowledge of syntax, but also critical thinking, reasoning, and creativity. I am aware that I could have created a better, neater, more functional tool more quickly using Cursor or ChatGPT, but a neat, functional tool was not my primary object in building pod-search. 

Perhaps pod-search marks a fork in my time spent coding from here on out. Perhaps from now on, I will code with one of two objects, or two mindesets. First, with a neat, functional final product in mind, or second, with the building of my brain and my character in mind. Maybe I will do the first in my profession, and the second as a hobby. 

I don't know how AI will change programming and I don't know how AI will change me. However, building pod-search has been both stimulating, frustrating, and relaxing for me, and I have enjoyed it immensely. 

## License
This project is licensed under the Apache 2.0 License - see the LICENSE file for details.


