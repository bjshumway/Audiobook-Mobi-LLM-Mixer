import os
import sys
import json
import subprocess
from flask import Flask, jsonify, request, send_from_directory, abort
from flask_cors import CORS

# Add the project root to sys.path to allow importing top-level modules like 'config'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import configuration
import config

app = Flask(__name__, static_folder=config.WEB_DIR)
CORS(app)  # Enable CORS for all routes

# --- Helper Functions ---

def get_book_path(book_id: str) -> str:
    """Returns the absolute path to a book's directory."""
    return os.path.join(config.BOOKS_DIR, book_id)

def get_book_json_path(book_id: str) -> str:
    """Returns the absolute path to a book's processed JSON file."""
    return os.path.join(get_book_path(book_id), f"{book_id}.json")

def get_mobi_path(book_id: str) -> str:
    """Returns the absolute path to a book's MOBI file."""
    # This assumes MOBI file has the same name as the book_id
    return os.path.join(get_book_path(book_id), f"{book_id}.mobi")

def get_mp3_path(book_id: str) -> str:
    """Returns the absolute path to a book's MP3 file."""
    # This assumes MP3 file has the same name as the book_id
    return os.path.join(get_book_path(book_id), f"{book_id}.mp3")

def get_book_title_and_author(mobi_path: str) -> tuple[str, str]:
    """
    Placeholder function to extract title/author from MOBI.
    Will be replaced by a proper parser from mobi_parser.py later.
    """
    # For now, just guess from filename or return Unknown
    book_id = os.path.basename(os.path.dirname(mobi_path))
    # In a real scenario, mobi_parser.py would be used here
    # For example: from scripts.mobi_parser import get_mobi_metadata
    # metadata = get_mobi_metadata(mobi_path)
    # return metadata.get('title', book_id), metadata.get('author', 'Unknown')
    return book_id.replace('_', ' ').title(), 'Unknown'

# --- Static File Serving ---

