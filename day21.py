from heapq import heappop, heappush

NUMERICAL_KEYPAD = {
    (0, 0): '7',
    (1, 0): '8',
    (2, 0): '9',
    (0, 1): '4',
    (1, 1): '5',
    (2, 1): '6',
    (0, 2): '1',
    (1, 2): '2',
    (2, 2): '3',
    (1, 3): '0',
    (2, 3): 'A',
}

DIRECTIONAL_KEYPAD = {
    (1, 0): '^',
    (2, 0): 'A',
    (0, 1): '<',
    (1, 1): 'v',
    (2, 1): '>',
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

def get_shortest_seq_length(code: str) -> int:
    unhandled_states = [(0, '', (2, 0), '', (2, 0), '', (2, 3), '')]
    handled_states = set()

    while unhandled_states:
        t, in_0, pos_1, in_1, pos_2, in_2, pos_3, in_3 = heappop(unhandled_states)

        if (in_3, pos_1, pos_2, pos_3) in handled_states:
            continue
        handled_states.add((in_3, pos_1, pos_2, pos_3))

        if in_3 == code:
            return t
        
        # I press direction
        for d, (dx, dy) in DIRECTIONS.items():
            x, y = pos_1[0] + dx, pos_1[1] + dy
            if (x, y) in DIRECTIONAL_KEYPAD:
                heappush(unhandled_states, (t + 1, in_0 + d, (x, y), in_1, pos_2, in_2, pos_3, in_3))

        # I press A
        action_1 = DIRECTIONAL_KEYPAD[pos_1]
        if action_1 in DIRECTIONS: # Robot 1 presses direction
            dx, dy = DIRECTIONS[action_1]
            x, y = pos_2[0] + dx, pos_2[1] + dy
            if (x, y) in DIRECTIONAL_KEYPAD:
                heappush(unhandled_states, (t + 1, in_0 + 'A', pos_1, in_1 + action_1, (x, y), in_2, pos_3, in_3))
        else: # Robot 1 presses A
            action_2 = DIRECTIONAL_KEYPAD[pos_2]
            if action_2 in DIRECTIONS: # Robot 2 presses direction
                dx, dy = DIRECTIONS[action_2]
                x, y = pos_3[0] + dx, pos_3[1] + dy
                if (x, y) in NUMERICAL_KEYPAD:
                    heappush(unhandled_states, (t + 1, in_0 + 'A', pos_1, in_1 + action_1, pos_2, in_2 + action_2, (x, y), in_3))
            else: # Robot 2 presses A
                action_3 = NUMERICAL_KEYPAD[pos_3]
                if action_3 != code[len(in_3)]:
                    continue
                heappush(unhandled_states, (t + 1, in_0 + 'A', pos_1, in_1 + action_1, pos_2, in_2 + action_2, pos_3, in_3 + action_3))

def solve_part_1(codes: list[str]) -> None:
    complexity_sum = 0

    for code in codes:
        shortest_seq_length = get_shortest_seq_length(code)
        numeric_part = int(code[:-1])
        complexity_sum += shortest_seq_length * numeric_part
    
    print(complexity_sum)

if __name__ == '__main__':
    codes = get_data()
    solve_part_1(codes)