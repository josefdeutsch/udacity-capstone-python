from typing import List
from docx import Document

from services.ingestor_generator.base.IngestorInterface import IngestorInterface
from services.ingestor_generator.base.QuoteModel import QuoteModel


class DOCXIngestor(IngestorInterface):
    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        quotes = []
        doc = Document(path)
        for para in doc.paragraphs:
            if para.text != "":
                parse = para.text.split(' - ')
                if len(parse) >= 2:
                    new_quote = QuoteModel(body=parse[0], author=parse[1])
                    quotes.append(new_quote)
        return quotes
