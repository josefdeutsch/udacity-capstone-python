import os
from typing import List
from docx import Document

from services.ingestor_generator.base.IngestorInterface import IngestorInterface
from services.ingestor_generator.base.QuoteModel import QuoteModel
from util.Util import check_file_path


class DOCXIngestor(IngestorInterface):
    allowed_extensions = ['docx']
      # Path to the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the root of the ingestor_generator
    root_dir = os.path.dirname(script_dir)

    # Path to the default.txt file
    default_path = os.path.join(root_dir, 'res', 'quotes', 'default.docx')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        quotes = []
        path = check_file_path(path, cls.default_path)  # Use the utility function to check and adjust the file path
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