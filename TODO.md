1. Refactor Episode class. Move `transcribe()` into the `__init__()` function.
2. Allow Index() to create Episode objects from paths and create a directory of Episode objects within the Index class.
3. Index() should be able to take a directory as input and create episode objects from each file.
4. Add functionality to download from urls as well.
5. Add docstrings and safety measures everywhere. Especially on API calls.
6. Maybe I want to accept a config file that organizes everything more easily, and adds everything from the config file containing paths. Have podcast name, series/season name, episode name.
7. Or different kinds of objects? That the index keeps track of? Podcasts, series, episodes? Each is like a directory?
8. Add the from_url functionality to Index.add_series()
9. Be mindful of default values and allow for more flexible file trees