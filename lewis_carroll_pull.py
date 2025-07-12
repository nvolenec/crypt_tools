import requests
from collections import Counter
import json
import re

# URLs of Lewis Carroll's main works on Project Gutenberg
works_urls = {
    "Alice's Adventures in Wonderland": "https://www.gutenberg.org/files/11/11-0.txt",
    "Through the Looking-Glass": "https://www.gutenberg.org/files/12/12-0.txt",
    "The Hunting of the Snark": "https://www.gutenberg.org/files/13/13-0.txt",
    "Sylvie and Bruno": "https://www.gutenberg.org/cache/epub/620/pg620.txt",
    "Sylvie and Bruno Concluded": "https://www.gutenberg.org/ebooks/48795.txt.utf-8"

}

def download_text(url):
    print(f"Downloading from {url} ...")
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def clean_gutenberg_text(text):
    # Remove Project Gutenberg's header and footer
    start_marker = "*** START OF THIS PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THIS PROJECT GUTENBERG EBOOK"
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        text = text[start_idx + len(start_marker):end_idx]
    # Strip extra whitespace
    return text.strip()

def tokenize(text):
    # Convert to lowercase and split on non-word characters (keeps only words)
    # This excludes punctuation and splits on spaces, newlines, etc.
    words = re.findall(r"\b\w+\b", text.lower())
    return words

def build_frequency_dictionary(words):
    return dict(Counter(words))

def main():
    combined_text = ""

    # Download and combine all texts
    for title, url in works_urls.items():
        raw_text = download_text(url)
        cleaned_text = clean_gutenberg_text(raw_text)
        with open( title.replace(' ', '_')+'.txt', 'w') as f:
            f.write( cleaned_text )
        combined_text += cleaned_text + "\n\n"

    # Tokenize combined text
    words = tokenize(combined_text)

    # Build frequency dictionary
    freq_dict = build_frequency_dictionary(words)

    # Save dictionary to JSON file
    with open("lewis_carroll_word_frequency.json", "w", encoding="utf-8") as outfile:
        json.dump(freq_dict, outfile, indent=4, ensure_ascii=False)

    print(f"Total unique words: {len(freq_dict)}")
    print("Word frequency dictionary saved to lewis_carroll_word_frequency.json")

if __name__ == "__main__":
    main()
