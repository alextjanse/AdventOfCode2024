file = open('data/day4.txt').read().splitlines()

# Get the width and height of the grid
height = len(file)
width = len(file[0])

search_word = 'XMAS'
search_length = len(search_word)

appearances = 0

# Loop over all coordinates
for x in range(0, width):
    for y in range(0, height):
        # If the value at (x,y) is the first letter, start looking for the search word
        if file[y][x] == search_word[0]:
            # Loop over all search directions (u, v). Note that (0, 0) is also a search vector,
            # but this always fail because (x, y) is the first letter of the search word.
            for u in range(-1, 2):
                for v in range(-1, 2):
                    # Check if final coordinate in the search direction is in bounds
                    x_end = x + (search_length - 1) * u
                    y_end = y + (search_length - 1) * v

                    if 0 <= x_end and x_end < width and 0 <= y_end and y_end < height:
                         # Check if the letters in the direction all correspond to the search word
                         if all([file[y + i * v][x + i * u] == c for i, c in enumerate(search_word)]):
                            appearances = appearances + 1

print(appearances)

# Alter the search word
search_word = 'MAS'
# Add the reversed word, to easily match it as well
search_words = [search_word, ''.join(reversed(search_word))]

appearances = 0

# Loop over all (x, y) that are one off the edge of the grid
for x in range(1, width - 1):
    for y in range(1, height - 1):
        # Create the diagonals with (x, y) in the center
        diag1 = file[y - 1][x - 1] + file[y][x] + file[y + 1][x + 1]
        diag2 = file[y + 1][x - 1] + file[y][x] + file[y - 1][x + 1]
        
        # Check if the diagonals are the search word
        if diag1 in search_words and diag2 in search_words:
            appearances = appearances + 1

print(appearances)
