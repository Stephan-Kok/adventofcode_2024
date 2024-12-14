from datetime import datetime

time_start = datetime.now()

with open('day_8.input', 'r') as file:
    lines = file.readlines()

antennas = {}
for y in range(len(lines)):
    for x in range(len(lines[0]) - 1):
        val = lines[y][x]
        if val != ".":
            if val in antennas:
                antennas[val].append((x,y))
            else:
                antennas[val] = [(x,y)]
# print("Keys", antennas.keys())

# ######## PART 1
def add_combination(x, y, array):
    if 0 <= x < len(lines[0]) - 1 and 0 <= y < len(lines):
        array.append((x, y))

combinations = []
for key, value in antennas.items():
    for i in range(len(value)):
        for j in range(i + 1, len(value)):
            x1, y1 = value[i]
            x2, y2 = value[j]
            dx = x1 - x2
            dy = y1 - y2
            add_combination(x1 + dx, y1 + dy, combinations)
            add_combination(x2 - dx, y2 - dy, combinations)
# print("Combinations:", combinations)

matrix = []
for line in lines:
    matrix.append(list(line))

count = 0
for x,y in combinations:
    if  matrix[y][x] != "#":
        count += 1
        matrix[y][x] = "#"

# for row in matrix:
#     print(" ".join(map(str, row[:-1])))
# print("Total part1", count)


# ######## PART 2
def add_resonate_combination(x, y, array, dx, dy):
    while 0 <= x < len(lines[0]) - 1 and 0 <= y < len(lines):
        array.append((x, y))
        x += dx
        y += dy

new_combinations = []
for key, value in antennas.items():
    for i in range(len(value)):
        for j in range(i + 1, len(value)):
            x1, y1 = value[i]
            x2, y2 = value[j]
            dx = x1 - x2
            dy = y1 - y2
            add_resonate_combination(x1 + dx, y1 + dy, new_combinations, dx, dy)
            add_resonate_combination(x2 - dx, y2 - dy, new_combinations, -dx, -dy)

matrix = []
for line in lines:
    matrix.append(list(line))

# exclude all antennas and add later
count = 0
for x,y in new_combinations:
    if matrix[y][x] == ".":
        count += 1
        matrix[y][x] = "#"

# for row in matrix:
#     print(" ".join(map(str, row[:-1])))

print("Total part1", count)
print("Total part2", count + sum([len(sublist) for sublist in antennas.values()]))

time_end = datetime.now()
print("Total time: ", time_end - time_start)
