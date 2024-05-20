from dataclasses import dataclass

@dataclass
class QuoteModel:
    """
    A data class to represent a quote.

    Attributes:
        body (str): The text of the quote.
        author (str): The author of the quote.
    """
    body: str
    author: str
