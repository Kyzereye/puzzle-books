from collections import defaultdict
import random
import os
import shutil
import csv
class PuzzleBookGenerator:
    def __init__(self, word_file_path):
        # Delete the directory if it exists
        if os.path.exists("word_search_books"):
            shutil.rmtree("word_search_books")
            print("Deleted existing word_search_books directory.")

        self.word_pool = self._load_and_organize_words(word_file_path)
        self.used_words = set()
        self.book_number = 0
        self.total_words_used = 0

        if not os.path.exists("word_search_books"):
            os.makedirs("word_search_books")

    def _load_and_organize_words(self, file_path):
        word_dict = defaultdict(list)
        try:
            with open(file_path, 'r') as f:
                for word in f:
                    word = word.strip().lower()
                    length = len(word)
                    if 4 <= length <= 16:
                        word_dict[length].append(word)
            print(f"Loaded {sum(len(words) for words in word_dict.values())} words.")
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return {}
        except Exception as e:
            print(f"An error occurred: {e}")
            return {}
        return word_dict

    def _get_unique_words(self, length_range, count):
        valid_words = []
        for length in length_range:
            valid_words.extend(self.word_pool[length])

        random.shuffle(valid_words)
        selected = []
        for word in valid_words:
            if word not in self.used_words and len(selected) < count:
                selected.append(word)
                self.used_words.add(word)
        return selected

    def create_book(self):
        print("create_book")
        try:
            book = {
                'easy': self._get_unique_words(range(4, 8), 225),      # 15 puzzles * 15 words - 1-7 easy, 8-15 easy+
                'intermediate': self._get_unique_words(range(7, 11), 375),  # 25 puzzles * 15 words INTERMEDIATE
                'hard': self._get_unique_words(range(10, 16), 150)     # 10 puzzles * 15 words 10 - advanced with 5 extra added hard
            }
            if all(len(words) == expected for words, expected in zip(book.values(), [225, 375, 150])):
                self.book_number += 1
                self.total_words_used += sum(len(book[d]) for d in book)
                return book
            else:
                return None
        except Exception as e:
            print(f"Error creating book: {e}")
            return None

    def save_book(self, book):
        if book is None:
            return False
        filename = f"word_search_books/book_{self.book_number:03d}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            difficulties = ['easy', 'intermediate', 'hard']
            for i, difficulty in enumerate(difficulties):
                for j in range(0, len(book[difficulty]), 15):
                    puzzle = book[difficulty][j:j+15]
                    for word in puzzle:
                        writer.writerow([word])
                    # Add blank row after each puzzle, except the last puzzle of the last difficulty
                    if not (i == len(difficulties) - 1 and j + 15 >= len(book[difficulty])):
                        writer.writerow([])
        print(f"Created {filename}")
        return True


if __name__ == "__main__":
    WORD_LIST_FILE = "cleaned_words.txt"  # Replace with your file path

    generator = PuzzleBookGenerator(WORD_LIST_FILE)

    while True:
        book = generator.create_book()
        if book:
            if not generator.save_book(book):
                print("Failed to save book. Stopping.")
                break
        else:
            print("Unable to create a complete book. Stopping.")
            break

    print(f"Total books created: {generator.book_number}")
    print(f"Total words used: {generator.total_words_used}")
