file = open('data/day1.txt').read().splitlines()

# Create a left and right list and add all numbers to them

leftList = []
rightList = []

for line in file:
    [left, right] = line.split()
    leftList.append(int(left))
    rightList.append(int(right))

# Sort the lists, so we can pair the smallest together

leftList.sort()
rightList.sort()

# Calculate the total difference between the pairs

total_difference = 0

for (left, right) in zip(leftList, rightList):
    total_difference += abs(left - right)

print(total_difference)

# Per number from the left list, count the occurrences in the right list
# to find the similarity of the left item. Add all together.

similarity_score = 0

for left in leftList:
    similarity_score += left * rightList.count(left)

print(similarity_score)
