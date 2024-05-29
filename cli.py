"""
This module provides a command-line interface (CLI) for generating memes.
The script allows the user to specify an image path, a quote body, and an author
to create a meme. If no image path or quote is provided, random selections are made.

Usage:
    python main_script.py --path <path_to_image> --body <quote_body> --author <quote_author>
"""

from argparse import ArgumentParser
from services.meme_generator.MemeGenerator import generate_meme

def main():
    """
    Main function to parse command-line arguments and generate a meme.
    
    Command-line arguments:
        --path: Path to an image file (optional).
        --body: Quote body to add to the image (optional).
        --author: Quote author to add to the image (optional).
    
    If no arguments are provided, random image and quote will be used.
    """
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
