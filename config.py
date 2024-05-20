import json
from threading import Lock

class Config:
    _instance = None
    _lock = Lock()


    def __new__(cls, json_file=None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Config, cls).__new__(cls)
                    cls._instance._initialize(json_file)
        return cls._instance

    def _initialize(self, json_file):
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

    def get_path(self, category, file_name):

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


def load_config(json_file):
    return Config(json_file)

