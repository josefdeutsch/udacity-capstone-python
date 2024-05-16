import os
from PIL import Image, ImageDraw, ImageFont

def check_file_path(path: str, default_path: str) -> str:
    """
    Checks if the file at the given path exists. If the path is None, empty, or if the file does not exist, returns the default path.
    
    :param path: The path to the file to check. Can be None or an empty string.
    :param default_path: The path to the default file to use if the primary file does not exist, if the path is None, or if it's empty.
    :return: The path to be used for reading the file.
    """
    if path is None or path == "" or not os.path.exists(path):
        if path is None or path == "":
            print(f"No valid file path provided, using default file at {default_path}.")
        else:
            print(f"File not found at {path}, using default file at {default_path}.")
        return default_path
    else:
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
