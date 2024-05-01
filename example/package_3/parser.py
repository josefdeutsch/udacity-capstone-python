import csv

def parse_csv(path: str):
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

# Assuming 'example.csv' is in your current directory

import json

def parse_json(path: str):
    with open(path, 'r') as jsonfile:
        return json.load(jsonfile)

# Assuming 'data.json' is in your current directory
