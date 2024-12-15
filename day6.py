from collections import defaultdict

field = [list(s) for s in open('data/day6.txt').read().splitlines()]

width = len(field[0])
height = len(field)

def find_guard() -> tuple[int, int]:
    '''Search the start point of the guard.'''
    global field, width, height

    for y in range(height):
        for x in range(width):
            if field[y][x] == '^':
                return (x, y)
    
    raise Exception('Start point not found.')

def get_visited_coords() -> set[tuple[int, int]]:
    '''Count the number of steps the guard takes.'''
    global field, width, height

    (x, y) = find_guard()
    (dx, dy) = (0, -1)

    # Store the coords that the guard visits
    visited_coords = set()

    while True:
        visited_coords.add((x, y))
        
        if not (0 <= x + dx < width and 0 <= y + dy < height):
            # Guard is out of bounds, return # of visited coords
            return visited_coords
        elif field[y + dy][x + dx] == '#':
            # Obstruction: turn right
            (dx, dy) = (-dy, dx)
        else:
            # No obstruction: set a step forward
            (x, y) = (x + dx, y + dy)
        
normal_route = get_visited_coords()
print(len(normal_route))

def check_for_loop() -> bool:
    '''Check if the guard walks in a loop.'''
    global field, width, height

    (x, y) = find_guard()
    (dx, dy) = (0, -1)

    # Store the direction of the guard at each step. If the guard walks
    # in the same direction on the same coord twice, he is looping.
    visited_coords_dir = defaultdict(set)

    while True:
        if (dx, dy) in visited_coords_dir[(x, y)]:
            # Already walked in this direction on this coord
            return True
        
        visited_coords_dir[(x, y)].add((dx, dy))

        if not (0 <= x + dx < width and 0 <= y + dy < height):
            # Out of bounds
            return False
        elif field[y + dy][x + dx] == '#':
            # Obstruction: turn right
            (dx, dy) = (-dy, dx)
        else:
            # No obstruction: set a step forward
            (x, y) = (x + dx, y + dy)

possible_obstructions = 0

# Check for every step on the normal path if obstructing it would result in a loop
for (x, y) in normal_route:
    if field[y][x] == '.':
        field[y][x] = '#'
        
        if check_for_loop():
            possible_obstructions += 1
        
        field[y][x] = '.'

print(possible_obstructions)
