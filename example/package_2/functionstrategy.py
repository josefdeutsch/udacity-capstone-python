import csv
import json
from typing import List, Callable, Dict

# Define the strategy functions
def parse_csv(path: str) -> List[str]:
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

def parse_json(path: str) -> List[str]:
    with open(path, 'r') as jsonfile:
        return json.load(jsonfile)

# Mapping of file extensions to parsing functions
parsers: Dict[str, Callable[[str], List[str]]] = {
    'csv': parse_csv,
    'json': parse_json,
}

# Function to check if the extension can be processed
def can_ingest(path: str) -> bool:
    ext = path.split('.')[-1]
    return ext in parsers

# Context function that uses a strategy function to parse files
def process_file(path: str) -> List[str]:
    ext = path.split('.')[-1]
    if can_ingest(path):
        parser_function = parsers[ext]
        return parser_function(path)
    else:
        raise ValueError(f"Unsupported file type for path: {path}")

# Usage example
if __name__ == "__main__":
    print(process_file("example.csv"))
    print(process_file("data.json"))
