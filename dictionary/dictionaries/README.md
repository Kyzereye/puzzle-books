# Dictionary-Based Word Find Generator

A consolidated word find puzzle generator that uses local dictionary files (NO APIs) to create word lists with definitions.

## Overview

This system filters word lists to remove common everyday words (like "ankle", "house", "garage") and matches remaining words with definitions from a local dictionary JSON file. It generates puzzle books with curated word lists suitable for word find puzzles.

## Structure

```
dictionaries/
├── data/                           # Data files
│   ├── dictionary.json            # Local dictionary (102K+ words with definitions)
│   ├── common_words_top2000.txt   # Top 2000 most common words to exclude
│   ├── common_words_extended.txt  # Extended exclusion list (+175 basic words)
│   └── filtered_words.json        # Final filtered words with definitions
├── scripts/                        # Processing scripts
│   ├── filter_words.py            # Filter words and match with definitions
│   ├── generate_books.py          # Generate puzzle books
│   └── add_common_basic_words.py  # Add basic words to exclusion list
└── output/
    └── word_lists/                 # Generated books
        ├── book_001.csv           # Words with definitions (CSV format)
        ├── book_001_words.txt     # Words only (one per line)
        ├── book_002.csv
        ├── book_002_words.txt
        ... (25 books total)
```

## Usage

### Step 1: Filter Words and Get Definitions

Filter your word list and match with definitions:

```bash
cd dictionaries/scripts
python3 filter_words.py
```

This will:
- Load `cleaned_words.txt` from parent directory
- Filter out common words (top 2000)
- Match remaining words with dictionary.json
- Output `filtered_words.json` (~48K words with definitions)

**Note:** To exclude more basic words (like "ankle"), update `filter_words.py` to use `common_words_extended.txt` instead.

### Step 2: Generate Puzzle Books

Generate 25 books with ~55 words each:

```bash
cd dictionaries/scripts
python3 generate_books.py
```

This will:
- Load filtered_words.json
- Organize words by difficulty (easy/intermediate/hard)
- Create 25 books with balanced difficulty distribution
- Output CSV files (with definitions) and TXT files (words only)

## Output Format

### CSV Files (`book_XXX.csv`)
Contains words and their definitions:
```csv
word,definition
krumhorn,"(a) A reed instrument of music..."
ratter,"1. One who, or that which, rats..."
```

### TXT Files (`book_XXX_words.txt`)
Contains words only, one per line:
```
krumhorn
ratter
chirographical
...
```

## Current Status

- ✅ 25 books generated
- ✅ ~55 words per book
- ✅ All words have definitions
- ✅ Words filtered to exclude common everyday words
- ✅ Mix of easy/intermediate/hard words
- ⚠️ Some basic words (like "ankle") may still appear - can refine filter

## Refining the Word Filter

To exclude more common/basic words:

1. Update `filter_words.py`:
   ```python
   COMMON_WORDS_FILE = DATA_DIR / "common_words_extended.txt"
   ```

2. Re-run `filter_words.py` to regenerate `filtered_words.json`

3. Re-run `generate_books.py` to create new books

## Data Sources

- **Dictionary:** Webster's English Dictionary (JSON format, 102K+ words)
  - Source: https://github.com/matthewreagan/WebstersEnglishDictionary
- **Common Words List:** Top 2000 most common English words
  - Source: Google 10000 English Words
- **Word List:** Your existing `cleaned_words.txt` (173K words)

## Requirements

- Python 3.10+
- Standard library only (no external packages needed)

## Statistics

- **Total words in dictionary:** 102,217
- **Words after filtering:** ~48,479 (with definitions)
- **Words used for books:** 1,375 (25 books × 55 words)
- **Words per book:** ~55
- **Difficulty distribution per book:** ~18 easy, ~22 intermediate, ~15 hard

