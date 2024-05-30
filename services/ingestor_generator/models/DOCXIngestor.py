import os
from typing import List
from docx import Document

from services.ingestor_generator.base.IngestorInterface import IngestorInterface
from services.ingestor_generator.base.QuoteModel import QuoteModel
from util.Utils import Utils


class DOCXIngestor(IngestorInterface):
    """
    An ingestor class to parse quotes from DOCX files.

    This class inherits from the IngestorInterface and implements the
    parse method to read quotes from DOCX files.
    """
    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse quotes from a DOCX file and return a list of QuoteModel instances.

        This method reads a DOCX file specified by the given path, extracts
        quote data, and returns a list of QuoteModel instances representing
        the quotes. Each paragraph in the DOCX file is expected to contain
        a quote in the format "body - author". If an error occurs during
        parsing, an error message is printed.

        Args:
            path (str): The file path to the DOCX file containing the quotes.

        Returns:
            List[QuoteModel]: A list of QuoteModel instances parsed from the DOCX file.
        """
        quotes = []
        # Use the utility function to check and adjust the file path
        path = Utils.validate_image_path(path, Utils.retrieve_file_path('default','default.docx')) 
        try:
            doc = Document(path)
            for para in doc.paragraphs:
                if para.text != "":
                    parse = para.text.split(' - ')
                    if len(parse) >= 2:
                        new_quote = QuoteModel(body=parse[0], author=parse[1])
                        quotes.append(new_quote)
        except Exception as e:
            # Handle any type of Exception that might occur during the document read
            print(f"An error occurred while parsing the DOCX file: {e}")
        
        return quotes