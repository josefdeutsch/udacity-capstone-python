from PIL import Image, ImageDraw, ImageFont
import os
import random

class MemeEngine:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def make_meme(self, img_path, text, author, width=500) -> str:
        try:
            with Image.open(img_path) as img:
                ratio = width / float(img.size[0])
                height = int(ratio * img.size[1])
                img = img.resize((width, height), Image.Resampling.LANCZOS)

                draw = ImageDraw.Draw(img)
                # Navigate up two levels from the script location
               
                # Load environment variables from .env file
            

            # Get the relative path from the environment variable
            font_rel_dir = os.getenv('FONT_DIR')
            # Get the environment variable
            font = os.getenv('FONT')
            
            if not font_rel_dir:
                print("FONT_PATH not set in .env file, using default font.")
                font = ImageFont.load_default()  # Load default font early if path is not set
            else:
                # Assuming the script is run from a directory that requires navigating up to the project root
                current_dir = os.path.dirname(os.path.realpath(__file__))
                project_root = os.path.join(current_dir, '..', '..', '..')  # Adjust based on your project's structure
                font_path = os.path.join(project_root, font_rel_dir, font)
            
                # Check if the font file exists, else use default font
                if os.path.exists(font_path):
                    font_size = int(height * 0.05)
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    print("Specified font not found, using default font")
                    font = ImageFont.load_default()

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






