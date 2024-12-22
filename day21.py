from heapq import heappop, heappush
from collections import Counter

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
    unhandled_states = [(0, '', '', [(2, 0)] * directional_robots, (2, 3))]
    handled_states = set()

    while unhandled_states:
        t, input, out, directional_pos, numerical_pos = heappop(unhandled_states)

        state_check = (out, tuple(directional_pos), numerical_pos)

        if state_check in handled_states:
            continue
        handled_states.add(state_check)

        if out == code:
            print(input)
            return t
        
        # I press direction
        for d, (dx, dy) in DIRECTIONS.items():
            x, y = directional_pos[0]
            x, y = x + dx, y + dy
            if (x, y) in DIRECTIONAL_KEYPAD:
                heappush(unhandled_states, (t + 1, input + d, out, [(x, y)] + directional_pos[1:], numerical_pos))

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
                        heappush(unhandled_states, (t + 1, input + 'A', out, new_directional_pos, numerical_pos))
                else:
                    x, y = numerical_pos
                    x, y = x + dx, y + dy
                    if (x, y) in NUMERICAL_KEYPAD:
                        heappush(unhandled_states, (t + 1, input + 'A', out, new_directional_pos, (x, y)))
                
                break
            else: # Action is A
                i += 1
        
        if i == len(directional_pos):
            # Numerical keypad is being pressed
            action = NUMERICAL_KEYPAD[numerical_pos]
            if action != code[len(out)]:
                continue
            heappush(unhandled_states, (t + 1, input + 'A', out + action, new_directional_pos, numerical_pos))

def solve_part_1(codes: list[str]) -> None:
    complexity_sum = 0

    for code in codes:
        seq = get_shortest_seq_length(code, 2)
        numeric_part = int(code[:-1])
        complexity_sum += seq * numeric_part
    
    print(complexity_sum)

def get_shortest_seq(keypad: dict[tuple[int, int], str], required_seq: str, start_button = 'A') -> str:
    start_pos = next(k for k, v in keypad.items() if v == start_button)
    unhandled_states = [(0, '', start_pos, '')]

    handled_states = dict()

    while unhandled_states:
        t, seq, pos, out = heappop(unhandled_states)

        if out == required_seq:
            return seq
        
        if (pos, out) in handled_states and t > handled_states[pos, out]:
            continue
        handled_states[pos, out] = t

        for d, (dx, dy) in DIRECTIONS.items():
            last_moves = seq.split('A')[-1]
            if d in last_moves and last_moves[-1] != d:
                # Prevent switching between directions
                continue
            new_pos = pos[0] + dx, pos[1] + dy

            if new_pos in keypad:
                heappush(unhandled_states, (t + 1, seq + d, new_pos, out))
        
        if keypad[pos] == required_seq[len(out)]:
            heappush(unhandled_states, (t + 1, seq + 'A', pos, out + keypad[pos]))

def solve_part_2(codes: list[str], direction_robots: int) -> None:
    move_translations = dict()

    move_translations['A'] = 'A'

    for d1 in DIRECTIONS:
        move_translations[d1 + 'A'] = get_shortest_seq(DIRECTIONAL_KEYPAD, d1 + 'A')
        for d2 in DIRECTIONS:
            move_translations[d1 + d2 + 'A'] = get_shortest_seq(DIRECTIONAL_KEYPAD, d1 + d2 + 'A')
            for d3 in DIRECTIONS:
                move_translations[d1 + d2 + d3 + 'A'] = get_shortest_seq(DIRECTIONAL_KEYPAD, d1 + d2 + d3 + 'A')

    complexity_score = 0

    for code in codes:
        seq = get_shortest_seq(NUMERICAL_KEYPAD, code)
        parts = Counter(map(lambda s: s + 'A', seq.split('A')))
        for _ in range(direction_robots):
            new_parts = Counter()
            for part, amount in parts.items():
                seq = move_translations[part]
                for new_part in map(lambda s: s + 'A', seq.split('A')[:-1]):
                    new_parts[new_part] += amount
            parts = new_parts
        seq_length = sum(map(lambda p: len(p[0]) * p[1], parts.items()))
        complexity_score += int(code[:-1]) * seq_length

    print(complexity_score)

if __name__ == '__main__':
    codes = get_data()
    # solve_part_1(codes)
    solve_part_2(['023A'], 2)