@app.route('/')
def serve_index():
    """Serves the main index.html page."""
    return send_from_directory(config.WEB_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serves other static files (CSS, JS) from the web directory."""
    return send_from_directory(config.WEB_DIR, filename)

# --- API Endpoints ---

@app.route('/api/books', methods=['GET'])
def list_books():
    """Lists all available book directories and their processing status."""
    books = []
    if not os.path.exists(config.BOOKS_DIR):
        return jsonify(books)

    for book_id in os.listdir(config.BOOKS_DIR):
        book_dir = get_book_path(book_id)
        if os.path.isdir(book_dir):
            book_json_path = get_book_json_path(book_id)
            processed = os.path.exists(book_json_path)
            title, author = 'Unknown', 'Unknown'

            if processed:
                try:
                    with open(book_json_path, 'r', encoding='utf-8') as f:
                        book_data = json.load(f)
                        title = book_data.get('metadata', {}).get('title', book_id.replace('_', ' ').title())
                        author = book_data.get('metadata', {}).get('author', 'Unknown')
                except json.JSONDecodeError:
                    app.logger.warning(f"Corrupt JSON for book {book_id}: {book_json_path}")
                    processed = False # Mark as unprocessed if JSON is corrupt

            books.append({
                "id": book_id,
                "title": title,
                "processed": processed,
                "author": author
            })
    return jsonify(books)

@app.route('/api/books/<book_id>', methods=['GET'])
def get_book_data(book_id):
    """Retrieves the full processed JSON data for a specific book."""
    book_json_path = get_book_json_path(book_id)
    if not os.path.exists(book_json_path):
        abort(404, description=f"Book data not found for ID: {book_id}")
    try:
        with open(book_json_path, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    except json.JSONDecodeError:
        abort(500, description=f"Error reading JSON for book ID: {book_id}")

@app.route('/api/books/<book_id>/progress', methods=['POST'])
def update_book_progress(book_id):
    """Updates the user's reading/listening progress for a given book."""
    progress_data = request.json
    book_json_path = get_book_json_path(book_id)
    if not os.path.exists(book_json_path):
        abort(404, description=f"Book data not found for ID: {book_id}")

    try:
        with open(book_json_path, 'r+', encoding='utf-8') as f:
            book_data = json.load(f)
            book_data['progress'] = progress_data
            f.seek(0) # Rewind to start of file
            json.dump(book_data, f, indent=2, ensure_ascii=False)
            f.truncate() # Remove remaining part if new data is shorter
        return jsonify({"status": "success", "message": "Progress updated"})
    except (json.JSONDecodeError, IOError) as e:
        app.logger.error(f"Error updating progress for book {book_id}: {e}")
        abort(500, description=f"Error updating progress: {e}")

@app.route('/api/books/<book_id>/process', methods=['POST'])
def process_book_trigger(book_id):
    """Triggers the backend processing pipeline for the specified book."""
    script_path = os.path.join(config.SCRIPTS_DIR, 'process_book.py')
    if not os.path.exists(script_path):
        abort(500, description="Processing script not found.")
    
    # Run the script as a separate process. Popen is non-blocking.
    # For a personal tool, logging stdout/stderr to files is recommended for debugging.
    try:
        subprocess.Popen(['python', script_path, book_id],
                         stdout=subprocess.DEVNULL, # or open('process_log.txt', 'a')
                         stderr=subprocess.DEVNULL) # or open('error_log.txt', 'a')
        return jsonify({"status": "processing_started", "message": f"Processing of book '{book_id}' initiated."})
    except Exception as e:
        app.logger.error(f"Failed to start processing for book {book_id}: {e}")
        abort(500, description=f"Failed to initiate processing: {e}")

@app.route('/api/books/<book_id>/export-llm', methods=['POST'])
def export_llm_text(book_id):
    """Exports a selected range of text from the book into a plain text file."""
    selection_data = request.json
    start_id = selection_data.get('start_paragraph_id')
    end_id = selection_data.get('end_paragraph_id')
    
    # Placeholder: In a real implementation, you'd load book_id.json,
    # extract paragraphs based on start_id and end_id,
    # then write them to a new TXT file in the book's directory.
    # For now, we'll just acknowledge the request.
    export_file_path = os.path.join(get_book_path(book_id), f"{book_id}_export.txt")
    with open(export_file_path, 'w', encoding='utf-8') as f:
        f.write(f"Exported text for LLM from {book_id} (paragraphs {start_id} to {end_id}).\n")
        f.write("Actual content extraction from JSON to be implemented.\n")

    return jsonify({
        "status": "success",
        "message": f"Text exported for book {book_id}.",
        "file_path": f"/books/{book_id}/{book_id}_export.txt" # Frontend-accessible path
    })

# --- Serving Book-Specific Files (MOBI, MP3) ---

@app.route('/books/<book_id>/<filename>', methods=['GET'])
def serve_book_files(book_id, filename):
    """Serves MOBI, MP3, or processed JSON files directly from book directories."""
    book_dir = get_book_path(book_id)
    if not os.path.exists(book_dir):
        abort(404, description="Book directory not found.")
    return send_from_directory(book_dir, filename)

# --- Server Initialization ---

if __name__ == '__main__':
    # Ensure the books directory exists
    os.makedirs(config.BOOKS_DIR, exist_ok=True)
    print(f"Serving files from: {config.WEB_DIR}")
    print(f"Books directory: {config.BOOKS_DIR}")
    print(f"Scripts directory: {config.SCRIPTS_DIR}")
    # Run on a specific host/port to be accessible from other devices on the local network
    # For debugging purposes, you might want app.run(debug=True)
    # host='0.0.0.0' makes it accessible externally. Change to '127.0.0.1' for local-only.
    app.run(host='0.0.0.0', port=5000, debug=False)

# Base directory for the entire project
# Assumes config.py is at the project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directories relative to BASE_DIR
BOOKS_DIR = os.path.join(BASE_DIR, 'books')
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts')
WEB_DIR = os.path.join(BASE_DIR, 'web') # This is where server.py and static files are