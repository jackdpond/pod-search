1. Refactor Episode class. Move `transcribe()` into the `__init__()` function.
2. Allow Index() to create Episode objects from paths and create a directory of Episode objects within the Index class.
3. Index() should be able to take a directory as input and create episode objects from each file.
4. Add functionality to download from urls as well.
5. Add docstrings and safety measures everywhere. Especially on API calls.