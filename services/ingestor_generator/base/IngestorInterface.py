from abc import ABC, abstractmethod
from typing import List

from services.ingestor_generator.base.QuoteModel import QuoteModel

class IngestorInterface(ABC):
    allowed_extensions = []
    """
    An abstract base class for quote ingestors, defining the interface for parsing quotes from different file formats.

    Attributes:
        allowed_extensions (list): A list of file extensions that the ingestor can handle.
    """

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Determine if the given file can be ingested based on its extension.

        Args:
            path (str): The file path to check.

        Returns:
            bool: True if the file extension is in the list of allowed extensions, False otherwise.
        """
        ext = path.split('.')[-1]
        return ext in cls.allowed_extensions

    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse quotes from the given file.

        This method must be implemented by subclasses to handle the parsing
        of quotes from specific file formats.

        Args:
            path (str): The file path to parse.

        Returns:
            List[QuoteModel]: A list of QuoteModel instances parsed from the file.
        """

        pass
    
    


    
  