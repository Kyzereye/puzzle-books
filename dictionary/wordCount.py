def count_words_in_ranges(txt_file):
    range_4_to_8 = 0
    range_7_to_11 = 0
    range_10_to_14 = 0
    
    # New counters for specific lengths
    specific_lengths = {i: 0 for i in range(4, 15)}

    with open(txt_file, 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip()  # Remove any leading/trailing whitespace
            word_length = len(word)
            
            # Count words in specified ranges based on their length
            if 4 <= word_length <= 8:
                range_4_to_8 += 1
            if 7 <= word_length <= 11:
                range_7_to_11 += 1
            if 10 <= word_length <= 14:
                range_10_to_14 += 1
            
            # Count words of specific lengths
            if 4 <= word_length <= 14:
                specific_lengths[word_length] += 1

    return range_4_to_8, range_7_to_11, range_10_to_14, specific_lengths

# Specify the path to your text file
txt_file_path = 'cleaned_words.txt'

# Call the function and print the results
result_4_to_8, result_7_to_11, result_10_to_14, specific_counts = count_words_in_ranges(txt_file_path)

print(f"Words with 4 to 8 characters: {result_4_to_8}")
print(f"Words with 7 to 11 characters: {result_7_to_11}")
print(f"Words with 10 to 14 characters: {result_10_to_14}")

print("\nCounts for specific word lengths:")
for length, count in specific_counts.items():
    print(f"{length} characters: {count} words")
