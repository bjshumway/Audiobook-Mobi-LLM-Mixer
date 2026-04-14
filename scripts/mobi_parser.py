import os
import sys
import re
import mobi
from bs4 import BeautifulSoup

# Add the project root to sys.path so we can import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

def extract_paragraphs_from_mobi(mobi_path):
    """
    Extracts text from a MOBI file and returns a list of clean paragraphs.
    """
    print(f"Unpacking MOBI file: {mobi_path}...")
    
    try:
        # The mobi library unpacks the file into a temporary directory
        # and returns the path to the main extracted HTML file.
        tempdir, filepath = mobi.extract(mobi_path)
    except Exception as e:
        print(f"Failed to extract MOBI file. Error: {e}")
        return None

    print(f"Parsing extracted HTML: {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        paragraphs = []
        
        # Find all paragraph tags <p> or div tags that act like paragraphs
        for p_tag in soup.find_all(['p', 'div']):
            # Extract text, replace HTML line breaks with spaces, and strip edge whitespace
            text = p_tag.get_text(separator=' ', strip=True)
            
            # Clean up weird spacing issues (multiple spaces, tabs, etc.)
            text = re.sub(r'\s+', ' ', text)
            
            # Only keep it if it actually contains words (filters out empty layout tags)
            if len(text) > 2:
                paragraphs.append(text)

        print(f"Successfully extracted {len(paragraphs)} paragraphs!")
        return paragraphs

    except Exception as e:
        print(f"Failed to parse HTML. Error: {e}")
        return None

if __name__ == "__main__":
    # --- Testing Block ---
    if len(sys.argv) < 2:
        print("Usage: python mobi_parser.py <path_to_mobi_file>")
        sys.exit(1)

    test_mobi = sys.argv[1]
    if not os.path.exists(test_mobi):
        print(f"File not found: {test_mobi}")
        sys.exit(1)

    print("--- Starting MOBI Test ---")
    paragraphs = extract_paragraphs_from_mobi(test_mobi)
    
    if paragraphs:
        print("\n--- Success! First 5 Paragraphs ---")
        for i, p in enumerate(paragraphs[:5]):
            print(f"\n[Paragraph {i+1}]: {p}")
            
        print(f"\n... and {len(paragraphs) - 5} more paragraphs.")
    else:
        print("\nExtraction failed or returned no text.")