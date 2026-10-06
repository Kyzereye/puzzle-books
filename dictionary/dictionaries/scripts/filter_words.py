#!/usr/bin/env python3
"""
Filter cleaned_words.txt to remove common words and match with definitions.
Outputs filtered word list with definitions in JSON format.
"""

import json
import os
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
OUTPUT_DIR = SCRIPT_DIR.parent / "output"

CLEANED_WORDS_FILE = Path(__file__).parent.parent.parent / "cleaned_words.txt"
COMMON_WORDS_FILE = DATA_DIR / "common_words_top2000.txt"
DICTIONARY_FILE = DATA_DIR / "dictionary.json"
OUTPUT_FILE = DATA_DIR / "filtered_words.json"

def load_common_words(filename):
    """Load common words to exclude (lowercase)."""
    with open(filename, 'r', encoding='utf-8') as f:
        return {line.strip().lower() for line in f if line.strip()}

def load_dictionary(filename):
    """Load dictionary JSON file."""
    print(f"Loading dictionary from {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        dictionary = json.load(f)
    print(f"Loaded {len(dictionary):,} words from dictionary")
    return dictionary

def load_cleaned_words(filename):
    """Load cleaned words from file."""
    print(f"Loading cleaned words from {filename}...")
    words = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip().lower()
            if word and 4 <= len(word) <= 16:  # Puzzle-friendly length
                words.append(word)
    print(f"Loaded {len(words):,} words from cleaned_words.txt")
    return words

def filter_and_match_words(cleaned_words, common_words, dictionary):
    """
    Filter out common words and match remaining words with definitions.
    Returns dict: {word: {definition: "...", part_of_speech: "..."}}
    """
    print("\nFiltering words...")
    filtered_words = {}
    
    # Remove duplicates and filter common words
    unique_words = []
    seen = set()
    for word in cleaned_words:
        if word not in seen and word not in common_words:
            unique_words.append(word)
            seen.add(word)
    
    print(f"After removing duplicates and common words: {len(unique_words):,} words")
    
    # Match with dictionary
    print("\nMatching words with definitions...")
    matched_count = 0
    for word in unique_words:
        # Try exact match
        if word in dictionary:
            definition = dictionary[word]
            # Skip very short definitions (likely just "See X")
            if definition and len(definition) > 10:
                filtered_words[word] = {
                    "definition": definition.strip(),
                    "part_of_speech": "unknown"  # Dictionary doesn't include POS
                }
                matched_count += 1
        # Try capitalized version
        elif word.capitalize() in dictionary:
            definition = dictionary[word.capitalize()]
            if definition and len(definition) > 10:
                filtered_words[word] = {
                    "definition": definition.strip(),
                    "part_of_speech": "unknown"
                }
                matched_count += 1
    
    print(f"Matched {matched_count:,} words with definitions")
    return filtered_words

def main():
    """Main function."""
    print("=" * 60)
    print("Word Filtering and Definition Matching")
    print("=" * 60)
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load data
    common_words = load_common_words(COMMON_WORDS_FILE)
    print(f"Loaded {len(common_words):,} common words to exclude")
    
    dictionary = load_dictionary(DICTIONARY_FILE)
    cleaned_words = load_cleaned_words(CLEANED_WORDS_FILE)
    
    # Filter and match
    filtered_words = filter_and_match_words(cleaned_words, common_words, dictionary)
    
    # Save results
    print(f"\nSaving {len(filtered_words):,} filtered words to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(filtered_words, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print(f"SUCCESS: Created {OUTPUT_FILE}")
    print(f"Total words with definitions: {len(filtered_words):,}")
    print("=" * 60)
    
    # Print some sample words
    print("\nSample words (first 10):")
    for i, word in enumerate(list(filtered_words.keys())[:10], 1):
        defn = filtered_words[word]["definition"][:80] + "..."
        print(f"{i}. {word}: {defn}")

if __name__ == "__main__":
    main()

