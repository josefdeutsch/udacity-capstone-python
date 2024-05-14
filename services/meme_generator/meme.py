import os
import random
from argparse import ArgumentParser

from services.ingestor_generator.base.QuoteModel import QuoteModel
from services.ingestor_generator.ingestor import Ingestor
from services.meme_generator.models.MemeEngine import MemeEngine

def generate_meme(path=None, body=None, author=None):
    """Generate a meme given a path and a quote."""
    img = None
    quote = None

    # Navigate up two levels from the script location
    current_dir = os.path.dirname(__file__)  # Gets the directory where the script is located
    base_dir = os.path.join(current_dir, '..', '..')  # Moves up two directories
    base_dir = os.path.abspath(base_dir)  # Resolves to absolute path

    # Determine the directories for images and quotes
    images_dir = os.path.join(base_dir, "data_private", "res", "img")
    quotes_dir = os.path.join(base_dir, "data_private", "res", "quotes")

    # Select a random image if no path is provided
    if path is None:
        imgs = [os.path.join(root, name) for root, dirs, files in os.walk(images_dir) for name in files]
        img = random.choice(imgs) if imgs else None
    else:
        if not os.path.isabs(path):  # If the path provided is not absolute
            path = os.path.join(base_dir, path)  # Create an absolute path
        img = path

    # Select a random quote if no body and author are provided
    if body is None:
        quote_files = [
            os.path.join(quotes_dir, "DogQuotesCSV.csv"),
            os.path.join(quotes_dir, "DogQuotesDOCX.docx"),
            os.path.join(quotes_dir, "DogQuotesPDF.pdf"),
            os.path.join(quotes_dir, "DogQuotesTXT.txt")
        ]
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))

        quote = random.choice(quotes) if quotes else None
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    # Generate the meme using the MemeEngine class
    meme = MemeEngine(os.path.join('tmp'))
    meme_path = meme.make_meme(img, quote.body, quote.author) if img and quote else "No meme generated."
    return meme_path

def main():
    parser = ArgumentParser(description="Meme Generator CLI")
    parser.add_argument('--path', type=str, help='Path to an image file', default=None)
    parser.add_argument('--body', type=str, help='Quote body to add to the image', default=None)
    parser.add_argument('--author', type=str, help='Quote author to add to the image', default=None)
    
    args = parser.parse_args()

    # Generate meme and print the file path
    try:
        meme_path = generate_meme(args.path, args.body, args.author)
        print(f'Meme created at: {meme_path}')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    main()
