import os

def check_file_path(path: str, default_path: str) -> str:
    """
    Checks if the file at the given path exists. If not, returns the default path.
    
    :param path: The path to the file to check.
    :param default_path: The path to the default file to use if the primary file does not exist.
    :return: The path to be used for reading the file.
    """
    if os.path.exists(path):
        return path
    else:
        print(f"File not found at {path}, using default file at {default_path}.")
        return default_path
