from typing import Iterator


def get_data() -> tuple[list[int], int, int, int]:
    '''Parse the data as a tuple of the register values and the program.'''
    with open('data/day17.txt', encoding='utf-8') as file:
        lines = file.read().splitlines()
        a = int(lines[0].split(': ')[1])
        b = int(lines[1].split(': ')[1])
        c = int(lines[2].split(': ')[1])

        program = [int(i) for i in lines[4].split(': ')[1].split(',')]
    
    return program, a, b, c

def get_combo_operand(operand: int, a: int, b: int, c: int) -> int:
    '''Return the combo operand depending on the operand value.'''
    if operand <= 3: return operand
    if operand == 4: return a
    if operand == 5: return b
    if operand == 6: return c
    
    raise Exception("Unknown operand")

def run_program(program: list[int], a: int, b: int, c: int) -> list[int]:
    '''Run the program and return the output.'''
    pointer = 0
    output = []
    
    while pointer < len(program):
        opcode = program[pointer]
        operand = program[pointer + 1]

        if opcode == 0: # adv
            a = a // (2**get_combo_operand(operand, a, b, c))
        elif opcode == 1: # bxl
            b = b ^ operand
        elif opcode == 2: # bst
            b = get_combo_operand(operand, a, b, c) % 8
        elif opcode == 3: # jnz
            if a != 0:
                pointer = operand
                continue
        elif opcode == 4: # bxc
            b = b ^ c
        elif opcode == 5: # out
            output.append(get_combo_operand(operand, a, b, c) % 8)
        elif opcode == 6: # bdv
            b = a // (2**get_combo_operand(operand, a, b, c))
        elif opcode == 7: # cdv
            c = a // (2**get_combo_operand(operand, a, b, c))
        else:
            raise Exception("Unknown instruction")
        
        pointer += 2
    
    return output

def check_program(program: list[int], a: int, b: int, c: int, depth) -> bool:
    '''Run the program and check whether the program outputs last
    numbers of the program.'''
    pointer = 0
    output = []

    expected_output = program[-depth - 1:]
    
    while pointer < len(program):
        opcode = program[pointer]
        operand = program[pointer + 1]

        if opcode == 0: # adv
            a = a // (2**get_combo_operand(operand, a, b, c))
        elif opcode == 1: # bxl
            b = b ^ operand
        elif opcode == 2: # bst
            b = get_combo_operand(operand, a, b, c) % 8
        elif opcode == 3: # jnz
            if a != 0:
                pointer = operand
                continue
        elif opcode == 4: # bxc
            b = b ^ c
        elif opcode == 5: # out
            x = get_combo_operand(operand, a, b, c) % 8

            # Check if the expected output is correct.
            if expected_output[len(output)] != x:
                return False
            
            output.append(x)
        elif opcode == 6: # bdv
            b = a // (2**get_combo_operand(operand, a, b, c))
        elif opcode == 7: # cdv
            c = a // (2**get_combo_operand(operand, a, b, c))
        else:
            raise Exception("Unknown instruction")

        pointer += 2
    
    # Because we checked if the output values are correct,
    # only check if the lengths are the same
    return len(output) == len(expected_output)

def find_self_printing_a(program: list[int], current_a: int = 0, depth = 0) -> Iterator[int]:
    '''Find the value for a, so that the program returns itself. The program
    always contains a (0, 3) command, which shifts a 3 bits to the right. We
    can start by checking the first 3 bits to see if it produces the last digit
    and recursively work on a solution from there.'''
    if depth == len(program):
        return current_a

    # Try all possible 3-bit numbers to put at the end of current_a
    for a_tail in range(8):
        a = (current_a << 3) | a_tail
        if check_program(program, a, 0, 0, depth):
            result = find_self_printing_a(program, a, depth + 1)
            if result is not None:
                return result
    
    # All possible tails have been checked, none worked
    return None

if __name__ == '__main__':
    program, a, b, c = get_data()

    # Solve part 1
    output = run_program(program, a, b, c)
    print(','.join(map(str, output)))

    # Solve part 2
    a = find_self_printing_a(program)

    print(a)
