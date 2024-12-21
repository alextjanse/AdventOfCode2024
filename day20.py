from heapq import heappop, heappush
from collections import defaultdict

def get_data() -> list[list[str]]:
    '''Parse the data into a 2d-list of characters.'''
    with open('data/day20.txt', encoding='utf-8') as file:
        return [list(line) for line in file.read().splitlines()]

def find_start(maze: list[list[str]]) -> tuple[tuple[int, int]]:
    '''Find the start position in the maze.'''
    start = None

    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 'S':
                start = x, y
    
    return start

def get_distances(maze: list[list[str]]) -> defaultdict[tuple[int, int], int]:
    '''Get the non-cheating distances from the start to each position in the maze.'''
    width = len(maze[0])
    height = len(maze)

    start = find_start(maze)

    distances = defaultdict(lambda: 1e9)

    unhandled_states = [(0, start)]

    while unhandled_states:
        cost, position = heappop(unhandled_states)

        if cost >= distances[position]:
            continue
        distances[position] = cost
        
        px, py = position
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            qx, qy = px + dx, py + dy
            
            if not (0 <= qx < width and 0 <= qy < height) or maze[qy][qx] == '#':
                continue

            heappush(unhandled_states, (cost + 1, (qx, qy)))
    
    return distances

def manhattan_distance(p: tuple[int, int], q: tuple[int, int]) -> int:
    '''Get the Manhattan distance between two points.'''
    px, py = p
    qx, qy = q
    return abs(px - qx) + abs(py - qy)

def find_cheat_paths(distances: defaultdict[tuple[int, int], int], total_cheats: int, min_saved: int) -> int:
    '''Check all possible cheats by pairing all possible starting positions
    and ending positions, checking if the cheat distance is valid and if the
    time saved is enough.'''
    result = 0

    for cheat_start, start_distance in distances.items():
        for cheat_end, end_distance in distances.items():
            cheat_distance = manhattan_distance(cheat_start, cheat_end)
            time_saved = end_distance - start_distance - cheat_distance
            if cheat_distance <= total_cheats and time_saved >= min_saved:
                result += 1
    
    print(result)

if __name__ == '__main__':
    maze = get_data()
    distances = get_distances(maze)
    find_cheat_paths(distances, 2, 100)
    find_cheat_paths(distances, 20, 100)
