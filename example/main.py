import os
from dotenv import load_dotenv
# example/__init__.py
from example.package_1.awesome_module import hello
from example.package_2.module import hello

def main():
    load_dotenv()
    print(hello)
    hello


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
