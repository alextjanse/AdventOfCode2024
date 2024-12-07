from typing import Iterator

lines = open('data/day7.txt').read().splitlines()

def check_combination(target: int, numbers: list[int], operators: list[str]) -> bool:
    '''Check if the target is met if following the given operators.'''
    result = numbers[0]

    for i, op in enumerate(operators):
        if op == '+':
            result += numbers[i + 1]
        elif op == '*':
            result *= numbers[i + 1]
        elif op == '||':
            result = int(str(result) + str(numbers[i + 1]))
        else:
            raise Exception("Unknown operator")
    
    return result == target

def operator_combinations(operators: list[str], length: int) -> Iterator[list[str]]:
    '''Iterate over all possible combinations of the given operators.'''
    num_operators = len(operators)
    combination = [operators[0]] * length

    '''There are n ** length number of combinations, where n is the number of operators.
    If we loop over all those numbers and convert them to a base-n number, then each digit
    corresponds to a operator for each position in the combination. We can find the exact
    operator by doing a modulo with the number of operators, and then for the next position
    we adjust by shifting to the next digit by deviding by n.'''
    for index in range(num_operators**length):
        temp_index = index
        for i in range(length):
            combination[i] = operators[temp_index % num_operators]
            temp_index //= num_operators
        yield combination[:]

part_1 = 0
part_2 = 0

for line in lines:
    [target, numbers] = line.split(': ')
    target = int(target)
    numbers = [int(n) for n in numbers.split(' ')]

    # Part 1: only two operators
    for operators in operator_combinations(['+', '*'], len(numbers) - 1):
        if check_combination(target, numbers, operators):
            part_1 += target
            break

    # Part 2: three operators
    for operators in operator_combinations(['+', '*', '||'], len(numbers) - 1):
        if check_combination(target, numbers, operators):
            part_2 += target
            break

print(part_1)
print(part_2)
