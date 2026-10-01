import csv

# List of input file names
input_files = [
    "random_words.csv",
    "random_words1.csv",
    "random_words2.csv",
    "random_words3.csv",
    "random_words4.csv",
]

# Output file name
output_file = "final_words.csv"

# Initialize an empty list to store all words (including duplicates)
all_words = []

# Initialize an empty set to store unique words
unique_words = set()

# Loop through each input file
for file in input_files:
    try:
        with open(file, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                # Add each word from the row to both the list and the set
                all_words.extend(row)
                unique_words.update(row)
    except FileNotFoundError:
        print(f"File {file} not found. Skipping...")
    except Exception as e:
        print(f"An error occurred while processing {file}: {e}")

# Sort the unique words alphabetically (optional)
sorted_words = sorted(unique_words)

# Print the total count of words before filtering
print(f"Total count of words before filtering: {len(all_words)}")

# Print the final count of unique words
print(f"Final count of unique words: {len(sorted_words)}")

# Write the unique words to the output file
try:
    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for word in sorted_words:
            writer.writerow([word])
    print(f"Final list of unique words saved to {output_file}")
except Exception as e:
    print(f"An error occurred while saving to {output_file}: {e}")
