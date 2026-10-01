import os
from dotenv import load_dotenv
load_dotenv()
import requests
import xml.etree.ElementTree as ET

MW_API_KEY = os.environ["MW_API_KEY"]

def has_definition(word):
    """Check both dictionary APIs for word definitions"""
    # Check Free Dictionary API
    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    if response.status_code == 200:
        return True
    
    # Check Merriam-Webster API
    response = requests.get(
        f"https://www.dictionaryapi.com/api/v1/references/collegiate/xml/{word}?key={MW_API_KEY}"
    )
    if response.status_code == 200:
        try:
            root = ET.fromstring(response.content)
            return len(root.findall('entry')) > 0
        except ET.ParseError:
            pass
    return False

# Read words from file
with open('random_words.txt', 'r') as f:
    words = [word.strip() for word in f.readlines()]

# Check definitions and save valid words
valid_words = []
total_words = len(words)

print(f"Processing {total_words} words...")

for index, word in enumerate(words, 1):
    if has_definition(word):
        valid_words.append(word)
        print(f"Word {index}/{total_words}: '{word}' is valid. Total valid words: {len(valid_words)}")
    else:
        print(f"Word {index}/{total_words}: '{word}' is not valid. Total valid words: {len(valid_words)}")

# Save results
with open('random_words_w_defs.txt', 'w') as f:
    f.write('\n'.join(valid_words))

print(f"\nFinished processing. Found {len(valid_words)} words with valid definitions out of {total_words} total words.")
