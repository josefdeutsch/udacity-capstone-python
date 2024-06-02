import inspect
import os
import re
from typing import List, Tuple
from PIL import Image, ImageFont
from config import load_config


class Utils:

    @staticmethod
    def validate_image_path(path: str, default_path: str) -> str:
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

    @staticmethod
    def resolve_image_path(file_path, default_path) -> str:
        """
        Resolve the provided file path by checking if it is a valid image file and not a hidden file.

        Args:
            file_path (str): The path to the file.
            default_path (str): The default path to return if the file_path is invalid.

        Returns:
            str: The file path if valid and not hidden, otherwise the default path.
        """
        # Check if the file is hidden
        if os.path.basename(file_path).startswith('.'):
            return default_path
        
        # Check if the file is a valid image
        try:
            with Image.open(file_path) as img:
                img.verify()
            return file_path
        except (IOError, SyntaxError) as e:
            return default_path
   
    @staticmethod
    def load_font(font_path: str) -> ImageFont.ImageFont:
        """
        Checks if the font file at the given path exists. If the path is invalid or the font file does not exist,
        returns a default font object.

        :param font_path: The path to the font file to check.
        :return: An ImageFont object.
        """
        if font_path is None or font_path == "" or not os.path.exists(font_path):
            if font_path is None or font_path == "":
                print("No valid font path provided, using default font.")
            else:
                print(f"Font not found at {font_path}, using default font.")
            return ImageFont.load_default()
        else:
            return ImageFont.truetype(font_path)

    @staticmethod
    def calculate_font_size(font: ImageFont.ImageFont, text: str, height: int) -> ImageFont.FreeTypeFont:
        """
        Adjust the font size based on the given font, text, and height.

        The font size is determined by the length of the text.
        The length is mapped to a font size using linear interpolation
        to ensure smooth transitions within the range of 0 to 256.
        If the default font is used, no adjustment is made.

        Args:
            font (ImageFont.ImageFont): The font object.
            text (str): The text whose length is used to calculate the font size.
            height (int): The height value used to calculate the font size.

        Returns:
            ImageFont.FreeTypeFont: The adjusted font object.
            None: If an error occurs.
        """
        try:
            # Check if the font is the default font
            if font == ImageFont.load_default():
                print("ImageFont not found, using default font.")
                return font

            text_length = len(text)

            # Linear interpolation to determine the font size
            if text_length <= 128:
                font_size = height * (0.05 - (0.01 * (text_length / 128)))
            elif text_length <= 256:
                font_size = height * (0.04 - (0.01 * ((text_length - 128) / 128)))
            else:
                font_size = height * (0.03 - (0.01 * ((text_length - 256) / 256)))

            print(f"Text length: {text_length}, Calculated font size: {font_size}")

            font_path = font.path  # Assuming the font object has a 'path' attribute
            return ImageFont.truetype(font_path, int(font_size))
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return None
        
    @staticmethod
    def split_text_into_lines(draw, text, font, max_width):
        """
        Splits the provided text into multiple lines to fit within the specified maximum width.

        Args:
            draw (ImageDraw.Draw): The ImageDraw object used to measure text size.
            text (str): The text to be split into multiple lines.
            font (ImageFont.FreeTypeFont): The font used to measure the text.
            max_width (int): The maximum width allowed for each line.

        Returns:
            str: The input text split into multiple lines, separated by newline characters.
        """
        lines = []
        words = text.split()
        current_line = words.pop(0)

        for word in words:
            test_line = f"{current_line} {word}"
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)  # Add the last line
        return '\n'.join(lines)    


    @staticmethod
    def format_text_with_line_breaks(full_text):
        """
        Splits the given text at " - " and joins the parts with a newline character, retaining the delimiter.
        
        Args:
            full_text (str): The text containing a quote and an author separated by " - ".
            
        Returns:
            str: The formatted text with the quote and author on separate lines, retaining the delimiter.
        """
        parts = full_text.split(" - ")
        if len(parts) == 2:
            formatted_text = f"{parts[0]}\n- {parts[1]}"
        else:
            formatted_text = full_text  # If the expected delimiter is not found, return the original text
        return formatted_text

    @staticmethod
    def get_text_segments(formatted_text):
        """
        Splits the formatted text into segments and marks whether each segment is an author.
        
        Args:
            formatted_text (str): The formatted text with quote and author on separate lines.
            
        Returns:
            list of tuples: Each tuple contains a text line and a boolean indicating if it's the author.
        """
        lines = formatted_text.split('#')
        return [(line, index == 1) for index, line in enumerate(lines)]
    
    @staticmethod
    def prefix_string(text: str) -> str:
        """
        Prefixes the given string with a '#' if it does not already start with one.

        Parameters:
        text (str): The input string.

        Returns:
        str: The input string prefixed with a '#' if not already present.
        """
        if text.startswith('#'):
            return text
        return f"#{text}"
    
    @staticmethod
    def remove_separators(input_string):
        """
        Remove all spaces, dots, underscores, or other separators from the input string.

        Parameters:
        input_string (str): The string from which separators will be removed.

        Returns:
        str: The input string with all separators removed.
        """
        return re.sub(r'[\s._]+', '', input_string)
    
    @staticmethod
    def add_spaces(input_string):
        """
        Add a space between lowercase and uppercase letters in the input string.

        Parameters:
        input_string (str): The string in which spaces will be added between lowercase and uppercase letters.

        Returns:
        str: The modified string with spaces added between lowercase and uppercase letters.
        """
        return re.sub(r'([a-z])([A-Z])', r'\1 \2', input_string)

    @staticmethod
    def locate_project_root(starting_directory: str, marker: str = ".git") -> str:
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


    @staticmethod
    def retrieve_file_path(category: str, file_name: str) -> str:
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
            root_path = Utils.locate_project_root(os.getcwd())
            config = Utils.load_development_config(root_path)
            cache_path = config.get_file_path(category, file_name)
            return os.path.join(root_path, cache_path)
        except ValueError:
            print("Not available")
            return None
        
    @staticmethod
    def retrieve_file_paths(directory_path: str, valid_extensions: Tuple[str, ...]) -> List[str]:
        """
        Retrieve all file paths with specified extensions from the given directory.

        This function lists all files in the specified directory and filters them to 
        include only those with the given extensions.

        Parameters:
        directory_path (str): The path to the directory containing the files.
        valid_extensions (Tuple[str, ...]): A tuple of valid file extensions to filter by.

        Returns:
        List[str]: A list of full paths to the files in the directory with specified extensions.
        """
        file_paths = [
            os.path.join(directory_path, file_name)
            for file_name in os.listdir(directory_path)
            if file_name.lower().endswith(valid_extensions)
        ]
        return file_paths
    
    @staticmethod    
    def retrieve_file_dir(category: str) -> str:
        """
        Retrieve the default cache directory path for a given category.

        This function constructs the path to the default cache directory based on the
        category provided. It combines the project's root path with the specific 
        path defined in the configuration file.

        Parameters:
        category (str): The category for which the cache directory path is needed.

        Returns:
        str: The full path to the default cache directory. Returns None if the path
            cannot be constructed.

        Raises:
        ValueError: If the configuration path is invalid.
        """
        try:
            root_path = Utils.locate_project_root(os.getcwd())
            config = Utils.load_development_config(root_path)
            cache_path = config.get_directory(category)
            return os.path.join(root_path, cache_path)
        except ValueError:
            print("Not available")
            return None

    @staticmethod
    def load_development_config(root_path: str, config_path='config/development.json'):
        """
        Load the configuration file from the specified root and config paths.

        Args:
            root_path (str): The root directory path.
            config_path (str): The configuration file path.

        Returns:
            The loaded configuration.
        """
        return load_config(os.path.join(root_path, config_path))


    @staticmethod
    def get_calling_child_script_directory(child_dir_name):
        """
        Get the path to a child directory within the calling script's directory.

        Parameters:
        child_dir_name (str): The name of the child directory.

        Returns:
        str: The absolute path to the child directory.
        """
        # Get the frame of the caller
        caller_frame = inspect.stack()[1]
        
        # Get the absolute path of the calling script
        calling_script_path = os.path.abspath(caller_frame.filename)
        
        # Get the directory name of the calling script's absolute path
        calling_script_directory = os.path.dirname(calling_script_path)
        
        # Create the child directory path
        child_directory_path = os.path.join(calling_script_directory, child_dir_name)
        
        # Return the child directory path
        return child_directory_path



    @staticmethod
    def get_calling_script_directory():
        """
        Get the directory name of the calling script's directory.

        Returns:
        str: The absolute path to the calling script's directory.
        """
        # Get the frame of the caller
        caller_frame = inspect.stack()[1]
        
        # Get the absolute path of the calling script
        calling_script_path = os.path.abspath(caller_frame.filename)
        
        # Get the directory name of the calling script's absolute path
        calling_script_directory = os.path.dirname(calling_script_path)
        
        # Return the calling script directory path
        return calling_script_directory

    