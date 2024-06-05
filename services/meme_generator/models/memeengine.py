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
        font_path_body = Utils.retrieve_file_path('fonts', 'OpenSans-Regular.ttf')

        # Load the font from the font file
        font_body = Utils.load_font(font_path_body)

        # Get the font file path
        font_path_author = Utils.retrieve_file_path('fonts', 'OpenSans-ExtraBold.ttf')

        # Load the font from the font file
        font_author = Utils.load_font(font_path_author)

        # Prefix author string
        author = Utils.prefix_string(author)

        # Remove spaces 
        author = Utils.remove_separators(author)
        
        # Combine text and author 
        full_text = f"{text}{author}"

        try:

            # Open the image using the provided or default image path
            with Image.open(img_path) as img:

                # Calculate the aspect ratio and resize the image to the specified width    
                ratio = width / float(img.size[0])
                height = int(ratio * img.size[1])
                img = img.resize((width, height), Image.LANCZOS)

                # Adjust the font size to fit the text within the image height
                font_body_result = Utils.calculate_font_size(font_body, full_text, height)
                
                # Adjust the font size to fit the text within the image height
                font_author_result = Utils.calculate_font_size(font_author, full_text, height)
                
                # Create a drawing context
                draw = ImageDraw.Draw(img)

                # Split the text into multiple lines to fit within the image width
                split_text = Utils.split_text_into_lines(draw, full_text, font_body_result, width)

                # Insert a line break at "#" to separate the body of the text from the author
                formatted_text = Utils.format_text_with_line_breaks(split_text)

                # Splits the formatted text into segments and marks whether each segment is an author
                text_segments = Utils.get_text_segments(formatted_text)





                # Step 1: Calculate the maximum text width among all segments
                max_text_width = max(
                    [
                        draw.textbbox((0, 0), segment, font=font_author_result if is_author else font_body_result)[2]
                        for segment, is_author in text_segments
                    ]
                )
                # Step 2: Calculate the total text height required for all segments including spaces between them
                total_text_height = sum(
                    [
                        draw.textbbox((0, 0), segment, font=font_author_result if is_author else font_body_result)[3] + 10
                        for segment, is_author in text_segments
                    ]
                )

                # Step 3: Randomly position the initial text within the image boundaries
                # Ensure the text fits within the width of the image
                initial_text_x = random.randint(0, max(0, width - max_text_width))
                # Ensure the text fits within the height of the image
                initial_text_y = random.randint(0, max(0, height - total_text_height))

                # Initialize the current y position
                current_y = initial_text_y

                # Step 4: Iterate through each text segment and its corresponding author status
                for segment, is_author in text_segments:
                    # If the segment is an author, add spaces between lowercase and uppercase letters
                    if is_author:
                        segment = Utils.add_spaces(segment)
                    # Step 5: Select the appropriate font based on whether the segment is an author
                    font = font_author_result if is_author else font_body_result
                    # Step 6: Calculate the bounding box of the text segment to get its width and height
                    text_bbox = draw.textbbox((0, 0), segment, font=font)
                    text_height = text_bbox[3] - text_bbox[1]

                    # Set the x position to the initial random value calculated earlier
                    text_x = initial_text_x

                    # Step 7: Check if the next segment fits within the image height
                    if current_y + text_height > height:
                        break  # Stop if the text exceeds the image height

                    # Step 8: Draw the text onto the image at the calculated x and current y positions
                    draw.text((text_x, current_y), segment, font=font, fill="white")

                    # Step 9: Increment the current y position by the height of the text segment plus some space
                    current_y += text_height + 10  # Add some space between lines

                # Save the created meme to the output directory with a random filename
                out_path = os.path.join(self.output_dir, f"meme_{random.randint(0, 1000000)}.jpg")
                img.save(out_path)
                return out_path
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""