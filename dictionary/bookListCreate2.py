import csv
import os
import random


def read_words_from_csv(file_name):
    """
    Reads words from a CSV file.
    
    Parameters:
        file_name (str): The name of the CSV file.
    
    Returns:
        list: A list of words read from the file.
    """
    with open(file_name, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        return [word.strip() for row in reader for word in row if word.strip()]


def categorize_words(word_list):
    """
    Categorizes words into easy, intermediate, and advanced based on their lengths.
    
    Parameters:
        word_list (list): The list of words to categorize.
    
    Returns:
        dict: A dictionary containing categorized words.
    """
    categories = {
        "easy": [],
        "intermediate": [],
        "advanced": []
    }
    
    for word in word_list:
        length = len(word)
        
        # Easy category: Majority 4-8 letters, some 9-10 letters
        if 4 <= length <= 8 or (9 <= length <= 10 and random.random() < 0.3):  # 30% chance for longer words
            categories["easy"].append(word)
        
        # Intermediate category: Majority 7-11 letters, some 5-6 and 12-13 letters
        elif (7 <= length <= 11 or (5 <= length <= 6 and random.random() < 0.3) or 
              (12 <= length <= 13 and random.random() < 0.3)):  # Add edge cases with probabilities
            categories["intermediate"].append(word)
        
        # Advanced category: Majority 10-14 letters, some 8-9 letters
        elif (10 <= length <= 14 or (8 <= length <= 9 and random.random() < 0.3)):  # Add edge cases with probabilities
            categories["advanced"].append(word)
    
    return categories


def create_puzzle(words, words_per_puzzle):
    """
    Creates a puzzle by randomly selecting words from a list.
    
    Parameters:
        words (list): The list of words to select from.
        words_per_puzzle (int): The number of words per puzzle.
    
    Returns:
        list: A list of selected words for the puzzle.
    """
    return random.sample(words, min(words_per_puzzle, len(words)))


def create_word_search_books(word_categories, puzzles_per_book=54, words_per_puzzle=20, output_folder="word_search_books"):
    """
    Creates word search books with puzzles divided into easy, intermediate, and advanced sections.
    
    Parameters:
        word_categories (dict): Categorized words (easy, intermediate, advanced).
        puzzles_per_book (int): The number of puzzles per book.
        words_per_puzzle (int): The number of words per puzzle.
        output_folder (str): The folder where the books will be saved.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    book_number = 1
    while True:
        easy_words = word_categories["easy"]
        intermediate_words = word_categories["intermediate"]
        advanced_words = word_categories["advanced"]

        # Check if we have enough words to create another book
        if len(easy_words) < words_per_puzzle * 18 or \
           len(intermediate_words) < words_per_puzzle * 18 or \
           len(advanced_words) < words_per_puzzle * 18:
            break

        book_file_name = os.path.join(output_folder, f"book_{book_number}.txt")

        with open(book_file_name, "w", encoding='utf-8') as book_file:
            # Write easy puzzles
            book_file.write("Easy Section\n\n")
            for _ in range(18):
                puzzle = create_puzzle(easy_words, words_per_puzzle)
                book_file.write("\n".join(puzzle) + "\n\n")
                for word in puzzle:
                    easy_words.remove(word)

            # Write intermediate puzzles
            book_file.write("Intermediate Section\n\n")
            for _ in range(18):
                puzzle = create_puzzle(intermediate_words, words_per_puzzle)
                book_file.write("\n".join(puzzle) + "\n\n")
                for word in puzzle:
                    intermediate_words.remove(word)

            # Write advanced puzzles
            book_file.write("Advanced Section\n\n")
            for _ in range(18):
                puzzle = create_puzzle(advanced_words, words_per_puzzle)
                book_file.write("\n".join(puzzle) + "\n\n")
                for word in puzzle:
                    advanced_words.remove(word)

        print(f"Created book {book_number}")
        book_number += 1

    print(f"Created {book_number - 1} books in the '{output_folder}' folder.")
    print(f"Words left unused: Easy: {len(easy_words)}, Intermediate: {len(intermediate_words)}, Advanced: {len(advanced_words)}")


# Read words from the CSV file
csv_file_name = 'random_words.csv'
word_list = read_words_from_csv(csv_file_name)

# Categorize words into easy, intermediate, and advanced sections
word_categories = categorize_words(word_list)

# Create word search books
create_word_search_books(word_categories)
