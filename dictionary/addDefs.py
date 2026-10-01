import os, csv, shutil
from concurrent.futures import ProcessPoolExecutor, as_completed
from definitions1 import getDefinition, getNewWord  # Import both functions from definitions.py

def processFile(filename):
    """Process individual book files with progress tracking"""
    try:
        input_path = os.path.join("word_search_books_test", filename)
        
        # Create finished_puzzles directory if it doesn't exist
        finished_puzzles_dir = "finished_puzzles"
        os.makedirs(finished_puzzles_dir, exist_ok=True)
        
        processed_output_path = os.path.join(finished_puzzles_dir, f"processed_{filename}")
        updated_output_path = os.path.join(finished_puzzles_dir, f"updated_{filename}")
        
        with open(input_path, 'r') as f:
            words = [line.strip() for line in f if line.strip()]
        
        definitions = []
        not_found = []
        errors = []
        updated_words = words.copy()
        
        for i, word in enumerate(words):
            definition = getDefinition(word, words)
            if definition == "NOT_FOUND":
                print(" WORD NOT FOUND")
                not_found.append(word)
                new_word = getNewWord(word, words)
                if new_word:
                    updated_words[i] = new_word
                    new_definition = getDefinition(new_word, words)
                    if new_definition not in ["NOT_FOUND", "ERROR"]:
                        definitions.append(new_definition)
                    else:
                        not_found.append(new_word)
            elif definition == "ERROR":
                errors.append(word)
            else:
                definitions.append(definition)
        
        with open(processed_output_path, 'w') as f:
            f.write('\n\n'.join(definitions))
            f.write('\n\nWords not found:\n')
            f.write('\n'.join(not_found))
            f.write('\n\nWords with errors:\n')
            f.write('\n'.join(errors))
        
        with open(updated_output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            for i, word in enumerate(updated_words, 1):
                writer.writerow([word])
                if i % 15 == 0 and i < len(updated_words):
                    writer.writerow([])  # Add a blank row after every 15 words, except at the end
        
        return f"Processed {filename}"
    except Exception as e:
        return f"Error processing {filename}: {str(e)}"

def main():
    """Main function with parallel processing"""
    # Clear out the finished_puzzles folder
    finished_puzzles_dir = "finished_puzzles"
    if os.path.exists(finished_puzzles_dir):
        shutil.rmtree(finished_puzzles_dir)
    os.makedirs(finished_puzzles_dir)

    # Create output directory if needed
    os.makedirs("word_search_books_test", exist_ok=True)

    # Get list of book files
    book_files = [f for f in os.listdir("word_search_books_test") 
                 if f.startswith("book_") and f.endswith(".csv")]

    # Create progress log
    with open("progress.log", "w") as f:
        f.write("Processing started\n")

    # Process files in parallel with progress tracking
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(processFile, fn): fn for fn in book_files}
        
        for future in as_completed(futures):
            filename = futures[future]
            try:
                result = future.result()
                with open("progress.log", "a") as log:
                    log.write(f"Completed: {filename}\n")
            except Exception as e:
                with open("progress.log", "a") as log:
                    log.write(f"Failed {filename}: {str(e)}\n")

if __name__ == "__main__":
    # Clear previous progress log if it exists
    if os.path.exists("progress.log"):
        os.remove("progress.log")

    try:
        main()
    except KeyboardInterrupt:
        print("\nFORCE EXIT: Terminating all processes...")
        os._exit(1)  # Nuclear option
