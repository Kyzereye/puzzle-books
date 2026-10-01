import requests
import time

def get_random_word():
    url = "https://random-word-api.herokuapp.com/word?number=1000"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching words: {e}")
        return []

# Initialize variables
word_list = []
min_length = 4
max_length = 16
num_iterations = 1300

# Main processing loop
for i in range(num_iterations):
    original_words = get_random_word()

    if original_words:
        new_additions = 0
        for word in original_words:
            #  check length
            word_len = len(word)

            if min_length <= word_len <= max_length:
                if word not in word_list:  # Avoid duplicates
                    word_list.append(word)
                    new_additions += 1

        print(f"Iteration {i+1}: Added {new_additions} words (Total: {len(word_list)})")
    else:
        print(f"Iteration {i+1}: Failed to retrieve words")

    time.sleep(1)

# Final output
print(f"\nTotal words collected: {len(word_list)}")

# Save to text file (one word per line)
text_file = "random_words.txt"
try:
    with open(text_file, 'w', encoding='utf-8') as f:
        for word in word_list:
            f.write(word + '\n')  # Write each word followed by a newline

    print(f"Saved {len(word_list)} unique words to {text_file}")
except Exception as e:
    print(f"Text file save error: {e}")
