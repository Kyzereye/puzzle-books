import csv
import random
import math

# Read the CSV file
with open('./lists/word_list.csv', 'r') as file:
    reader = csv.reader(file)
    words = [word.strip().upper().replace('-', '') for row in reader for word in row if word.strip()]

# Remove duplicates
words = list(dict.fromkeys(words))

# Shuffle the words
random.shuffle(words)

# Prepare the output list with a blank element every n words
n = 15
output = []
for i, word in enumerate(words, 1):
    output.append(word)
    if i % n == 0:
        output.append('')

# Calculate the number of groups and remaining words
num_groups = len(words) / n
remaining_words = len(words) % n

# Calculate the number of words needed to make a whole number of groups
words_needed = n - remaining_words

print(f"Number of words: {len(words)}")
print(f"Number of groups (every {n} words): {math.floor(num_groups)}")
print(f"Remaining words: {remaining_words}")
print(f"Words needed to make a whole number of groups: {words_needed}")

# Write the result to a new CSV file
with open('./output/processed_word_list.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for word in output:
        writer.writerow([word])
