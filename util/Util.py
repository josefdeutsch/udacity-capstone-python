import os
from PIL import Image, ImageDraw, ImageFont
from config import load_config

def is_path(path: str, default_path: str) -> str:
    """
    Check if the file at the given path exists. If the path is None, empty, 
    or if the file does not exist, returns the default path.

    Parameters:
    path (str): The path to the file to check. Can be None or an empty string.
    default_path (str): The path to the default file to use if the primary 
                        file does not exist, if the path is None, or if it's empty.

    Returns:
    str: The path to be used for reading the file.
    """
    if path is None or path == "" or not os.path.exists(path):
        if path is None or path == "":
            print(f"No valid file path provided, using default file at {default_path}.")
        else:
            print(f"File not found at {path}, using default file at {default_path}.")
        return default_path
    return path


    

def get_font(font_path: str, height: int) -> ImageFont.FreeTypeFont:
    """
    Checks if the font file at the given path exists, if the path is None, or if it's empty. 
    If the path is invalid or the font file does not exist, returns a default font object.
    Otherwise, returns the font object with size set to 5% of the provided height.

    :param font_path: The path to the font file to check. Can be None or an empty string.
    :param height: The height of the area (e.g., image height) to base the font size on.
    :return: An ImageFont object configured with the appropriate size.
    """
    if font_path is None or font_path == "" or not os.path.exists(font_path):
        if font_path is None or font_path == "":
            print("No valid font path provided, using default font.")
        else:
            print(f"Font not found at {font_path}, using default font.")
        return ImageFont.load_default()
    else:
        font_size = int(height * 0.05)  # Calculate the font size as 5% of the given height
        return ImageFont.truetype(font_path, font_size)



def find_project_root(starting_directory: str, marker: str = ".git") -> str:
    """
    Find the project root directory containing the specified marker.

    This function traverses up the directory tree from the starting directory
    until it finds a directory containing the specified marker (e.g., ".git").

    Parameters:
    starting_directory (str): The directory to start the search from.
    marker (str): The name of the marker file or directory that identifies
                  the project root. Defaults to ".git".

    Returns:
    str: The path to the project root directory containing the marker.

    Raises:
    FileNotFoundError: If the marker is not found in any directory up the
                       tree from the starting directory.
    """
    current_directory = starting_directory
    
    while True:
        if marker in os.listdir(current_directory):
            return current_directory
        new_directory = os.path.dirname(current_directory)
        if new_directory == current_directory:
            raise FileNotFoundError(f"Project root containing {marker} not found")
        current_directory = new_directory


   
def get_default_cache(category: str, file_name: str) -> str:
        """
        Retrieve the default cache path for a given category and file name.

        This function constructs the path to the default cache file based on the
        category and file name provided. It combines the project's root path
        with the specific path defined in the configuration file.

        Parameters:
        category (str): The category for which the cache path is needed.
        file_name (str): The name of the cache file.

        Returns:
        str: The full path to the default cache file. Returns None if the path
            cannot be constructed.

        Raises:
        ValueError: If the configuration path is invalid.
        """
        try:
            root_path = find_project_root(os.getcwd())
            config = load_config_dev(root_path,'config/development.json')
            cache_path = config.get_path(category, file_name)
            return os.path.join(root_path, cache_path)
        except ValueError:
            print("Not available")
            return None


import os

def load_config_dev(root_path: str, config_path: str):
    """
    Load the configuration file from the specified root and config paths.

    Args:
        root_path (str): The root directory path.
        config_path (str): The configuration file path.

    Returns:
        The loaded configuration.
    """
    return load_config(os.path.join(root_path, config_path))


