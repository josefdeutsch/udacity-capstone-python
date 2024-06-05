"""
This module provides functionality to generate memes given an image path and a quote.
If no image path or quote is provided, random selections are made from available images and quotes.

Functions:
    generate_meme(path=None, body=None, author=None): Generate a meme with the specified parameters.
"""
import os
import random
from services.ingestor_generator.base.QuoteModel import QuoteModel
from services.ingestor_generator.QuoteEngine import Ingestor
from services.meme_generator.models.MemeEngine2 import ImageCaptioner

from util.Utils import Utils

def generate_meme(path=None, body=None, author=None):

    """
    Generate a meme given a path and a quote.
    
    Args:
        path (str, optional): Path to an image file. Defaults to None.
        body (str, optional): Quote body to add to the image. Defaults to None.
        author (str, optional): Quote author to add to the image. Defaults to None.
    
    Returns:
        str: Path to the generated meme image.
    
    Raises:
        Exception: If body is provided without an author.
    """

    img = None
    quote = None

    base_dir = Utils.locate_project_root(os.getcwd())
    images_dir = Utils.retrieve_file_dir('images')
    quotes_dir = Utils.retrieve_file_dir('quotes')


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
    
    # Get the path to the 'tmp' directory within the calling script's directory
    tmp_directory = Utils.get_calling_child_script_directory('tmp')
    # Generate the meme using the MemeEngine class
    meme = ImageCaptioner(tmp_directory)

    meme_path = meme.make_meme(img, quote.body, quote.author)
    return meme_path


