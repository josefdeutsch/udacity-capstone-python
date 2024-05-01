from abc import ABC, abstractmethod
import csv
import json
from typing import List

class Importer(ABC):
    @abstractmethod
    def parse(self, path: str) -> List:
        pass

class CSVImporter(Importer):
    def parse(self, path: str) -> List:
         with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader]

class JSONImporter(Importer):
    def parse(self, path: str) -> List:
         with open(path, 'r') as jsonfile:
            return json.load(jsonfile)

class FileProcessor:
    def __init__(self, importer: Importer):
        self.importer = importer

    def process_file(self, path: str):
        return self.importer.parse(path)


