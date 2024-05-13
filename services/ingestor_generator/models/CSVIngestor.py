import csv
from typing import List

from services.ingestor_generator.base.IngestorInterface import IngestorInterface
from services.ingestor_generator.base.QuoteModel import QuoteModel

class CSVIngestor(IngestorInterface):
    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        quotes = []
        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                new_quote = QuoteModel(body=row['body'], author=row['author'])
                quotes.append(new_quote)
        return quotes
