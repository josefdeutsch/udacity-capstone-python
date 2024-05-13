from typing import List
from services.ingestor_generator.base.IngestorInterface import IngestorInterface
from services.ingestor_generator.base.QuoteModel import QuoteModel

class TXTIngestor(IngestorInterface):
    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        quotes = []
        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.strip():
                    parse = line.strip().split(' - ')
                    if len(parse) >= 2:
                        new_quote = QuoteModel(body=parse[0], author=parse[1])
                        quotes.append(new_quote)
        return quotes
