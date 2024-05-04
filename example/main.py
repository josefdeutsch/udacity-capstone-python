import argparse
import logging
import os
import subprocess
from dotenv import load_dotenv

from example.package_1.objectstrategy import CSVImporter, FileProcessor
from example.package_2.functionstrategy import process_file
# example/__init__.py


def main():
    load_dotenv()
    #parser = argparse.ArgumentParser(description="Example script to demonstrate argparse usage.")
    
    # Add arguments
    #parser.add_argument('--name', type=str, required=True, help='Enter your name')
    #parser.add_argument('--age', type=int, required=True, help='Enter your age')

    # Parse arguments
    #args = parser.parse_args()

    # Call the main function with parsed arguments
    #print(f"Hello, {args.name}! You entered age {args.age}.")

    result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
    print(result.stdout)

        # Assuming 'example.csv' is in your current directory
    # print('*** Functional Strategy *** :')
    # print(process_file('/Users/Joseph/Documents/Template/python-structure-template/example/res/example.csv'))
    # print(process_file('/Users/Joseph/Documents/Template/python-structure-template/example/res/example.json'))
        
    # print('*** Object Strategy *** :')
    # csv_importer = CSVImporter()
    # processor = FileProcessor(csv_importer)
    # print(processor.process_file('/Users/Joseph/Documents/Template/python-structure-template/example/res/example.csv'))
    # print(processor.process_file('/Users/Joseph/Documents/Template/python-structure-template/example/res/example.json'))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error("Failed to run main function", exc_info=True)


# Environment variables are read as strings
db_port = os.getenv('DB_PORT')

# Convert to integer
db_port = int(db_port)

# Handling boolean
use_cache = os.getenv('USE_CACHE').lower() == 'true'
