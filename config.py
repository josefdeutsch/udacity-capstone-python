"""
This module provides a singleton Config class to handle configuration settings from a JSON file.
It ensures only one instance of the configuration is created, even in a multi-threaded environment.

Classes:
    Config: A singleton class to load and provide access to configuration settings.
"""

import json
from threading import Lock

class Config:
    """
    A singleton class to load and provide access to configuration settings from a JSON file.
    
    Attributes:
        metadata (dict): Metadata information from the JSON configuration.
        config (dict): Configuration settings from the JSON configuration.
        debug (bool): Debug setting.
        database (dict): Database configuration settings.
        logging (dict): Logging configuration settings.
        paths (dict): Directory paths for various categories.
        files (dict): File listings for various categories.
    """

    _instance = None
    _lock = Lock()


    def __new__(cls, json_file=None):
        """
        Ensure only one instance of the Config class is created.
        
        Args:
            json_file (str, optional): Path to the JSON file containing configuration settings.
        
        Returns:
            Config: The singleton instance of the Config class.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Config, cls).__new__(cls)
                    cls._instance._initialize(json_file)
        return cls._instance

    def _initialize(self, json_file):
        """
        Initialize the configuration settings from the JSON file.
        
        Args:
            json_file (str): Path to the JSON file containing configuration settings.
        
        Raises:
            ValueError: If the JSON file is not provided or if required categories or files are missing.
        """
        if not hasattr(self, 'initialized'):
            if json_file is None:
                raise ValueError("A JSON file must be provided for the initial configuration load.")

            with open(json_file, 'r') as file:
                data = json.load(file)

            # Metadata
            self.metadata = data.get("metadata", {})

            # Configuration settings
            self.config = data.get("config", {})

            # Extracting individual settings for easier access if needed
            self.debug = self.config.get("debug", False)
            self.database = self.config.get("database", {})
            self.logging = self.config.get("logging", {})
            self.paths = self.config.get("paths", {})
            self.files = self.config.get("files", {})

            self.initialized = True

    def get_file_path(self, category, file_name):
        """
        Get the full path of a file given its category and name.
        :param category: str - Category of the file ('fonts', 'quotes', 'images', 'default')
        :param file_name: str - Name of the file
        :return: str - Full path to the file
        """
        path = self.paths.get(category)
        if path is None:
            raise ValueError(f"Category '{category}' not found in paths.")
        
        if file_name not in self.files.get(category, []):
            raise ValueError(f"File '{file_name}' not found in files under category '{category}'.")
        
        return f"{path}/{file_name}"
    

    def get_directory(self, category):
        """
        Get the directory path of a category.
        :param category: str - Category of the file ('fonts', 'quotes', 'images', 'default')
        :return: str - Directory path for the category
        """
        path = self.paths.get(category)
        if path is None:
            raise ValueError(f"Category '{category}' not found in paths.")
        
        return path



def load_config(json_file):
    """
    Load the configuration from the given JSON file.
    
    Args:
        json_file (str): Path to the JSON file containing configuration settings.
    
    Returns:
        Config: The singleton instance of the Config class.
    """
    return Config(json_file)

