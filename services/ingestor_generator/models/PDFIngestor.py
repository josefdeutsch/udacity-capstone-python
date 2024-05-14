import os
import subprocess
from typing import List
from services.ingestor_generator.base.QuoteModel import QuoteModel
from services.ingestor_generator.base.IngestorInterface import IngestorInterface

class PDFIngestor(IngestorInterface):
    allowed_extensions = ['pdf']

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        ext = path.split('.')[-1].lower()  # Ensure the check is case-insensitive
        return ext in cls.allowed_extensions

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise ValueError(f"Cannot ingest given file extension, allowed extensions are: {cls.allowed_extensions}")

        temp_txt = '/tmp/temp_file.txt'  # Temporary file to store the text output
        try:
            # Using subprocess to call pdftotext and convert PDF to text
            subprocess.run(['/Applications/xpdf/bin64/pdftotext', '-layout', path, temp_txt], check=True)

            quotes = []
            # Reading from the temporary text file
            with open(temp_txt, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        # Assuming each line contains a quote and its author in the format: "quote" - author
                        parts = line.split(' - ')
                        if len(parts) == 2:
                            quote, author = parts
                            quotes.append(QuoteModel(quote.strip(), author.strip()))
        finally:
            # Ensure the temporary file is deleted
            os.remove(temp_txt)
        
        return quotes

# Example usage:
# Assuming a PDF file 'example.pdf' exists and contains quotes in the assumed format.
# quotes = PDFIngestor.parse('/path/to/example.pdf')
# for quote in quotes:
#     print(f"{quote.text} by {quote.author}")

# Example usage:
# Assuming a PDF file 'example.pdf' exists and contains quotes in the assumed format.
# quotes = PDFIngestor.parse('/path/to/example.pdf')
# for quote in quotes:
#     print(f"{quote.text} by {quote.author}")

