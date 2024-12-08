from collections import defaultdict
from math import gcd

field = open('data/day8.txt').read().splitlines()

width = len(field[0])
height = len(field)

frequency_locations = defaultdict(list)

# Read out all locations of the antenna's
for y, line in enumerate(field):
    for x, c in enumerate(line):
        if c != '.':
            frequency_locations[c].append((x, y))

def check_in_bounds(x: int, y: int) -> bool:
    '''Check if the given coordinates are in bounds of the field.'''
    global field, width, height
    return 0 <= x < width and 0 <= y < height

antinodes = set()

for frequency, locations in frequency_locations.items():
    for i in range(0, len(locations) - 1):
        (xi, yi) = locations[i]
        for j in range(i + 1, len(locations)):
            (xj, yj) = locations[j]

            # (dx, dy) is the vector from i to j
            (dx, dy) = (xj - xi, yj - yi)

            # a1 is the antinode after j
            (xa1, ya1) = (xj + dx, yj + dy)
            if check_in_bounds(xa1, ya1):
                antinodes.add((xa1, ya1))
            
            # a2 is the antinode before i
            (xa2, ya2) = (xi - dx, yi - dy)
            if check_in_bounds(xa2, ya2):
                antinodes.add((xa2, ya2))

print(len(antinodes))

# No need to clear the antinode set, they're viable for part two as well

for frequency, locations in frequency_locations.items():
    for i in range(0, len(locations) - 1):
        (xi, yi) = locations[i]
        for j in range(i + 1, len(locations)):
            (xj, yj) = locations[j]

            # (dx, dy) is the vector from i to j
            (dx, dy) = (xj - xi, yj - yi)
            
            # Reduce the direction vector to the smallest integer steps
            f = gcd(dx, dy)
            dx //= f
            dy //= f

            i = 0
            while check_in_bounds(xj + i * dx, yj + i * dy):
                antinodes.add((xj + i * dx, yj + i * dy))
                i += 1
            
            i = -1
            while check_in_bounds(xj + i * dx, yj + i * dy):
                antinodes.add((xj + i * dx, yj + i * dy))
                i -= 1

print(len(antinodes))
