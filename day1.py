file = open('data/day1.txt').read().splitlines()

leftList = []
rightList = []

for line in file:
    [left, right] = line.split()
    leftList.append(int(left))
    rightList.append(int(right))

leftList.sort()
rightList.sort()

total_difference = 0

for (left, right) in zip(leftList, rightList):
    total_difference += abs(left - right)

print(total_difference)

similarity_score = 0

for left in leftList:
    similarity_score += left * rightList.count(left)

print(similarity_score)