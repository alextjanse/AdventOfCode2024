from typing import Iterator

class HeightMap:
    '''A class storing the height data of a map.'''
    def __init__(self, heights: list[list[int]]):
        self.heights = heights
        self.width = len(heights[0])
        self.height = len(heights)
    
    def get_height(self, x, y) -> int:
        '''Get the height at a given coordinate.'''
        return self.heights[y][x]
    
    def enumerate_coordinates(self) -> Iterator[tuple[int, int]]:
        '''Iterate all coordinates in the height map.'''
        for y in range(self.height):
            for x in range(self.width):
                yield (x, y)

def get_height_map() -> HeightMap:
    '''Read the file and return it as a HeightMap.'''
    with open('data/day10.txt', encoding='utf-8') as file:
        data = []

        for line in file.read().splitlines():
            data.append([int(c) for c in line])
    
    return HeightMap(data)

def get_trailhead_score(height_map: HeightMap, x: int, y: int) -> int:
    '''Use DFS to search all paths to find valid paths to endpoints. Return
    the number of reachable endpoints.'''
    if height_map.get_height(x, y) != 0:
        # Starting location is not a trailhead
        return 0

    reachable_endpoints = set()

    trail_stack: list[tuple[int, int, str]] = [(x, y, '')]

    directions = {
        'N': (0, -1),
        'S': (0, 1),
        'W': (-1, 0),
        'E': (1, 0),
    }

    # DFS
    while trail_stack:
        px, py, route = trail_stack.pop()

        if height_map.get_height(px, py) != len(route):
            # The last step in the path is invalid, expected a different height
            continue
        
        if height_map.get_height(px, py) == 9:
            # Check if endpoint has been reached
            reachable_endpoints.add((px, py))
        else:
            # Add all follow-up paths to the stack. Note that stepping back is also
            # added. This however is an invalid path and fill be removed when handled.
            for d, (dx, dy) in directions.items():
                if 0 <= px + dx < height_map.width and 0 <= py + dy < height_map.height:
                    trail_stack.append((px + dx, py + dy, route + d))
    
    return len(reachable_endpoints)

def get_trailhead_rating(height_map: HeightMap, x: int, y: int) -> int:
    '''Similar to get_trailhead_score, but now it counts every successful path
    instead of every reachable endpoint.'''
    if height_map.get_height(x, y) != 0:
        # Starting location is not a trailhead
        return 0

    trail_stack: list[tuple[int, int, str]] = [(x, y, '')]

    directions = {
        'N': (0, -1),
        'S': (0, 1),
        'W': (-1, 0),
        'E': (1, 0),
    }

    rating = 0

    # DFS
    while trail_stack:
        px, py, route = trail_stack.pop()

        if height_map.get_height(px, py) != len(route):
            continue
        
        if height_map.get_height(px, py) == 9:
            rating += 1
        else:
            for d, (dx, dy) in directions.items():
                if 0 <= px + dx < height_map.width and 0 <= py + dy < height_map.height:
                    trail_stack.append((px + dx, py + dy, route + d))
    
    return rating

def solve_part_1(height_map: HeightMap) -> None:
    '''Solve the first part of the problem.'''
    total_score = 0

    for x, y in height_map.enumerate_coordinates():
        total_score += get_trailhead_score(height_map, x, y)
    
    print(total_score)

def solve_part_2(height_map: HeightMap) -> None:
    '''Solve the second part of the problem.'''
    total_rating = 0

    for x, y in height_map.enumerate_coordinates():
        total_rating += get_trailhead_rating(height_map, x, y)
    
    print(total_rating)

if __name__ == '__main__':
    height_map = get_height_map()
    solve_part_1(height_map)
    solve_part_2(height_map)
