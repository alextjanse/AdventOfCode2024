from typing import Iterator
from heapq import heappop, heappush

class Maze:
    def __init__(self, layout: list[list[str]]):
        if not all(map(lambda row: len(row) == len(layout[0]), layout)):
            raise Exception("Not every row is of the same length")
        
        self.layout = layout
        self.width = len(layout[0])
        self.height = len(layout)

    def get_cell(self, p: tuple[int, int]) -> str:
        x, y = p

        if not (0 <= x < self.width and 0 <= y < self.height):
            return None
        return self.layout[y][x]
    
    def loop_over_coords(self) -> Iterator[tuple[int, int]]:
        for x in range(self.width):
            for y in range(self.height):
                yield x, y

def get_data() -> Maze:
    with open('data/day16.txt', encoding='utf-8') as file:
        return Maze([list(line) for line in file.read().splitlines()])

def find_start_and_end(maze: Maze) -> tuple[tuple[int, int], tuple[int, int]]:
    start = None
    end = None

    for p in maze.loop_over_coords():
        if maze.get_cell(p) == 'S':
            start = p
        elif maze.get_cell(p) == 'E':
            end = p
    
    return start, end

def get_manhattan_distance(p: tuple[int, int], q: tuple[int, int]) -> int:
    return abs(p[0] - q[0]) + abs(p[1] - q[1])

def solve(maze: Maze) -> int:
    start, end = find_start_and_end(maze)

    distances: dict[tuple[tuple[int, int], tuple[int, int]], int] = dict()

    unhandled_states: list[tuple[int, tuple[int, int], tuple[int, int], list[tuple[int, int]]]] = [
        (0, start, (1, 0), [start]),
    ]

    best_cost = 1e9
    best_paths_visited_positions = set()

    while unhandled_states:
        cost, position, direction, path = heappop(unhandled_states)

        if (position, direction) in distances and cost > distances[position, direction]:
            continue
        distances[position, direction] = cost

        if position == end and cost <= best_cost:
            best_paths_visited_positions.update(path)
            best_cost = cost
        
        px, py = position
        dx, dy = direction
        for c, dx, dy in [(1, dx, dy), (1001, -dy, dx), (1001, dy, -dx)]:
            qx = px + dx
            qy = py + dy
            q = qx, qy

            if maze.get_cell(q) == '#':
                continue

            heappush(unhandled_states, (cost + c, q, (dx, dy), path + [q]))
    
    return best_cost, len(best_paths_visited_positions)

if __name__ == '__main__':
    maze = get_data()
    print(solve(maze))
