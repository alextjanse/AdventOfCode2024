from itertools import groupby

def get_data() -> list[int | None]:
    '''Read the data and put it in a list. Each entry contains the
    id of the file or either None if the register is empty.'''
    file = open('data/day9.txt').read().rstrip()
    disk = []

    number = True
    id = 0

    for c in file:
        i = int(c)
        
        if number:
            disk += [id] * i
            id += 1
        else:
            disk += [None] * i
        
        number = not number
    
    return disk[:]

def solve_part_1(disk: list[int | None]) -> int:
    '''Solve part one by following to index, one from the start and
    one from the end. If the start location is empty, fill it with the
    file at the end location.'''
    index = 0
    end_index = len(disk) - 1

    while index < end_index:
        if disk[index] is not None:
            index += 1
        elif disk[end_index] is None:
            end_index -= 1
        else:
            disk[index] = disk[end_index]
            disk[end_index] = None

    return check_sum(disk)

def check_sum(disk: list[int | None]) -> int:
    '''Calculate the check sum of the disk.'''
    result = 0

    for i, v in enumerate(disk):
        if v is not None:
            result += i * v
    
    return result

def solve_part_2(disk: list[int | None]) -> int:
    '''Solve part two by brute force. For each item, check if there is
    space at the beginning and fill it if possible. Takes quite some time,
    but whatever.'''

    files = { key: len(list(group)) for key, group in groupby(filter(lambda x: x is not None, disk)) }
    
    max_id = len(files) - 1

    for file_id in range(max_id, -1, -1):
        size = files[file_id]

        for i, v in enumerate(disk):
            if v == file_id:
                # We have struck the current file location
                break
            elif all(map(lambda d: d is None, disk[i: i + size])):
                # Remove the file from its original location
                disk = [None if d == file_id else d for d in disk]
                
                # Place the file at the new location
                for j in range(i, i + size):
                    disk[j] = file_id
                
                break

    return check_sum(disk)

if __name__ == '__main__':
    data = get_data()
    
    print(solve_part_1(data))

    data = get_data()

    print(solve_part_2(data))
