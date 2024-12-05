from datetime import datetime

time_start = datetime.now()

with open('day_4.input', 'r') as file:
    matrix = file.readlines()

width = len(matrix[0])
height = len(matrix)
word = ['X', 'M', 'A', 'S']

mark = [["." for j in range(width - 1)] for i in range(height)]


def traverse_top(x, y, dept):
    if check_bounds(x, y):
        return False
    if matrix[y][x] == word[dept]:
        if dept == len(word) - 1:
            # mark[y][x] = "S"
            return True
        return traverse_top(x, y - 1, dept + 1)
    return False

def traverse_top_right(x, y, dept):
    if check_bounds(x, y):
        return False
    if matrix[y][x] == word[dept]:
        if dept == len(word) - 1:
            # mark[y][x] = "S"
            return True
        return traverse_top_right(x + 1, y - 1, dept + 1)
    return False

def traverse_right(x, y, dept):
    if check_bounds(x, y):
        return False
    if matrix[y][x] == word[dept]:
        if dept == len(word) - 1:
            # mark[y][x] = "S"
            return True
        return traverse_right(x + 1, y, dept + 1)
    return False

def traverse_bottem_right(x, y, dept):
    if check_bounds(x, y):
        return False
    if matrix[y][x] == word[dept]:
        if dept == len(word) - 1:
            # mark[y][x] = "S"
            return True
        return traverse_bottem_right(x + 1, y + 1, dept + 1)
    return False

def traverse_bottem(x, y, dept):
    if check_bounds(x, y):
        return False
    if matrix[y][x] == word[dept]:
        if dept == len(word) - 1:
            # mark[y][x] = "S"
            return True
        return traverse_bottem(x, y + 1, dept + 1)
    return False

def traverse_bottem_left(x, y, dept):
    if check_bounds(x, y):
        return False
    if matrix[y][x] == word[dept]:
        if dept == len(word) - 1:
            # mark[y][x] = "S"
            return True
        return traverse_bottem_left(x - 1, y + 1, dept + 1)
    return False

def traverse_left(x, y, dept):
    if check_bounds(x, y):
        return False
    if matrix[y][x] == word[dept]:
        if dept == len(word) - 1:
            # mark[y][x] = "S"
            return True
        return traverse_left(x - 1, y, dept + 1)
    return False

def traverse_top_left(x, y, dept):
    if check_bounds(x, y):
        return False
    if matrix[y][x] == word[dept]:
        if dept == len(word) - 1:
            # mark[y][x] = "S"
            return True
        return traverse_top_left(x - 1, y - 1, dept + 1)
    return False

def check_bounds(x, y):
    return x < 0 or x > width - 1 or y < 0 or y > height - 1


def part1():
    total = 0
    for y in range(height):
        for x in range(width):
            # Search in all 8 directions
            if traverse_top(x, y, 0):
                total += 1
            if traverse_top_right(x, y, 0):
                total += 1
            if traverse_right(x, y, 0):
                total += 1
            if traverse_bottem_right(x, y, 0):
                total += 1
            if traverse_bottem(x, y, 0):
                total += 1
            if traverse_bottem_left(x, y, 0):
                total += 1
            if traverse_left(x, y, 0):
                total += 1
            if traverse_top_left(x, y, 0):
                total += 1
    print(total)

part1()

# print(matrix)

def search_x_mas(x, y):
    if matrix[y - 1][x - 1] == "M":
        if matrix[y - 1][x + 1] == "M":
            return matrix[y + 1][x + 1] == "S" and matrix[y + 1][x - 1] == "S"
        if matrix[y + 1][x - 1] == "M":
            return matrix[y + 1][x + 1] == "S" and matrix[y - 1][x + 1] == "S"
        return False
    if matrix[y - 1][x - 1] == "S":
        if matrix[y - 1][x + 1] == "S":
            return matrix[y + 1][x + 1] == "M" and matrix[y + 1][x - 1] == "M"
        if matrix[y + 1][x - 1] == "S":
            return matrix[y + 1][x + 1] == "M" and matrix[y - 1][x + 1] == "M"
        return False
    return False

def part2():
    total = 0
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if matrix[y][x] == "A":
                if search_x_mas(x, y):
                    total += 1

    print(total)

part2()
#
# for row in mark:
#     print(" ".join(map(str, row)))




time_end = datetime.now()
print("Total time: ", time_end - time_start)
