from collections import defaultdict

[ordering_rules, update_procedures] = [s.splitlines() for s in open('data/day5.txt').read().split('\n\n')]

predecessor_rules = defaultdict(set)

for rule in ordering_rules:
    [pred, succ] = [int(s) for s in rule.split('|')]
    
    predecessor_rules[succ].add(pred)

def check_update_procedure(procedure: list[int]) -> bool:
    global predecessor_rules
    
    invalid_successors = set()
    
    for page in procedure:
        if page in invalid_successors:
            return False
        invalid_successors.update(predecessor_rules[page])
    
    return True

middle_sum = 0

invalid_procedures = list()

for line in update_procedures:
    procedure = [int(s) for s in line.split(',')]

    if check_update_procedure(procedure):
        middle_sum += procedure[len(procedure) // 2]
    else:
        invalid_procedures.append(procedure)

print(middle_sum)

def fix_procedure(procedure: list[int]) -> None:
    global predecessor_rules

    invalid_successors = dict()

    for (index, page) in enumerate(procedure):
        if page in invalid_successors.keys():
