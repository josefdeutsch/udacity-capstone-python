import os

def check_file_path(path: str, default_path: str) -> str:
    """
    Checks if the file at the given path exists. If the path is None or if the file does not exist, returns the default path.
    
    :param path: The path to the file to check. Can be None.
    :param default_path: The path to the default file to use if the primary file does not exist or if path is None.
    :return: The path to be used for reading the file.
    """
    if path is None or not os.path.exists(path):
        if path is None:
            print(f"No file path provided, using default file at {default_path}.")
        else:
            print(f"File not found at {path}, using default file at {default_path}.")
        return default_path
    else:
        return path