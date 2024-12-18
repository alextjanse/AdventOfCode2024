def get_data() -> tuple[int, int, int, list[int]]:
    with open('data/day17.txt', encoding='utf-8') as file:
        lines = file.read().splitlines()
        a = int(lines[0].split(': ')[1])
        b = int(lines[1].split(': ')[1])
        c = int(lines[2].split(': ')[1])

        program = [int(i) for i in lines[4].split(': ')[1].split(',')]
    
    return a, b, c, program

def get_combo_operand(operand, a, b, c) -> int:
    if operand <= 3: return operand
    if operand == 4: return a
    if operand == 5: return b
    if operand == 6: return c
    
    raise Exception("Unknown operand")

def run_program(a, b, c, program) -> list[int]:
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

def solve_part_1() -> None:
    output = run_program(*get_data())

    print(','.join(map(str, output)))

def run_and_check_program(a, b, c, program) -> bool:
    pointer = 0
    output = []
    
    while pointer < len(program):
        try:
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

                if program[len(output)] != x:
                    return False
                
                output.append(x)
            elif opcode == 6: # bdv
                b = a // (2**get_combo_operand(operand, a, b, c))
            elif opcode == 7: # cdv
                c = a // (2**get_combo_operand(operand, a, b, c))
            else:
                raise Exception("Unknown instruction")

            pointer += 2
        except:
            return False
    
    return len(output) == len(program)

def solve_part_2():
    _, b, c, program = get_data()

    a = 8**(len(program) - 1)
    while not run_and_check_program(a, b, c, program):
        a += 1
    
    print(a)

if __name__ == '__main__':
    solve_part_1()
    solve_part_2()
