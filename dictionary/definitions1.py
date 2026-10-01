from dotenv import load_dotenv
load_dotenv()
import requests
import random
import os, csv, shutil
import xml.etree.ElementTree as ET
from collections import defaultdict

# Add your Merriam-Webster API key here
MW_API_KEY = os.environ["MW_API_KEY"]
used_words = set()

def get_mw_definition(word):
    # print("Merriam-Webster")
    """Check Merriam-Webster API for word definitions"""
    try:
        url = f"https://www.dictionaryapi.com/api/v1/references/collegiate/xml/{word}?key={MW_API_KEY}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        if root.find('entry') is None:
            return "NOT_FOUND"
            
        # Parse MW XML response
        output = f"[ ] {word}\n"
        for entry in root.findall('entry'):
            part_of_speech = entry.findtext('fl', 'unknown').lower()
            definitions = []
            for dt in entry.findall('.//def//dt'):
                definition = dt.text.strip(": ") if dt.text else ""
                if definition:
                    definitions.append(definition)
            
            if definitions:
                output += f"[{part_of_speech}]\n"
                for i, defn in enumerate(definitions[:3], 1):
                    output += f"{i}. {defn}\n"
                output += "\n"
        
        return output.strip() if output.count('\n') > 1 else "NOT_FOUND"

    except Exception as e:
        print(f"Merriam-Webster error for {word}: {str(e)[:100]}")
        return "ERROR"

def getDefinition(word, words):
    print(f"Checking: {word}")
    
    # First try Merriam-Webster
    mw_result = get_mw_definition(word)
    if mw_result != "NOT_FOUND" and mw_result != "ERROR":
        return mw_result
    
    # If word not found in Merriam-Webster, try dictionaryapi.dev
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data:
            new_word = getNewWord(word, words)
            if new_word:
                words = update_csv_file(words, word, new_word)  # Update the words list
                return getDefinition(new_word, words)
            return "NOT_FOUND"

        output = f"[ ] {word}\n"
        grouped_definitions = defaultdict(list)
        for item in data:
            for meaning in item.get('meanings', []):
                part_of_speech = meaning.get('partOfSpeech', 'unknown').lower()
                definitions = [d['definition'] for d in meaning.get('definitions', [])[:3]]
                grouped_definitions[part_of_speech].extend(definitions)

        if not grouped_definitions:
            new_word = getNewWord(word, words)
            if new_word:
                return getDefinition(new_word, words)
            return "NOT_FOUND"

        for pos, definitions in grouped_definitions.items():
            output += f"[{pos}]\n"
            for i, definition in enumerate(definitions[:3], 1):
                output += f"{i}. {definition}\n"
            output += "\n"

        return output.strip()

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error for {word}: Word not found in Dictionary")
        new_word = getNewWord(word, words)
        if new_word:
            return getDefinition(new_word, words)
        return "ERROR"
    except Exception as e:
        print(f"General error for {word}: {str(e)[:100]}")
        new_word = getNewWord(word, words)
        if new_word:
            return getDefinition(new_word, words)
        return "ERROR"

def getNewWord(word, words):
    word_len = len(word)
    print(f"Looking for a new word of length {word_len}...")

    try:
        # Read all words from random_words.txt if not already loaded
        if not hasattr(getNewWord, 'random_words'):
            with open("random_words.txt", "r") as f:
                getNewWord.random_words = [line.strip() for line in f if line.strip()]

        # Filter words that match the length, are not in the list `words`, and haven't been used
        valid_words = [w for w in getNewWord.random_words 
                       if len(w) == word_len and w not in words and w not in used_words]

        if valid_words:
            new_word = random.choice(valid_words)
            used_words.add(new_word)  # Mark the word as used
            print(f"Found new word: {new_word}")
            return new_word
        else:
            print("No valid word found.")
            return None

    except FileNotFoundError:
        print("random_words.txt file not found.")
        return None
    except Exception as e:
        print(f"Error occurred while getting new word: {str(e)}")
        return None
    
def update_csv_file(words, word_to_replace, new_word):
    """Update the words list with a replacement word and save it as a new CSV file"""
    # Replace the word in the words list
    updated_words = [new_word if word == word_to_replace else word for word in words]

    # Create the finished_puzzles directory if it doesn't exist
    finished_puzzles_dir = "finished_puzzles"
    os.makedirs(finished_puzzles_dir, exist_ok=True)

    # Write updated words to a new CSV file with blank rows between sections of 15 words
    updated_file = os.path.join(finished_puzzles_dir, "updated_book.csv")
    with open(updated_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for i, word in enumerate(updated_words, 1):
            writer.writerow([word])
            if i % 15 == 0 and i < len(updated_words):
                writer.writerow([])  # Add a blank row after every 15 words, except at the end

    print(f"Updated CSV saved as {updated_file}")
    return updated_words  # Return the updated list of words

