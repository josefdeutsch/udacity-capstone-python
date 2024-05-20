import os
from typing import List
from util.Util import get_file
from services.ingestor_generator.models.CSVIngestor import CSVIngestor
from services.ingestor_generator.models.DOCXIngestor import DOCXIngestor
from services.ingestor_generator.base.QuoteModel import QuoteModel
from services.ingestor_generator.models.TXTIngestor import TXTIngestor
from services.ingestor_generator.models.PDFIngestor import PDFIngestor

class Ingestor:
    ingestors = [CSVIngestor, DOCXIngestor, TXTIngestor, PDFIngestor]  # Add other specific ingestors as needed

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        raise ValueError(f"No ingestor available for file {path}")


def main():

    
    quote_files = [
            get_file('quotes','DogQuotesCSV.csv'), 
            get_file('quotes','DogQuotesDOCX.docx'),
            get_file('quotes','DogQuotesPDF.pdf'),
            get_file('quotes','DogQuotesTXT.txt')
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