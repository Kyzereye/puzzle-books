import random
import numpy as np

def create_word_search(words, size=15):
    # Initialize grids
    grid = np.full((size, size), ' ')
    solution = np.full((size, size), '.')
    
    # Define directions (horizontal, vertical, diagonal_down, diagonal_up)
    directions = {
        'horizontal': (0, 1),
        'vertical': (1, 0),
        'diagonal_down': (1, 1),
        'diagonal_up': (-1, 1)
    }
    
    for word in words:
        word = word.upper()
        placed = False
        attempts = 0
        
        while not placed and attempts < 100:
            # Randomly choose direction and starting position
            dir_name = random.choice(list(directions.keys()))
            dr, dc = directions[dir_name]
            row = random.randint(0, size-1)
            col = random.randint(0, size-1)
            
            # Check if word fits
            valid = True
            for i, char in enumerate(word):
                r = row + dr * i
                c = col + dc * i
                if r >= size or c >= size or r < 0 or c < 0:
                    valid = False
                    break
                if grid[r][c] not in (' ', char):
                    valid = False
                    break
            
            # Place the word if valid
            if valid:
                for i, char in enumerate(word):
                    r = row + dr * i
                    c = col + dc * i
                    grid[r][c] = char
                    solution[r][c] = char
                placed = True
            attempts += 1
    
    # Fill empty spaces with random letters
    letters = 'ABCDEFGHIJKLMNOPRSTUVWXYZ'  # Excluding Q
    for i in range(size):
        for j in range(size):
            if grid[i][j] == ' ':
                grid[i][j] = random.choice(letters)
    
    return grid, solution

def print_grid(grid, title="Word Search Puzzle"):
    print(f"\n{title}:")
    print("+" + "---" * len(grid) + "+")
    for row in grid:
        print("|" + " ".join(row) + "|")
    print("+" + "---" * len(grid) + "+")

# Sample word list (add/remove as needed)
word_list = [
    "PYTHON", "PROGRAMMING", "PUZZLE", 
    "ALGORITHM", "DEVELOPMENT", "FUNCTION",
    "VARIABLE", "STRING", "ITERATION", "LOGIC"
]

# Generate puzzle
puzzle, solution = create_word_search(word_list, size=15)

# Display results
print_grid(puzzle)
print_grid(solution, "Solution Key")

# Optional: Save to files
np.savetxt('puzzle.txt', puzzle, fmt='%s')
np.savetxt('solution.txt', solution, fmt='%s')
