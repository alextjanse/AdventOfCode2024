file = open('data/day4.txt').read().splitlines()

height = len(file)
width = len(file[0])

search_word = 'XMAS'
search_length = len(search_word)

appearances = 0

for x in range(0, width):
    for y in range(0, height):
        if file[y][x] == search_word[0]:
            for u in range(-1, 2):
                for v in range(-1, 2):
                    x_end = x + (search_length - 1) * u
                    y_end = y + (search_length - 1) * v

                    if 0 <= x_end and x_end < width and 0 <= y_end and y_end < height:
                         if all([file[y + i * v][x + i * u] == c for i, c in enumerate(search_word)]):
                            appearances = appearances + 1

print(appearances)

appearances = 0

for x in range(1, width - 1):
    for y in range(1, height - 1):
        diag1 = file[y - 1][x - 1] + file[y][x] + file[y + 1][x + 1]
        diag2 = file[y + 1][x - 1] + file[y][x] + file[y - 1][x + 1]
        
        if (diag1 == 'MAS' or diag1 == 'SAM') and (diag2 == 'MAS' or diag2 == 'SAM'):
            appearances = appearances + 1

print(appearances)