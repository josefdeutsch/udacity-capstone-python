"""
This module contains the MemeEngine class which is responsible for generating memes.
It allows the user to specify an image, text, and author, and saves the generated meme to the specified output directory.

Classes:
    MemeEngine: A class to create memes with a given image, text, and author.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import random
from util.Utils import Utils
from PIL import Image

class ImageCaptioner:

    """
    A class to create memes with a given image, text, and author.
    
    Attributes:
        output_dir (str): The directory where the generated memes will be saved.
    """

    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def make_meme(self, img_path, text, author, width=500) -> str:

        """
        Creates a meme by adding text and author to an image.

        Args:
        img_path (str): The file path to the input image.
        text (str): The text to be added to the image.
        author (str): The author of the text.
        width (int): The desired width of the output image. Defaults to 500.

         Returns:
        str: The file path to the created meme image.
        """

        # Get the default image path
        default_path = Utils.retrieve_file_path('default', 'default.jpg')

        # Validate if the provided image path exists, otherwise use the default image
        img_path = Utils.validate_image_path(img_path, default_path)

        # Resolve hidden files by checking if the image path is hidden
        img_path = Utils.resolve_image_path(img_path, default_path)

        # Get the font file path
        font_path = Utils.retrieve_file_path('fonts', 'OpenSans-Regular.ttf')

        # Load the font from the font file
        font = Utils.load_font(font_path)

        # Combine text and author 
        full_text = f"{text} - {author}"

        try:

            # Open the image using the provided or default image path
            with Image.open(img_path) as img:

                # Calculate the aspect ratio and resize the image to the specified width    
                ratio = width / float(img.size[0])
                height = int(ratio * img.size[1])
                img = img.resize((width, height), Image.Resampling.LANCZOS)

                # Adjust the font size to fit the text within the image height
                font = Utils.calculate_font_size(font, full_text, height)

                # Create a drawing context
                draw = ImageDraw.Draw(img)

                # Split the text into multiple lines to fit within the image width
                split_text = Utils.split_text_into_lines(draw, full_text, font, width)

                # Insert a line break at " - " to separate the body of the text from the author
                result_text = Utils.format_text_with_line_breaks(split_text)

                # Calculate the bounding box of the text to determine its size
                text_bbox = draw.textbbox((0, 0), split_text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                # Randomly position the text within the image boundaries
                text_x = random.randint(0, max(0, width - text_width))
                text_y = random.randint(0, max(0, height - text_height))

                # Draw the text onto the image with white color
                draw.text((text_x, text_y), result_text, font=font, fill="white")

                # Save the created meme to the output directory with a random filename
                out_path = os.path.join(self.output_dir, f"meme_{random.randint(0, 1000000)}.jpg")
                img.save(out_path)
                return out_path
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""