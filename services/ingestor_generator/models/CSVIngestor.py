import csv
from typing import List

from services.ingestor_generator.base.IngestorInterface import IngestorInterface
from services.ingestor_generator.base.QuoteModel import QuoteModel

import pandas as pd
from typing import List

class CSVIngestor(IngestorInterface):
    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        quotes = []
        data = pd.read_csv(path)
        for _, row in data.iterrows():
            new_quote = QuoteModel(body=row['body'], author=row['author'])
            quotes.append(new_quote)
        return quotes
