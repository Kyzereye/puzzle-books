#!/usr/bin/env python3
"""
Generate 25 puzzle books with ~55 words each from filtered word list.
Each book contains words with definitions suitable for word find puzzles.
"""

import json
import random
import csv
from pathlib import Path
from collections import defaultdict

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
OUTPUT_DIR = SCRIPT_DIR.parent / "output" / "word_lists"

FILTERED_WORDS_FILE = DATA_DIR / "filtered_words.json"
WORDS_PER_BOOK = 55
NUM_BOOKS = 25

def load_filtered_words(filename):
    """Load filtered words with definitions."""
    print(f"Loading filtered words from {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        words = json.load(f)
    print(f"Loaded {len(words):,} words with definitions")
    return words

def organize_by_length(words_dict):
    """Organize words by length for difficulty classification."""
    by_length = defaultdict(list)
    for word, data in words_dict.items():
        length = len(word)
        if 4 <= length <= 16:  # Puzzle-friendly length
            by_length[length].append((word, data))
    return by_length

def get_difficulty_level(length):
    """Classify word difficulty by length."""
    if 4 <= length <= 7:
        return "easy"
    elif 8 <= length <= 11:
        return "intermediate"
    else:  # 12-16
        return "hard"

def select_words_for_book(by_length, used_words, words_per_book=55):
    """
    Select words for one book, ensuring variety in difficulty.
    Target: ~20 easy, ~20 intermediate, ~15 hard
    """
    selected = []
    
    # Shuffle word lists for randomness
    easy_words = []
    intermediate_words = []
    hard_words = []
    
    for length, word_list in by_length.items():
        difficulty = get_difficulty_level(length)
        for word, data in word_list:
            if word not in used_words:
                if difficulty == "easy":
                    easy_words.append((word, data))
                elif difficulty == "intermediate":
                    intermediate_words.append((word, data))
                else:
                    hard_words.append((word, data))
    
    # Randomize
    random.shuffle(easy_words)
    random.shuffle(intermediate_words)
    random.shuffle(hard_words)
    
    # Select words (target distribution)
    easy_count = min(20, len(easy_words), words_per_book // 3)
    intermediate_count = min(20, len(intermediate_words), words_per_book // 3)
    hard_count = min(15, len(hard_words), words_per_book - easy_count - intermediate_count)
    
    # Fill remaining slots if needed
    remaining = words_per_book - easy_count - intermediate_count - hard_count
    if remaining > 0:
        # Fill with intermediate words (most versatile)
        if len(intermediate_words) > intermediate_count:
            intermediate_count += min(remaining, len(intermediate_words) - intermediate_count)
            remaining = words_per_book - easy_count - intermediate_count - hard_count
    
    if remaining > 0 and len(easy_words) > easy_count:
        easy_count += min(remaining, len(easy_words) - easy_count)
    
    # Collect selected words
    selected.extend(easy_words[:easy_count])
    selected.extend(intermediate_words[:intermediate_count])
    selected.extend(hard_words[:hard_count])
    
    # Randomize final selection
    random.shuffle(selected)
    
    return selected[:words_per_book]

def save_book(book_number, words, output_dir):
    """Save book as CSV file with words and definitions."""
    filename = output_dir / f"book_{book_number:03d}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(['word', 'definition'])
        # Write words
        for word, data in words:
            definition = data['definition']
            # Truncate very long definitions (keep first 200 chars)
            if len(definition) > 200:
                definition = definition[:197] + "..."
            writer.writerow([word, definition])
    
    return filename

def save_book_text(book_number, words, output_dir):
    """Save book as text file (just words, one per line, for puzzle generation)."""
    filename = output_dir / f"book_{book_number:03d}_words.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        for word, _ in words:
            f.write(word + '\n')
    
    return filename

def main():
    """Main function to generate books."""
    print("=" * 60)
    print("Puzzle Book Generator")
    print(f"Generating {NUM_BOOKS} books with ~{WORDS_PER_BOOK} words each")
    print("=" * 60)
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load filtered words
    words_dict = load_filtered_words(FILTERED_WORDS_FILE)
    
    # Organize by length
    by_length = organize_by_length(words_dict)
    print(f"\nWords organized by length:")
    for length in sorted(by_length.keys()):
        difficulty = get_difficulty_level(length)
        print(f"  Length {length:2d} ({difficulty:12s}): {len(by_length[length]):5,} words")
    
    # Generate books
    used_words = set()
    books_created = 0
    
    print(f"\nGenerating books...")
    for book_num in range(1, NUM_BOOKS + 1):
        # Select words for this book
        selected_words = select_words_for_book(by_length, used_words, WORDS_PER_BOOK)
        
        if len(selected_words) < WORDS_PER_BOOK:
            print(f"\nWARNING: Book {book_num:03d} only has {len(selected_words)} words "
                  f"(target: {WORDS_PER_BOOK}). Not enough words remaining.")
            break
        
        # Mark words as used
        for word, _ in selected_words:
            used_words.add(word)
        
        # Save book files
        csv_file = save_book(book_num, selected_words, OUTPUT_DIR)
        txt_file = save_book_text(book_num, selected_words, OUTPUT_DIR)
        
        # Calculate difficulty distribution
        difficulty_counts = defaultdict(int)
        for word, _ in selected_words:
            difficulty_counts[get_difficulty_level(len(word))] += 1
        
        print(f"  Book {book_num:03d}: {len(selected_words)} words "
              f"(E:{difficulty_counts['easy']} I:{difficulty_counts['intermediate']} "
              f"H:{difficulty_counts['hard']}) - {csv_file.name}")
        
        books_created += 1
    
    print("\n" + "=" * 60)
    print(f"SUCCESS: Created {books_created} books in {OUTPUT_DIR}")
    print(f"Total words used: {len(used_words):,}")
    print(f"Average words per book: {len(used_words) / books_created:.1f}")
    print("=" * 60)

if __name__ == "__main__":
    main()

