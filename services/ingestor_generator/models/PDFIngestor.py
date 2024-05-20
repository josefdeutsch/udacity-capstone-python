import os
import subprocess
from typing import List
from services.ingestor_generator.base.QuoteModel import QuoteModel
from services.ingestor_generator.base.IngestorInterface import IngestorInterface
from util.Util import get_file, is_path   

class PDFIngestor(IngestorInterface):
    """
    An ingestor class to parse quotes from PDF files.

    This class inherits from the IngestorInterface and implements the
    parse method to read quotes from PDF files.
    """
    allowed_extensions = ['pdf']
    
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Determine if the given file can be ingested based on its extension.

        Args:
            path (str): The file path to check.

        Returns:
            bool: True if the file extension is in the list of allowed extensions, False otherwise.
        """
        return path.split('.')[-1].lower() in cls.allowed_extensions

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse quotes from a PDF file and return a list of QuoteModel instances.

        This method reads a PDF file specified by the given path, converts it to text,
        extracts quote data, and returns a list of QuoteModel instances representing
        the quotes. Each line in the PDF file is expected to contain a quote in the 
        format "quote - author". If the file cannot be ingested due to an unsupported 
        file extension, a ValueError is raised. If an error occurs during PDF processing,
        an error message is printed and an empty list is returned.

        Args:
            path (str): The file path to the PDF file containing the quotes.

        Returns:
            List[QuoteModel]: A list of QuoteModel instances parsed from the PDF file.

        Raises:
            ValueError: If the file extension is not supported for ingestion.
        """
        if not cls.can_ingest(path):
            raise ValueError("Cannot ingest given file extension, allowed extensions are: {}".format(cls.allowed_extensions))
       
        # Use the utility function to check and adjust the file path
        path = is_path(path, get_file('default','default.pdf'))
       
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

