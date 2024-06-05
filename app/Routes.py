import os
import random
import tempfile
from flask import Flask, render_template, request, abort, url_for
import requests
from util.Utils import Utils
from services.ingestor_generator.QuoteEngine import Ingestor
from services.meme_generator.models.MemeEngine import ImageCaptioner

class MemeApp:
    """A Flask application for generating memes."""

    def __init__(self):
        """Initialize the Flask app, set up routes, and load quotes and images."""
        try:
            self.app = Flask(__name__)
            # Get the path to the 'tmp' directory within the calling script's directory
            static_folder = Utils.get_calling_child_script_directory('static')
            self.meme = ImageCaptioner(static_folder)
            self.quotes, self.imgs = self.setup()
            self.setup_routes()
        except Exception as e:
            print(f"Error during initialization: {e}")

    def setup(self):
        """Retrieve quotes and images for the meme generator.

        Returns:
            tuple: A tuple containing lists of quotes and image file paths.
        """
        try:
            quotes_dir = Utils.retrieve_file_dir('quotes')
            quote_files = Utils.retrieve_file_paths(quotes_dir, ('.csv', '.docx', '.pdf', '.txt'))

            quotes = []
            for file in quote_files:
                quotes.extend(Ingestor.parse(file))

            images_path = Utils.retrieve_file_dir('images')
            imgs = Utils.retrieve_file_paths(images_path, ('.jpg',))

            return quotes, imgs
        except Exception as e:
            print(f"Error during setup: {e}")
            return [], []

    def setup_routes(self):
        """Define the routes for the Flask app."""
        @self.app.route('/')
        def meme_rand():
            """Generate a random meme and render it."""
            try:
                if not self.quotes or not self.imgs:
                    abort(404, description="No quotes or images found.")
                
                img = random.choice(self.imgs)
                quote = random.choice(self.quotes)
                path = self.meme.make_meme(img, quote.body, quote.author)
                relative_path = os.path.relpath(path, self.app.static_folder)
                return render_template('meme.html', path=url_for('static', filename=relative_path))
            except Exception as e:
                abort(500, description=f"Error generating random meme: {e}")

        @self.app.route('/create', methods=['GET'])
        def meme_form():
            """Render the form for creating a custom meme."""
            try:
                return render_template('meme_form.html')
            except Exception as e:
                abort(500, description=f"Error rendering meme form: {e}")

        @self.app.route('/create', methods=['POST'])
        def meme_post():
            image_url = request.form['image_url']
            body = request.form['body']
            author = request.form['author']
            if not image_url or not body or not author:
                abort(400, description="Image URL, body, and author are required.")
            tmp_file_path = os.path.join(tempfile.gettempdir(), next(tempfile._get_candidate_names()) + '.jpg')
            try:
                response = requests.get(image_url)
                if response.status_code != 200:
                    abort(400, description="Could not retrieve image from URL.")
                with open(tmp_file_path, 'wb') as tmp_file:
                    tmp_file.write(response.content)
                path = self.meme.make_meme(tmp_file_path, body, author)
                relative_path = os.path.relpath(path, self.app.static_folder)
                return render_template('meme.html', path=url_for('static', filename=relative_path))
            except requests.RequestException as re:
                abort(400, description=f"Request error: {re}")
            except Exception as e:
                abort(500, description="Internal error during meme creation.")
            finally:
                if os.path.exists(tmp_file_path):
                    os.remove(tmp_file_path)

           

    def run(self, host='0.0.0.0', port=5000):
        """Run the Flask app."""
        try:
            self.app.run(host=host, port=port)
        except Exception as e:
            print(f"Error running the application: {e}")

