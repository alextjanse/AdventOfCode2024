from collections import defaultdict, Counter

def get_data() -> list[int]:
    '''Read the data from the file and return it as a list of integers.'''
    with open('data/day11.txt', encoding='utf-8') as file:
        data = file.read().rstrip().split(' ')
    return [int(i) for i in data]

def count_stones(value: int, steps: int) -> int:
    '''Count how many stones there are after a given amount of steps. Use recursion.'''
    if steps == 0:
        # No more steps
        return 1
    
    s = str(value)

    if value == 0:
        return count_stones(1, steps - 1)
    if len(s) % 2 == 0:
        split_1 = int(s[: len(s) // 2])
        split_2 = int(s[len(s) // 2: ])
        return count_stones(split_1, steps - 1) + count_stones(split_2, steps - 1)
    
    return count_stones(2024 * value, steps - 1)

def solve_part_1(stones: list[int], steps: int) -> None:
    '''Solve part one with recursion.'''
    result = 0

    for stone in stones:
        result += count_stones(stone, steps)
    
    print(result)

def get_next_split(value: int) -> tuple[int, int, int]:
    '''Calculate in how many steps the stone will split and in which
    numbers it splits.'''

    steps = 1

    while len(str(value)) % 2 != 0:
        value = 1 if value == 0 else 2024 * value
        steps += 1
    
    s = str(value)

    if steps > 75:
        print('too many steps! {steps}')

    return (steps, int(s[: len(s) // 2]), int(s[len(s) // 2:]))

class EventQueue:
    '''Class for an event queue. At each timestamp, store a counter
    that counts the number of stones with each value.'''
    def __init__(self):
        self.events = defaultdict(Counter)

    def is_empty(self) -> bool:
        '''Check if the event queue is empty.'''
        return len(self.events) == 0
    
    def get_next_events(self) -> tuple[int, Counter]:
        '''Get the counter at the lowest time and remove it from the event queue.'''
        time = min(self.events.keys())
        return (time, self.events.pop(time))
    
    def add_event(self, time, item, amount = 1) -> None:
        '''Add an amount of an item at a given time.'''
        self.events[time][item] += amount

def solve_part_2(stones: list[int], max_steps: int) -> None:
    '''Solve part two using an event queue.'''
    result = len(stones)

    stone_lookup: dict[int, tuple[int, int, int]] = dict()

    # Create an event queue
    event_queue = EventQueue()

    # Add the starting stones to the event queue
    for stone in stones:
        event_queue.add_event(0, stone)

    while not event_queue.is_empty():
        # Get all the stones that split at this time
        time, event_stones = event_queue.get_next_events()

        for stone, amount in event_stones.items():
            # For each stone that splits, queue the next split event
            if stone not in stone_lookup:
                stone_lookup[stone] = get_next_split(stone)
            
            steps, split_1, split_2 = stone_lookup[stone]

            if time + steps <= max_steps:
                # Only queue events that are in the time window
                result += amount
                event_queue.add_event(time + steps, split_1, amount)
                event_queue.add_event(time + steps, split_2, amount)

    print(result)

if __name__ == '__main__':
    stones = get_data()
    solve_part_1(stones, 25)
    solve_part_2(stones, 75)
