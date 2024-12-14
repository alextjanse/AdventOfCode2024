def get_data() -> tuple[int, int, int, int, int, int]:
    with open('data/day13.txt', encoding='utf-8') as file:
        raw_data = file.read()
    
    machine_info: list[tuple[int, int, int, int, int, int]] = []

    for machine in raw_data.split('\n\n'):
        [_, _, a11, a12, _, _, a21, a22, _, b1, b2] = machine.split()

        a11 = int(a11[2:-1])
        a12 = int(a12[2:])
        a21 = int(a21[2:-1])
        a22 = int(a22[2:])
        b1 = int(b1[2:-1])
        b2 = int(b2[2:])

        machine_info.append((a11, a12, a21, a22, b1, b2))
    
    return machine_info

def solve(machine_info: list[tuple[int, int, int, int, int, int]], target_offset = 0) -> None:
    '''Solve part one by solving plane-line intersections in 3D.'''
    total_cost = 0

    for (a11, a12, a21, a22, b1, b2) in machine_info:
        '''The solution plane has base vectors v=(a11, a12, 3) and w=(a21, a22, 1).
        Going one step into direction v corresponds to pressing Button A once and vice
        versa for w with Button B. The target (b1, b2) becomes a line with base (b1, b2, 0)
        and direction (0, 0, 1). The plane and line intersect at P=(b1, b2, c), where c is the
        cost of reaching the target. If the plane and line are not parallel, then the solution
        is unique.
        There is one problem: we can only do full steps of v and w. We can check this by breaking
        up P into P=i*v + j*w for some i and j, and check if i and j are integer numbers.
        For more info on the calculations:
        https://en.wikipedia.org/wiki/Line%E2%80%93plane_intersection#Parametric_form
        '''
        b1 += target_offset
        b2 += target_offset

        det = a11 * a22 - a21 * a12

        if det == 0:
            # Parallel: no solution
            continue
 
        i = (b1 * a22 - b2 * a21) / det
        j = (b2 * a11 - b1 * a12) / det 

        if i.is_integer() and j.is_integer():
            total_cost += int(3 * i + j)

    print(total_cost)

if __name__ == '__main__':
    machine_info = get_data()
    solve(machine_info)
    solve(machine_info, 10000000000000)
