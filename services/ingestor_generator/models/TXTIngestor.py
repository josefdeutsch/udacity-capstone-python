from typing import List
from services.ingestor_generator.base.IngestorInterface import IngestorInterface
from services.ingestor_generator.base.QuoteModel import QuoteModel
from util.Utils import Utils

class TXTIngestor(IngestorInterface):
    """
    An ingestor class to parse quotes from TXT files.

    This class inherits from the IngestorInterface and implements the
    parse method to read quotes from TXT files.
    """
    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse quotes from a text file and return a list of QuoteModel instances.

        This method reads a text file specified by the given path, extracts
        quote data, and returns a list of QuoteModel instances representing
        the quotes. Each line in the text file is expected to contain a quote
        in the format "quote - author". If an error occurs during file reading,
        an error message is printed and an empty list is returned.

        Args:
            path (str): The file path to the text file containing the quotes.

        Returns:
            List[QuoteModel]: A list of QuoteModel instances parsed from the text file.
        """
        # Use the utility function to check and adjust the file path
        path = Utils.validate_image_path(path, Utils.retrieve_file_path('default','default.txt')) 
        try:
            quotes = []
            with open(path, 'r', encoding='utf-8') as file:  # Ensuring to handle encoding
                lines = file.readlines()
                for line in lines:
                    if line.strip():
                        parse = line.strip().split(' - ')
                        if len(parse) >= 2:
                            new_quote = QuoteModel(body=parse[0], author=parse[1])
                            quotes.append(new_quote)
            return quotes
        except Exception as e:
            # Handle exceptions related to file opening or reading
            print(f"An error occurred while reading the text file: {e}")
            return []  
