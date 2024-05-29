"""
This module contains the MemeEngine class which is responsible for generating memes.
It allows the user to specify an image, text, and author, and saves the generated meme to the specified output directory.

Classes:
    MemeEngine: A class to create memes with a given image, text, and author.
"""

from PIL import Image, ImageDraw
import os
import random
from util.Utils import Utils

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

        # Default image path
        default_path = Utils.retrieve_file_path('default', 'default.jpg')

        # Font path
        font_path = Utils.retrieve_file_path('fonts','OpenSans-Regular.ttf')

        # Check if the img file exists, else use default img
        img_path = Utils.get_valid_path(img_path, default_path)

           # Validate the image file
        if not Utils.check_against_hidden_files(img_path):
            print(f"Invalid or hidden image file detected and skipped: {img_path}")
            img_path = default_path
        
        try:
            with Image.open(img_path) as img:
                ratio = width / float(img.size[0])
                height = int(ratio * img.size[1])
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                # Check if the font file exists, else use default font
    
                # Load the font
                font = Utils.load_font(font_path)

                # Get the custom font with appropriate size
                font = Utils.calculate_font_size(font, font_path, height)
            
                draw = ImageDraw.Draw(img)
               
            
                # Calculate text size using the bounding box
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                text_x = random.randint(0, width - text_width)
                text_y = random.randint(0, height - text_height)
                draw.text((text_x, text_y), text, font=font, fill="white")

                author_bbox = draw.textbbox((0, 0), f"- {author}", font=font)
                author_width = author_bbox[2] - author_bbox[0]
                author_height = author_bbox[3] - author_bbox[1]

                author_x = random.randint(0, width - author_width)
                author_y = random.randint(0, height - author_height)
                draw.text((author_x, author_y), f"- {author}", font=font, fill="white")
                
                out_path = os.path.join(self.output_dir, f"meme_{random.randint(0, 1000000)}.jpg")
                img.save(out_path)
                return out_path
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""





