def get_data() -> list[tuple[tuple[int, int], tuple[int, int]]]:
    with open('data/day14.txt', encoding='utf-8') as file:
        return [tuple(tuple(int(i) for i in s[2:].split(',')) for s in line.split(' ')) \
            for line in file.read().splitlines()]

def solve_part_1(robot_data: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:
    '''Calculate where each robot is after 100 seconds and check in which quadrant they are.'''
    width = 101
    height = 103
    time = 100
    
    quadrants = {
        'top-left': 0,
        'top-right': 0,
        'bottom-left': 0,
        'bottom-right': 0,
        'middle': 0,
    }

    for ((px, py), (vx, vy)) in robot_data:
        x = (px + vx * time) % width
        y = (py + vy * time) % height

        if x < width // 2:
            if y < height // 2:
                quadrants['top-left'] += 1
            elif y > height // 2:
                quadrants['bottom-left'] += 1
            else:
                quadrants['middle'] += 1
        elif x > width // 2:
            if y < height // 2:
                quadrants['top-right'] += 1
            elif y > height // 2:
                quadrants['bottom-right'] += 1
            else:
                quadrants['middle'] += 1
        else:
            quadrants['middle'] += 1

    safety_factor = quadrants['top-left'] * quadrants['top-right'] * quadrants['bottom-left'] * quadrants['bottom-right']
    print(safety_factor)

def solve_part_2(robot_data: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:
    '''Print the robot layout at after each iteration and ask the user to confirm if it's a
    christmas tree.'''
    width = 101
    height = 103

    isChristmasTree = False

    # Noticed that at this time a strip formed
    time = 46

    while not isChristmasTree:
        print(f't={time}')

        picture = [['.' for _ in range(width)] for _ in range(height)]
        
        for i, ((px, py), (vx, vy)) in enumerate(robot_data):
            x = (px + vx * time) % width
            y = (py + vy * time) % height

            picture[y][x] = '#'

        for y in range(height):
            print(''.join(picture[y]))

        isChristmasTree = input('Is it a christmas tree? (y/n)') == 'y'

        # Every 101 steps, the strip would return
        time += 101
    
    print(time)

if __name__ == '__main__':
    data = get_data()
    solve_part_1(data)
    solve_part_2(data)
