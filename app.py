"""
Main entry point for the Flask application.

This script initializes and runs the MemeApp defined in app.routes. The MemeApp is a
Flask application that generates memes using quotes and images. It provides routes
for displaying random memes, as well as for creating custom memes through a form.

Modules:
    MemeApp (from app.Routes): The main application class for the meme generator.
"""

from app.Rooutes import MemeApp

def main():
    """Main function to initialize and run the MemeApp."""
    try:
        meme_app = MemeApp()
        meme_app.run()
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()


    