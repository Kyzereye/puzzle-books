# Consolidation Plan: Dictionary-Based Word Find Generator

## Goals
1. ✅ Consolidate into clean `dictionaries` folder structure
2. ✅ Use local dictionary file (NO APIs)
3. ✅ Filter for words that are NOT commonplace (house, garage, etc.) but still commonly used
4. ✅ Generate word lists for word find puzzles with definitions
5. ✅ Clean, maintainable codebase

---

## Plan Overview

### Phase 1: Local Dictionary Setup
- Use a local JSON dictionary file with words + definitions
- Filter words by frequency (exclude top 1000-2000 most common words)
- Include words with 4-16 characters (suitable for puzzles)
- Focus on "uncommon but still used" vocabulary

### Phase 2: New Folder Structure
```
dictionaries/
├── data/
│   ├── word_list.json          # Full word list with definitions
│   ├── filtered_words.json     # Filtered for puzzles
│   └── word_frequency.txt      # Common word exclusions
├── scripts/
│   ├── filter_words.py         # Filter common words
│   ├── generate_word_list.py   # Create puzzle word lists
│   └── create_books.py         # Generate puzzle books
└── output/
    ├── word_lists/             # Generated word lists
    └── puzzle_books/           # Final puzzle books
```

### Phase 3: Word Selection Criteria
- **Exclude:** Top 1000-2000 most common English words (house, car, dog, etc.)
- **Include:** Words still commonly used in literature/media (serendipity, eloquent, etc.)
- **Length:** 4-16 characters (puzzle-friendly)
- **Format:** All words lowercase, valid English words only

---

## Implementation Strategy

### Option A: Use Existing Word List + Local Dictionary
1. Take your existing `cleaned_words.txt` (174K words)
2. Filter out common words using frequency list
3. Match remaining words against local dictionary
4. Keep words that have definitions
5. Output: Curated list with definitions

### Option B: Create Fresh Curated List
1. Start with a comprehensive local dictionary (JSON)
2. Apply frequency filtering
3. Select words in target range (uncommon but used)
4. Generate word lists for puzzles

**Recommended: Option A** (you already have good word data)

---

## Local Dictionary Solution

### Source Options:
1. **Use Python `pyenchant` or similar** - Limited definitions
2. **Download open dictionary JSON** - GitHub has several
3. **Build from your existing API responses** - If you have cached definitions
4. **Use a simple word-list + generate definitions** - Manual curation

**Best Approach:** 
- Use a free dictionary JSON file (like `words_dictionary.json` + definitions)
- Or create a curated list from your existing validated words
- Store as JSON: `{word: {definition: "...", part_of_speech: "..."}}`

---

## Word Frequency Filtering

### Common Word Lists (to EXCLUDE):
- Top 1000 most common English words
- Top 2000 for stricter filtering
- Basic vocabulary: house, car, dog, cat, run, walk, etc.

### Target Words (to INCLUDE):
- Academic vocabulary
- Literary words
- Professional terminology (common but not basic)
- Words like: serendipity, eloquent, resilience, articulate, etc.

---

## Proposed Code Structure

### `dictionaries/scripts/filter_words.py`
- Loads word frequency list (common words to exclude)
- Filters cleaned_words.txt
- Matches against local dictionary
- Outputs filtered word list with definitions

### `dictionaries/scripts/generate_word_list.py`
- Organizes filtered words by difficulty (length)
- Creates word lists for puzzles
- Exports in CSV/JSON format

### `dictionaries/scripts/create_books.py`
- Generates puzzle books from word lists
- Organizes by difficulty (easy/intermediate/hard)
- Creates output files

---

## Next Steps

1. **Choose dictionary source** (local JSON file)
2. **Set up folder structure**
3. **Create frequency filter** (exclude common words)
4. **Filter existing word list**
5. **Generate puzzle word lists**
6. **Test and refine**

---

## Questions for You:

1. Do you want to use your existing `cleaned_words.txt` or start fresh?
2. Do you have any cached/collected definitions already?
3. What's your preference for word selection? More academic or more general "uncommon"?
4. How many words do you want in the final list?

