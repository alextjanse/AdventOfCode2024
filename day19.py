def get_data() -> tuple[list[str], list[list[str]]]:
    with open('data/day19.txt', encoding='utf-8') as file:
        lines = file.read()

        [patterns, designs] = lines.split('\n\n')
        patterns = patterns.split(', ')
        designs = designs.splitlines()
        
        return patterns, designs

def solve(patterns, designs):
    '''Solve using dynamic programming. We can check in how many ways
    the end of the design can be made and increase the size of the design
    from the back. If a pattern is smaller than the current length and fits
    the start of the current design, we can easily check if the rest of the
    design (current design - length of pattern) was possible.'''
    
    # Sort patterns, so we can easily skip to the next end length
    patterns.sort(key=len)

    possible_designs = 0
    possible_ways = 0

    for design in designs:
        # Dynamic program: how many ways are the end stripes possible
        dp = [0] * len(design)
        
        # For each i, take the i last stripes of the design
        for i in range(1, len(design) + 1):
            for pattern in patterns:
                if len(pattern) > i:
                    # Patterns is sorted by length, all following patterns are too long
                    break
                elif pattern == design[-i:]:
                    dp[-i] += 1
                elif pattern == design[-i:len(pattern) - i] and dp[len(pattern) - i] > 0:
                    dp[-i] += dp[len(pattern) - i]
        
        # dp[0] is the number of ways that the total design can me made
        possible_designs += 1 if dp[0] > 0 else 0
        possible_ways += dp[0]
    
    print(possible_designs, possible_ways)

if __name__ == '__main__':
    data = get_data()
    solve(*data)