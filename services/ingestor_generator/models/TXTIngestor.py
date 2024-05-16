import os
from typing import List
from services.ingestor_generator.base.IngestorInterface import IngestorInterface
from services.ingestor_generator.base.QuoteModel import QuoteModel
from util.Util import check_file_path

class TXTIngestor(IngestorInterface):
    allowed_extensions = ['txt']

    # Path to the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the root of the ingestor_generator
    root_dir = os.path.dirname(script_dir)

    # Path to the default.txt file
    default_path = os.path.join(root_dir, 'res', 'quotes', 'default.txt')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        path = check_file_path(path, cls.default_path)  # Use the utility function to adjust the file path

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
