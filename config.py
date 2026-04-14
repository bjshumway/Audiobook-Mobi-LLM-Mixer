import os

# Import configuration

# Base directory for the entire project
# Assumes config.py is at the project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directories relative to BASE_DIR
BOOKS_DIR = os.path.join(BASE_DIR, 'books')
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts')
WEB_DIR = os.path.join(BASE_DIR, 'web') # This is where server.py and static files are
GOOGLE_APPLICATION_CREDENTIALS = os.path.join(BASE_DIR, 'mobi-mp3-llm-syncer-226538ba5cd3.json')