# Udacity-capstone-python, Meme Generator
A multimedia application to dynamically generate memes by overlaying quotes on images.

## Project Overview
The Meme Generator project is designed to create a multimedia application that dynamically generates memes by overlaying quotes on images. The application showcases advanced Python skills by loading quotes from various file types, including PDFs, Word Documents, CSVs, and text files, and allowing image manipulation and saving. It features both a command-line tool and a web service for dynamic user input, simulating real-world data engineering and full-stack development tasks. The project emphasizes object-oriented programming, DRY principles, and the use of Python modules and packages, while adhering to PEP 8 standards for coding best practices and documentation.

## Installation
Follow these steps to set up the project on your local machine:

### Clone the repository:
    Open your terminal and run:
    git clone https://github.com/josefdeutsch/udacity-capstone-python.git
    cd ./udacity-capstone-python.git

### Create and activate a virtual environment (optional but recommended):
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

### Install the dependencies:
    pip install -r requirements.txt


## Usage
The CLI allows you to generate memes by specifying an image path, a quote body, and an author. If no image path or quote is provided, random selections are made. The Flask application provides a web interface to generate memes. It offers routes for displaying random memes and creating custom memes through a form. 

### Command-Line Interface (CLI)
    python3 cli.py --path <path_to_image> --body <quote_body> --author <quote_author>

### Flask application (APP)
    python3 app.py

## Contributing:
To contribute to the project, fork the repository, create a new branch for your updates, make and test your changes, submit a pull request, and await code review feedback from the maintainers.
## License
This project is under the MIT License - details in the LICENSE file. It permits various uses, including commercial, as long as the original creators are credited.
