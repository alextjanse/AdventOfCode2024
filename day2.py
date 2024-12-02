file = open('data/day2.txt').read().splitlines()

reports = [[int(i) for i in level.split()] for level in file]

def check_validity(report):
    asc = 1 if report[1] - report[0] > 0 else -1

    for (fst, snd) in zip(report[:-1], report[1:]):
        diff = (snd - fst) * asc
        if not(1 <= diff and diff <= 3):
            return False
    return True

safe_reports = 0

for report in reports:
    if check_validity(report):
        safe_reports += 1

print(safe_reports)

def check_tolerances(report):
    if check_validity(report): return True

    for i in range(len(report)):
        if check_validity(report[:i] + report[i+1:]): return True
    
    return False

safe_reports = 0

for report in reports:
    if check_tolerances(report): safe_reports += 1

print(safe_reports)