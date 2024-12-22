def get_data() -> list[int]:
    with open('data/day22.txt', encoding='utf-8') as file:
        return [int(line) for line in file.read().splitlines()]

def mix(n: int, secret: int) -> int:
    '''Mix the number n with the secret.'''
    return n ^ secret

def prune(secret: int) -> int:
    '''Prune the secret number.'''
    return secret & ((1 << 24) - 1)

def evolve(secret: int) -> int:
    '''Evolve the secret number.'''
    secret = prune(mix(secret << 6, secret))
    secret = prune(mix(secret >> 5, secret))
    secret = prune(mix(secret << 11, secret))
    return secret

def solve(secrets: list[int]) -> None:
    '''Solve both parts simultaneously.'''
    part_1 = 0

    # Keep track of all the sequences, when they occur for the first time for each
    # merchant, and what the price is at that moment.
    sequences: dict[tuple[int, int, int, int], dict[int, int]] = dict()

    for merchant, secret in enumerate(secrets):
        prev_price = secret % 10
        changes = []
        for _ in range(2000):
            secret = evolve(secret)
            price = secret % 10
            # Add the price change to changes and keep the last four
            changes = (changes + [price - prev_price])[-4:]
            # Transform it into a tuple, so it can be hashed for the dict
            seq = tuple(changes)
            if seq not in sequences:
                # New sequence, add it to the dictionary and add the price
                sequences[seq] = dict({ merchant: price })
            elif merchant not in sequences[seq]:
                # This merchant hasn't seen this sequence yet
                sequences[seq][merchant] = price
            prev_price = price
        part_1 += secret
    
    print(part_1)
    
    max_bananas = 0
    for seq, prices in sequences.items():
        if len(seq) < 4:
            # The first sequences get added as well, filter here
            continue
        bananas = sum(prices.values())
        max_bananas = max(max_bananas, bananas)
    print(max_bananas)

if __name__ == '__main__':
    data = get_data()
    solve(data)