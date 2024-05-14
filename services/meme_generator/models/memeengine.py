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
                
                # Check if the font file exists, else use default font
                font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
                if os.path.exists(font_path):
                    font_size = int(height * 0.05)
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    print("Font not found, using default font")
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

# Example usage remains the same



def get_image_path(image_filename):
    # Get the directory where the current script is located
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Combine the directory path with the image filename
    return os.path.join(script_directory, image_filename)


output_directory = "/Users/Joseph/udacity-capstone-python/python-structure-template/services/meme_generator/tmp"  # specify the output directory for saved memes
meme_generator = MemeEngine(output_directory)

image_path = get_image_path("xander_1.jpg")
print("Image path:", image_path)
text = "When you realize you've debugged successfully"
author = "Anonymous"

meme_path = meme_generator.make_meme(image_path, text, author)
print(f"Meme saved at: {meme_path}")
# Usage




