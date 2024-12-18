def get_data(number_of_bytes = None) -> list[list[str]]:
    '''Transform the bytes into a field, where the bytes are blocks (#) and open
    spaces are dots (.).'''
    width, height = 71, 71

    field = [['.' for _ in range(width)] for _ in range(height)]

    with open('data/day18.txt', encoding='utf-8') as file:
        for line in file.read().splitlines()[:number_of_bytes]:
            [x, y] = [int(i) for i in line.split(',')]
            field[y][x] = '#'
    
    return field

def get_shortest_path(field: list[list[str]]) -> list[tuple[int, int]]:
    '''Get the shortest path in the field from start (top-left) to the end (bottom-right).
    Return as a list of visited positions.'''
    width = len(field[0])
    height = len(field)

    start = 0, 0
    end = width - 1, height - 1

    bfs_queue = [(start, '')]
    visited = set()

    while bfs_queue:
        position, path = bfs_queue.pop(0)

        if position == end:
            x, y = 0, 0
            route = [(x, y)]
            for d in path:
                if d == 'N':
                    y -= 1
                elif d == 'S':
                    y += 1
                elif d == 'E':
                    x += 1
                elif d == 'W':
                    x -= 1
                route.append((x, y))
            return route

        if position in visited:
            continue
        visited.add(position)

        px, py = position
        for dx, dy, d in [(1, 0, 'E'), (-1, 0, 'W'), (0, -1, 'N'), (0, 1, 'S')]:
            qx = px + dx
            qy = py + dy
            if 0 <= qx < width and 0 <= qy < height and field[qy][qx] == '.':
                bfs_queue.append(((px + dx, py + dy), path + d))
    
    return None

def solve_part_1():
    '''Get the field after the first 1024 bytes and find the shortest path in it.'''
    field = get_data(1024)
    route = get_shortest_path(field)
    print(len(route) - 1) # -1, because start position is counted as well

def solve_part_2():
    '''Keep track of the shorest path and update it if a new byte blocks it. If no
    path can be found, print the byte that blocked the way and halt'''
    width, height = 71, 71

    field = [['.' for _ in range(width)] for _ in range(height)]

    with open('data/day18.txt', encoding='utf-8') as file:
        bytes = [(int(x), int(y)) for [x, y] in [byte.split(',') for byte in file.read().splitlines()]]
    
    shortest_path = get_shortest_path(field)

    for byte in bytes:
        bx, by = byte
        field[by][bx] = '#'
        if byte in shortest_path:
            shortest_path = get_shortest_path(field)

            if shortest_path is None:
                # This byte blocks all ways
                print(byte)
                break

if __name__ == '__main__':
    solve_part_1()
    solve_part_2()