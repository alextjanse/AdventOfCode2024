class FieldMap:
    def __init__(self, data: list[list[str]]):
        if not all(map(lambda row: len(row) == len(data[0]), data)):
            raise Exception("Not all rows are of the same length.")
        
        self.field = data
        self.width = len(data[0])
        self.height = len(data)

    def get_field_type(self, x: int, y: int) -> str | None:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.field[y][x]
        return None
    
def get_field_map():
    with open('data/day12.txt', encoding='utf-8') as file:
        data = [[str(c) for c in line] for line in file.read().splitlines()]
    
    return FieldMap(data)

def find_field(field_map: FieldMap, qx: int, qy: int) -> tuple[set[(int, int)], set[(int, int)]]:
    '''Find the coordinates, area and perimeter of a field. Returns
    a tuple of a set of field coordinates, the area, and the perimeter.'''
    field_type = field_map.get_field_type(qx, qy)

    field_coordinates = set()

    coordinate_stack: list[tuple[int, int, int, int]] = [(qx, qy, qx, qy)]

    directions = {
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    }

    fences: set[tuple[int, int]] = set()

    while coordinate_stack:
        ox, oy, px, py = coordinate_stack.pop()

        if (px, py) in field_coordinates:
            continue

        if field_map.get_field_type(px, py) != field_type:
            # This (px, py) lies outside the field, so there is a fence.
            fences.add((ox + 0.1 * (px - ox), oy + 0.1 * (py - oy)))
            continue

        field_coordinates.add((px, py))

        for (dx, dy) in directions:
            coordinate_stack.append((px, py, px + dx, py + dy))
    
    return field_coordinates, fences

def solve_part_1(field_map: FieldMap) -> None:
    handled_coordinates = set()

    fields: list[set[tuple[int, int]]] = []

    total_price = 0

    for y in range(field_map.height):
        for x in range(field_map.width):
            if (x, y) not in handled_coordinates:
                field, fences = find_field(field_map, x, y)
                handled_coordinates.update(field)
                total_price += len(field) * len(fences)

    print(total_price)

def get_fence_sides(fences: set[tuple[int, int]]) -> int:
    sides = 0

    unhandled_fences = fences.copy()

    while unhandled_fences:
        fx, fy = unhandled_fences.pop()

        sides += 1

        # Determine direction based on fence type
        dx, dy = (1, 0) if fx % 1 == 0 else (0, 1)  # Horizontal: move along y, Vertical: move along x

        # Remove fences in both positive and negative directions
        for direction in (1, -1):
            i = direction
            while (fx + i * dx, fy + i * dy) in unhandled_fences:
                unhandled_fences.remove((fx + i * dx, fy + i * dy))
                i += direction
    
    return sides

def solve_part_2(field_map: FieldMap) -> None:
    handled_coordinates = set()

    total_price = 0

    for y in range(field_map.height):
        for x in range(field_map.width):
            if (x, y) not in handled_coordinates:
                field, fences = find_field(field_map, x, y)
                handled_coordinates.update(field)
                sides = get_fence_sides(fences)
                total_price += len(field) * sides
    
    print(total_price)

if __name__ == '__main__':
    field_map = get_field_map()
    solve_part_1(field_map)
    solve_part_2(field_map)
