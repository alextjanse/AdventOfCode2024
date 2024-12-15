def get_data() -> tuple[list[list[str]], list[str]]:
    '''Parse the data into a list of list of strings and a flattened list of move symbols.'''
    with open('data/day15.txt', encoding='utf-8') as file:
        [layout, moves] = file.read().split('\n\n')
        layout = [list(line) for line in layout.splitlines()]
        moves = ''.join(moves.split())
    return layout, moves

def find_robot(layout: list[list[str]]) -> tuple[int, int]:
    '''Find the x,y-coordinates of the robot in the layout.'''
    for y, row in enumerate(layout):
        for x, col in enumerate(row):
            if col == '@':
                return (x, y)
            
    raise Exception('Robot not found')

def solve_part_1() -> None:
    '''Solve part one one of the problem by updating the layout after each move.'''
    layout, moves = get_data()

    directions = {
        '^': (0, -1),
        'v': (0, 1),
        '<': (-1, 0),
        '>': (1, 0),
    }

    rx, ry = find_robot(layout)

    for move in moves:
        dx, dy = directions[move]
        # Check how many steps forward we have to check.
        d = 1
        while layout[ry + d * dy][rx + d * dx] == 'O':
            d += 1
        # If the space after d-1 boxes is empty, we can move all boxes
        if layout[ry + d * dy][rx + d * dx] == '.':
            # Move the boxes from back to front
            for i in range(d, 0, -1):
                layout[ry + i * dy][rx + i * dx] = layout[ry + (i - 1) * dy][rx + (i - 1) * dx]
            # Empty the current cell and update coordinates
            layout[ry][rx] = '.'
            ry += dy
            rx += dx
    
    gps_sum = 0
    for y, row in enumerate(layout):
        for x, col in enumerate(row):
            if col == 'O':
                gps_sum += 100 * y + x
    
    print(gps_sum)

def can_move(layout: list[list[str]], x: int, y: int, dx: int, dy: int) -> bool:
    '''Recursively check whether the move can be made.'''
    c = layout[y][x]

    if c == '.':
        return True
    if c == '#':
        return False
    if c == '@':
        return can_move(layout, x + dx, y + dy, dx, dy)
    if c == '[':
        # Prevent recursion: only test if a box can move from its left half and based on dx.
        return (can_move(layout, x + dx, y + dy, dx, dy) if dx <= 0 else True) and \
               (can_move(layout, x + 1 + dx, y + dy, dx, dy) if dx >= 0 else True)
    if c == ']':
        # Found right half of box, check if the left half can move
        return can_move(layout, x - 1, y, dx, dy)
    
    raise Exception('Unknown symbol found in layout')

def move(layout: list[list[str]], x: int, y: int, dx: int, dy: int) -> None:
    '''Recursively move all the and robot.'''
    c = layout[y][x]

    if c == '.':
        pass
    elif c == '#':
        raise Exception('Trying to move a wall')
    elif c == '@':
        move(layout, x + dx, y + dy, dx, dy)
        layout[y][x] = '.'
        layout[y + dy][x + dx] = '@'
    elif c == '[':
        # Move the adjacent tile. Adjeceny is based on dx.
        if dx <= 0:
            move(layout, x + dx, y + dy, dx, dy)
        if dx >= 0:
            move(layout, x + 1 + dx, y + dy, dx, dy)
        layout[y][x] = '.'
        layout[y][x + 1] = '.'
        layout[y + dy][x + dx] = '['
        layout[y + dy][x + 1 + dx] = ']'
    elif c == ']':
        # Found right half of a box, move the left half
        move(layout, x - 1, y, dx, dy)
    else:
        raise Exception('Unknown symbol found in layout')

def solve_part_2() -> None:
    layout, moves = get_data()

    upsize_map = {
        '#': '##',
        'O': '[]',
        '.': '..',
        '@': '@.',
    }

    layout = [list(line) for line in [''.join([upsize_map[col] for col in row]) for row in layout]]

    directions = {
        '^': (0, -1),
        'v': (0, 1),
        '<': (-1, 0),
        '>': (1, 0),
    }

    rx, ry = find_robot(layout)

    for (dx, dy) in map(lambda d: directions[d], moves):
        if can_move(layout, rx, ry, dx, dy):
            move(layout, rx, ry, dx, dy)
            rx += dx
            ry += dy
    
    gps_sum = 0
    for y, row in enumerate(layout):
        for x, col in enumerate(row):
            if col == '[':
                gps_sum += 100 * y + x
    
    print(gps_sum)

if __name__ == '__main__':
    solve_part_1()
    solve_part_2()