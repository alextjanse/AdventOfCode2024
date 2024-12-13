def get_data():
    with open('data/day13.txt', encoding='utf-8') as file:
        raw_data = file.read()
    
    machine_info: list[tuple[int, int, int, int, int, int]] = []

    for machine in raw_data.split('\n\n'):
        [_, _, a11, a12, _, _, a21, a22, _, b1, b2] = machine.split()

        a11 = int(a11[2:-1])
        a12 = int(a12[2:])
        a21 = int(a21[2:-1])
        b1 = int(b1[2:-1])
        b2 = int(b2[2:])

        machine_info.append((a11, a12, a21, a22, b1, b2))
    
    return machine_info

def dot(v1: tuple[int, int, int], v2: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(map(lambda x: x[0] * x[1], zip(v1, v2)))

def cross(v1: tuple[int, int, int], v2: tuple[int, int, int]) -> tuple[int, int, int]:
    (x1, y1, z1) = v1
    (x2, y2, z2) = v2
    return (y1 * z2 - z1 * y2, z1 * x2 - x1 * z2, x1 * y2 - y1 * x2)

def solve_part_1(machine_info):
    '''Solve part one by solving plane-line intersections in 3D. The points on
    the plane are the reachable amounts by pressing button A and B. The z-axis
    represents the total cost. The line is the target: (b1, b2, 0) + d*(0, 0, 1).
    For more info:
    https://en.wikipedia.org/wiki/Line%E2%80%93plane_intersection#Algebraic_form'''
    total_cost = 0

    for (a11, a12, a21, a22, b1, b2) in machine_info:
        v1 = (a11, a12, 3)
        v2 = (a21, a22, 1)

        n = cross(v1, v2)
 
        cost = dot((-b1, -b2, 0), n) / dot((0, 0, 1), n)

        total_cost += cost

    print(total_cost)

if __name__ == '__main__':
    machine_info = get_data()
