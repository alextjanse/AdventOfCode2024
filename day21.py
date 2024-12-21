from heapq import heappop, heappush

NUMERICAL_KEYPAD = {
    (0, 0): '7', (1, 0): '8', (2, 0): '9',
    (0, 1): '4', (1, 1): '5', (2, 1): '6',
    (0, 2): '1', (1, 2): '2', (2, 2): '3',
                 (1, 3): '0', (2, 3): 'A',
}

DIRECTIONAL_KEYPAD = {
                 (1, 0): '^', (2, 0): 'A',
    (0, 1): '<', (1, 1): 'v', (2, 1): '>',
}

DIRECTIONS = {
    '<': (-1, 0),
    '>': (1, 0),
    '^': (0, -1),
    'v': (0, 1),
}

def get_data() -> list[str]:
    with open('data/day21.txt', encoding='utf-8') as file:
        return file.read().splitlines()

def get_shortest_seq_length(code: str, directional_robots: int) -> int:
    '''Find the shortest sequence of input using BFS.'''
    unhandled_states = [(0, '', [(2, 0)] * directional_robots, (2, 3))]
    handled_states = set()

    while unhandled_states:
        t, out, directional_pos, numerical_pos = heappop(unhandled_states)

        state_check = (out, tuple(directional_pos), numerical_pos)

        if state_check in handled_states:
            continue
        handled_states.add(state_check)

        if out == code:
            return t
        
        # I press direction
        for dx, dy in DIRECTIONS.values():
            x, y = directional_pos[0]
            x, y = x + dx, y + dy
            if (x, y) in DIRECTIONAL_KEYPAD:
                heappush(unhandled_states, (t + 1, out, [(x, y)] + directional_pos[1:], numerical_pos))

        # I Press A

        # Use a copy of the directions for the new states
        new_directional_pos = directional_pos[:]

        i = 0
        while i < len(directional_pos):
            action = DIRECTIONAL_KEYPAD[directional_pos[i]]
            if action in DIRECTIONS:
                dx, dy = DIRECTIONS[action]

                if i + 1 < len(directional_pos):
                    x, y = directional_pos[i + 1]
                    x, y = x + dx, y + dy
                    if (x, y) in DIRECTIONAL_KEYPAD:
                        new_directional_pos[i + 1] = x, y
                        heappush(unhandled_states, (t + 1, out, new_directional_pos, numerical_pos))
                else:
                    x, y = numerical_pos
                    x, y = x + dx, y + dy
                    if (x, y) in NUMERICAL_KEYPAD:
                        heappush(unhandled_states, (t + 1, out, new_directional_pos, (x, y)))
                
                break
            else: # Action is A
                i += 1
        
        if i == len(directional_pos):
            # Numerical keypad is being pressed
            action = NUMERICAL_KEYPAD[numerical_pos]
            if action != code[len(out)]:
                continue
            heappush(unhandled_states, (t + 1, out + action, new_directional_pos, numerical_pos))

def solve_part_1(codes: list[str]) -> None:
    complexity_sum = 0

    for code in codes:
        shortest_seq_length = get_shortest_seq_length(code, 2)
        numeric_part = int(code[:-1])
        complexity_sum += shortest_seq_length * numeric_part
    
    print(complexity_sum)

def solve_part_2(codes: list[str]) -> None:
    complexity_sum = 0

    for code in codes:
        pass

    print(complexity_sum)

if __name__ == '__main__':
    codes = get_data()
    solve_part_1(codes)
    solve_part_2(codes)