#!/usr/bin/env python3
"""
Add more common/basic words to the exclusion list.
Words like body parts, common objects, basic actions that are too everyday.
"""

# Common body parts, objects, actions that should be excluded
ADDITIONAL_COMMON_WORDS = [
    # Body parts
    "ankle", "arm", "back", "bone", "chest", "chin", "ear", "eye", "face", 
    "finger", "foot", "hair", "hand", "head", "heart", "knee", "leg", "mouth",
    "neck", "nose", "shoulder", "stomach", "tooth", "toe", "wrist",
    
    # Common objects
    "ball", "bed", "book", "box", "car", "chair", "door", "desk", "floor",
    "house", "key", "knife", "lamp", "light", "paper", "pen", "pencil",
    "phone", "plate", "ring", "room", "shoe", "table", "wall", "window",
    
    # Basic actions
    "run", "walk", "jump", "sit", "stand", "eat", "drink", "sleep", "wake",
    "see", "look", "hear", "feel", "touch", "smell", "taste", "know", "think",
    "say", "tell", "talk", "speak", "ask", "answer", "call", "name",
    "write", "read", "draw", "paint", "play", "sing", "dance",
    
    # Common adjectives
    "big", "small", "long", "short", "tall", "high", "low", "new", "old",
    "good", "bad", "right", "wrong", "easy", "hard", "fast", "slow",
    "hot", "cold", "warm", "cool", "dry", "wet", "clean", "dirty",
    
    # Common nouns
    "dog", "cat", "bird", "fish", "tree", "flower", "grass", "water", "fire",
    "sun", "moon", "star", "sky", "cloud", "rain", "snow", "wind",
    "day", "night", "time", "hour", "minute", "year", "month", "week",
    "man", "woman", "person", "people", "child", "boy", "girl", "baby",
    "friend", "family", "father", "mother", "parent", "son", "daughter",
    
    # Common places
    "school", "home", "store", "park", "street", "road", "city", "town",
    "country", "world", "place", "way", "side", "top", "bottom", "front", "back",
    
    # Numbers (basic)
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
]

def main():
    """Add additional common words to the exclusion list."""
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / "data"
    common_words_file = data_dir / "common_words_top2000.txt"
    extended_common_words_file = data_dir / "common_words_extended.txt"
    
    # Read existing common words
    with open(common_words_file, 'r', encoding='utf-8') as f:
        existing_words = {line.strip().lower() for line in f if line.strip()}
    
    # Add additional common words
    all_common_words = existing_words | {word.lower() for word in ADDITIONAL_COMMON_WORDS}
    
    # Write extended list
    sorted_words = sorted(all_common_words)
    with open(extended_common_words_file, 'w', encoding='utf-8') as f:
        for word in sorted_words:
            f.write(word + '\n')
    
    print(f"Extended common words list:")
    print(f"  Original: {len(existing_words):,} words")
    print(f"  Added: {len(ADDITIONAL_COMMON_WORDS)} words")
    print(f"  Total: {len(all_common_words):,} words")
    print(f"Saved to: {extended_common_words_file}")
    print("\nTo use this extended list, update filter_words.py to use:")
    print(f"  COMMON_WORDS_FILE = DATA_DIR / 'common_words_extended.txt'")

if __name__ == "__main__":
    from pathlib import Path
    main()

