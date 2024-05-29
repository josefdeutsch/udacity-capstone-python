import os
from PIL import Image, ImageFont
from config import load_config

class Utils:

    @staticmethod
    def get_valid_path(path: str, default_path: str) -> str:
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
    def check_against_hidden_files(file_path):
        """
        Check if the provided file path is a valid image file and not a hidden file.
        
        Args:
            file_path (str): The path to the file.
        
        Returns:
            bool: True if the file is a valid image and not a hidden file, False otherwise.
        """
        # Check if the file is hidden
        if os.path.basename(file_path).startswith('.'):
            return False
        
        # Check if the file is a valid image
        try:
            with Image.open(file_path) as img:
                img.verify()
            return True
        except (IOError, SyntaxError) as e:
            return False
   
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
    def calculate_font_size(font: ImageFont.ImageFont, font_path: str, height: int) -> ImageFont.FreeTypeFont:
        """
        If the font is not the default font, calculates the font size as 5% of the given height
        and returns the appropriate font object.

        :param font: The ImageFont object loaded from the font path.
        :param font_path: The path to the font file.
        :param height: The height of the area to base the font size on.
        :return: An ImageFont object with the appropriate size.
        """
        if font != ImageFont.load_default():
            font_size = int(height * 0.05)  # Calculate the font size as 5% of the given height
            return ImageFont.truetype(font_path, font_size)
        else:
            return font


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




    