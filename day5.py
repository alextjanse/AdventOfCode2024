from collections import defaultdict

# Split the file by the ordering rules and update procedures
[ordering_rules, update_procedures] = [s.splitlines() for s in open('data/day5.txt').read().split('\n\n')]

# Create a dictionary that stores for each successor which predecessors it could have.
# We are going to use this dictionary to check if a given number has predecessors and
# if they have passed already. If so, the procedure is invalid.
predecessor_rules = defaultdict(set)

for rule in ordering_rules:
    [pred, succ] = [int(s) for s in rule.split('|')]
    
    predecessor_rules[succ].add(pred)

def check_procedure(procedure: list[int]) -> bool:
    '''Check if the given procedure follows the procedure rules.'''
    global predecessor_rules
    
    # A set with the successors that are invalid according to the rules.
    invalid_successors = set()
    
    # Go through all pages
    for page in procedure:
        # Check wether the page is a valid successor
        if page in invalid_successors:
            return False
        
        # Add the pages that are predecessors in the rules for this page
        # to the invalid successors
        invalid_successors.update(predecessor_rules[page])
    
    return True

middle_sum = 0

# Store the invalid procedures for part two
invalid_procedures = list()

# Check all procedures
for line in update_procedures:
    procedure = [int(s) for s in line.split(',')]

    if check_procedure(procedure):
        middle_sum += procedure[len(procedure) // 2]
    else:
        invalid_procedures.append(procedure)

print(middle_sum)

def fix_procedure_iterate(procedure: list[int]) -> bool:
    '''Check if a procedure is valid. If not, swap the invalid successor
    with the predecessor it clashes with and return False. Return true if the
    procedure is valid.'''
    global predecessor_rules

    # Store the indices of the first occurrence of a predecessor in the predecessor rules
    invalid_successors = dict()

    for (index, page) in enumerate(procedure):
        if page in invalid_successors:
            # Invalid procedure. Swap the successor and predecessor.
            swap_index = invalid_successors[page]
            swap_value = procedure[swap_index]
            procedure[swap_index] = page
            procedure[index] = swap_value

            return False

        # Add the predecessors to the invalid successor dictionary if it's their first occurrence
        for pred in predecessor_rules[page]:
            if pred not in invalid_successors:
                invalid_successors[pred] = index

    # All rules are met, procedure is valid
    return True

def fix_procedure(procedure: list[int]) -> None:
    # Keep iterating over the procedure until it's valid
    while not fix_procedure_iterate(procedure):
        pass

middle_sum = 0

for procedure in invalid_procedures:
    fix_procedure(procedure)

    middle_sum += procedure[len(procedure) // 2]

print(middle_sum)
