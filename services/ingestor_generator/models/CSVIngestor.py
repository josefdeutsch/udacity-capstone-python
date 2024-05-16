import csv
import os
from typing import List

from services.ingestor_generator.base.IngestorInterface import IngestorInterface
from services.ingestor_generator.base.QuoteModel import QuoteModel

import pandas as pd
from typing import List

from util.Util import check_file_path

class CSVIngestor(IngestorInterface):
    allowed_extensions = ['csv']
    # Path to the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the root of the ingestor_generator
    root_dir = os.path.dirname(script_dir)

    # Path to the default.txt file
    default_path = os.path.join(root_dir, 'res', 'quotes', 'default.txt')

   # @classmethod
   # def parse(cls, path: str) -> List[QuoteModel]:
   #     quotes = []
   #     data = pd.read_csv(path)
   #     for _, row in data.iterrows():
   #         new_quote = QuoteModel(body=row['body'], author=row['author'])
   #        quotes.append(new_quote)
   #     return quotes

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
            quotes = []
            # Use the utility function to check the file path
            path = check_file_path(path, cls.default_path)
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
