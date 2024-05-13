from typing import List
from dotenv import load_dotenv
from services.ingestor_generator.models.CSVIngestor import CSVIngestor
from services.ingestor_generator.models.DOCXIngestor import DOCXIngestor
from services.ingestor_generator.base.QuoteModel import QuoteModel
from services.ingestor_generator.models.TXTIngestor import TXTIngestor

class Ingestor:
    ingestors = [CSVIngestor, DOCXIngestor, TXTIngestor]  # Add other specific ingestors as needed

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        raise ValueError(f"No ingestor available for file {path}")

def main():
    load_dotenv()
    quote_files = [
        '/Users/Joseph/udacity-capstone-python/python-structure-template/data_private/res/quotes/DogQuotesCSV.csv',
        '/Users/Joseph/udacity-capstone-python/python-structure-template/data_private/res/quotes/DogQuotesDOCX.docx',
        '/Users/Joseph/udacity-capstone-python/python-structure-template/data_private/res/quotes/DogQuotesPDF.pdf',
        '/Users/Joseph/udacity-capstone-python/python-structure-template/data_private/res/quotes/DogQuotesTXT.txt'
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