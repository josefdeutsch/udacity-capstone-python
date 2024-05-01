import pytest
import csv
import json
from io import StringIO
from typing import List, Callable, Dict

# Redefine the strategy functions with slight modifications for inline testing
def parse_csv(content: str) -> List[Dict[str, str]]:
    reader = csv.DictReader(StringIO(content))
    return [row for row in reader]

def parse_json(content: str) -> List[Dict[str, int]]:
    return json.loads(content)

# Mapping of file content to parsing functions (simulating paths with content directly)
parsers: Dict[str, Callable[[str], List[Dict]]] = {
    'csv': parse_csv,
    'json': parse_json,
}

# Function to simulate processing of file content directly
def process_content(file_type: str, content: str) -> List[Dict]:
    if file_type in parsers:
        parser_function = parsers[file_type]
        return parser_function(content)
    else:
        raise ValueError(f"Unsupported file type for file_type: {file_type}")

# Test functions
def test_parse_csv():
    csv_content = "name,age\nAlice,30\nBob,25"
    assert parse_csv(csv_content) == [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]

def test_parse_json():
    json_content = '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]'
    assert parse_json(json_content) == [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]

def test_process_content_csv():
    csv_content = "name,age\nAlice,30\nBob,25"
    assert process_content('csv', csv_content) == [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]

def test_process_content_json():
    json_content = '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]'
    assert process_content('json', json_content) == [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]

def test_process_content_unsupported_type():
    with pytest.raises(ValueError) as excinfo:
        process_content('xml', '<data></data>')
    assert 'Unsupported file type for file_type: xml' in str(excinfo.value)

# Run the pytest directly (useful for standalone scripts or demos)
if __name__ == "__main__":
    pytest.main()
