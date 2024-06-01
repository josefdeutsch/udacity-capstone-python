import os
import random
import tempfile
from flask import Flask, render_template, request, abort
import requests
from util.Utils import Utils
from services.ingestor_generator.QuoteEngine import Ingestor
from services.meme_generator.models.MemeEngine import ImageCaptioner

app = Flask(__name__)

# Initialize the ImageCaptioner with the path to the static directory
meme = ImageCaptioner(os.path.join('static'))


def setup():
    """
    Load all resources required for the meme generator.

    This function retrieves all quote files from the 'quotes' directory and all
    image files from the 'images' directory. It parses the quotes and returns
    a list of quotes and a list of image file paths.

    Returns:
        tuple: A tuple containing a list of quotes and a list of image file paths.
    """
    quotes_dir = Utils.retrieve_file_dir('quotes')

    # Retrieve all quote files in the quotes directory
    quote_files = Utils.retrieve_file_paths(quotes_dir, ('.csv', '.docx', '.pdf', 'txt'))
    print(quote_files)

    quotes = []
    for file in quote_files:
        quotes.extend(Ingestor.parse(file))

    images_path = Utils.retrieve_file_dir('images')

    # Retrieve all image files in the images directory
    imgs = Utils.retrieve_file_paths(images_path, ('.jpg'))
    print(imgs)

    return quotes, imgs


# Load quotes and images
quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """
    Generate a random meme.

    This function selects a random image and a random quote, then generates a meme
    using these selections. The generated meme is displayed on the main page.

    Returns:
        str: The rendered HTML template for the meme page.
    """
    if not quotes or not imgs:
        abort(404, description="No quotes or images found.")

    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """
    Render the meme creation form.

    This function displays a form for the user to input details for creating a meme.

    Returns:
        str: The rendered HTML template for the meme form page.
    """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """
    Create a user-defined meme.

    This function handles POST requests to create a meme based on user input.
    It downloads an image from a given URL, generates a meme with provided text,
    and removes the temporary image file.

    Returns:
        str: The rendered HTML template for the meme page.
    """
    image_url = request.form['image_url']
    body = request.form['body']
    author = request.form['author']

    if not image_url or not body or not author:
        abort(400, description="Image URL, body, and author are required.")

    # Create a temporary file in the /tmp directory
    tmp_dir = '/tmp'
    tmp_file_path = os.path.join(tmp_dir, next(tempfile._get_candidate_names()) + '.jpg')

    try:
        # Download the image and save it to the temporary file
        response = requests.get(image_url)
        if response.status_code != 200:
            abort(400, description="Could not retrieve image from URL.")

        with open(tmp_file_path, 'wb') as tmp_file:
            tmp_file.write(response.content)

        # Generate a meme using the temporary image file
        path = meme.make_meme(tmp_file_path, body, author)
    except Exception as e:
        abort(500, description=str(e))
    finally:
        # Remove the temporary file
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)

    return render_template('meme.html', path=path)


def main():
    """
    Run the Flask application.

    This function runs the Flask application, making the meme generator available.
    """
    app.run()


if __name__ == "__main__":
    main()
