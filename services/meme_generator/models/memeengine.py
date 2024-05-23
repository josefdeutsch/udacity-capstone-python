from PIL import Image, ImageDraw, ImageFont
import os
import random

from util.Util import retrieve_file_path, get_valid_path ,load_font, check_against_hidden_files

class MemeEngine:


    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def make_meme(self, img_path, text, author, width=500) -> str:

        # Default image path
        default_path = retrieve_file_path('default', 'default.jpg')

        # Check if the img file exists, else use default img
        img_path = get_valid_path(img_path, default_path)

           # Validate the image file
        if not check_against_hidden_files(img_path):
            print(f"Invalid or hidden image file detected and skipped: {img_path}")
            img_path = default_path
        
        try:
            with Image.open(img_path) as img:
                ratio = width / float(img.size[0])
                height = int(ratio * img.size[1])
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                # Check if the font file exists, else use default font
                font = load_font(retrieve_file_path('fonts','OpenSans-Regular.ttf'),height)
            
                draw = ImageDraw.Draw(img)
                # Navigate up two levels from the script location
            
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






