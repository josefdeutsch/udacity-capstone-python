import os
from typing import List
from util.Util import get_file, is_path
from services.ingestor_generator.base.IngestorInterface import IngestorInterface
from services.ingestor_generator.base.QuoteModel import QuoteModel
import pandas as pd
from typing import List


class CSVIngestor(IngestorInterface):
    """
    An ingestor class to parse quotes from CSV files.

    This class inherits from the IngestorInterface and implements the
    parse method to read quotes from CSV files.
    """
    allowed_extensions = ['csv']
   

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        
        """
        Parse quotes from a CSV file and return a list of QuoteModel instances.

        This method reads a CSV file specified by the given path, extracts
        quote data, and returns a list of QuoteModel instances representing
        the quotes. If the CSV file is empty, a warning message is printed.
        In case of other errors, an error message is printed.

        Args:
            path (str): The file path to the CSV file containing the quotes.

        Returns:
            List[QuoteModel]: A list of QuoteModel instances parsed from the CSV file.
        """
        
        quotes = []
        # Use the utility function to check and adjust the file path
        path = is_path(path, get_file('default','default.csv'))
        try:
            data = pd.read_csv(path)
            for _, row in data.iterrows():
                new_quote = QuoteModel(body=row['body'], author=row['author'])
                quotes.append(new_quote)
        except pd.errors.EmptyDataError:
            print("Warning: The CSV file is empty.")
        except Exception as e:
            print(f"An error occurred: {e}")
        return quotes
    
