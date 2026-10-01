import os
import random
import csv

def add_sections_to_book(filepath, num_sections=5, words_per_section=15, min_word_length=8):
    """
    Adds new sections to a book file using existing words, with each word on its own line in CSV format.

    Args:
        filepath (str): The path to the book's CSV file.
        num_sections (int): The number of new sections to add.
        words_per_section (int): The number of words to include in each new section.
        min_word_length (int): The minimum length of words to be used in the new sections.
    """
    try:
        # Read existing content from the CSV file
        all_words = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:  # Skip empty rows
                    all_words.extend(row)

        # Filter words based on minimum length
        long_words = [word.strip() for word in all_words if len(word.strip()) >= min_word_length]

        if not long_words:
            print(f"Not enough words of length {min_word_length} or more in {filepath} to create new sections.")
            return

        # Add new sections
        with open(filepath, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for i in range(num_sections):
                new_section = random.sample(long_words, words_per_section)
                print(f"Adding section {i + 1} of {num_sections}")
                writer.writerow([])  # Add an empty row to separate sections
                for word in new_section:
                    writer.writerow([word])  # Write each word on its own line

        print(f"Successfully added {num_sections} sections to {filepath}")

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except Exception as e:
        print(f"An error occurred while processing {filepath}: {e}")

def main(directory="word_search_books"):
    """
    Processes all CSV files in a directory to add new sections.

    Args:
        directory (str): The directory containing the book files. Defaults to "word_search_books".
    """
    if not os.path.exists(directory):
        print(f"Error: Directory not found: {directory}")
        return

    for filename in os.listdir(directory):
        if filename.startswith("book_") and filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            add_sections_to_book(filepath)

if __name__ == "__main__":
    main()
