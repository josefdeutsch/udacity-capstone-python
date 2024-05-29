"""
This module provides functionality to parse various file types to extract quotes.
It uses specific ingestor classes for different file formats.

Classes:
    Ingestor

Functions:
    main()
"""

from typing import List
from util.Utils import Utils
from services.ingestor_generator.models.CSVIngestor import CSVIngestor
from services.ingestor_generator.models.DOCXIngestor import DOCXIngestor
from services.ingestor_generator.base.QuoteModel import QuoteModel
from services.ingestor_generator.models.TXTIngestor import TXTIngestor
from services.ingestor_generator.models.PDFIngestor import PDFIngestor

class Ingestor:
    """
    Class to handle the ingestion of different file types using specific ingestors.

    Attributes:
        ingestors (list): List of ingestor classes that can parse different file types.
    """

    ingestors = [CSVIngestor, DOCXIngestor, TXTIngestor, PDFIngestor]  # Add other specific ingestors as needed

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        raise ValueError(f"No ingestor available for file {path}")


def main():

    quote_files = [
            Utils.retrieve_file_path('quotes','DogQuotesCSV.csv'), 
            Utils.retrieve_file_path('quotes','DogQuotesDOCX.docx'),
            Utils.retrieve_file_path('quotes','DogQuotesPDF.pdf'),
            Utils.retrieve_file_path('quotes','DogQuotesTXT.txt')
        ]


    quotes = []
    for file_path in quote_files:
       try:
            quotes.extend(Ingestor.parse(file_path))
       except ValueError as e:
            print(e)

    for quote in quotes:
       print(f'"{quote.body}" - {quote.author}')

if __name__ == "__main__":
    main()