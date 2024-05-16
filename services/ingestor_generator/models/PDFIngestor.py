import os
import subprocess
from typing import List
from services.ingestor_generator.base.QuoteModel import QuoteModel
from services.ingestor_generator.base.IngestorInterface import IngestorInterface
from util.Util import check_file_path  # Ensure this path is correct

class PDFIngestor(IngestorInterface):
    allowed_extensions = ['pdf']

    # Path to the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the root of the ingestor_generator
    root_dir = os.path.dirname(script_dir)

    # Path to the default.txt file
    default_path = os.path.join(root_dir, 'res', 'quotes', 'default.pdf')
    
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        return path.split('.')[-1].lower() in cls.allowed_extensions

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise ValueError("Cannot ingest given file extension, allowed extensions are: {}".format(cls.allowed_extensions))
        
        path = check_file_path(path, cls.default_path)
        temp_txt = '/tmp/temp_file.txt'
        
        try:
            # Attempt to convert PDF to text using pdftotext
            subprocess.run(['/Applications/xpdf/bin64/pdftotext', '-layout', path, temp_txt], check=True)
            quotes = []
            with open(temp_txt, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        parts = line.split(' - ')
                        if len(parts) == 2:
                            quote, author = parts
                            quotes.append(QuoteModel(quote.strip(), author.strip()))
        except Exception as e:
            # Handle exceptions related to file processing or subprocess execution
            print(f"Failed to process PDF file: {e}")
            return []  # Return an empty list or handle differently based on your application needs
        finally:
            # Clean up by ensuring the temporary file is removed
            if os.path.exists(temp_txt):
                os.remove(temp_txt)
        
        return quotes

# Usage example remains the same
