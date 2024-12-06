from datetime import datetime
from enum import Enum

time_start = datetime.now()

with open('day_6.input', 'r') as file:
    lines = file.readlines()

# Generate matrix
matrix = []
for line in lines:
    matrix.append(list(line))

# Find start
height = len(matrix)
width = len(matrix[0])
for i in range(height):
    for j in range(width):
        if matrix[i][j] == '^':
            start_x = j
            start_y = i
            print("Found guard at: ", j , i)
            break

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Obstructions(Enum):
    OPEN = 0
    OBJECT = 1
    FREE = 2


object_count = {} # Loop counter hack
def check_obstructions(pos_x: int, pos_y: int):
    if pos_x < 0 or pos_x > width - 1 or pos_y < 0 or pos_y > height - 1:
        return Obstructions.FREE
    if matrix[pos_y][pos_x] == ".":
        return Obstructions.OPEN
    if matrix[pos_y][pos_x] == "#":
        # Loop counter hack for part2
        index = "X:" + str(pos_x) + "Y:" + str(pos_y)
        object_count[index] = object_count.get(index, 0) + 1
        if object_count[index] > 5:
            raise ValueError("PossibleLoopEncountered")
        return Obstructions.OBJECT
    if matrix[pos_y][pos_x] == "X":
        return Obstructions.OPEN
    return None


class Guard:
    direction = Direction.UP
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def walk(self):
        (x, y) = self.next_move()
        obstruction = check_obstructions(x, y)
        while obstruction != Obstructions.FREE:
            while obstruction == Obstructions.OBJECT:
                self.change_direction()
                (x, y) = self.next_move()
                obstruction = check_obstructions(x, y)
            self.move(x, y)
            (x, y) = self.next_move()
            obstruction = check_obstructions(x, y)
        matrix[self.y][self.x] = "X"
        # print("Motherfucker free")

    def move(self, x, y):
        matrix[self.y][self.x] = "X"
        matrix[y][x] = "^"
        self.x = x
        self.y = y

    def next_move(self):
        if self.direction == Direction.UP:
            return self.x, self.y - 1
        if self.direction == Direction.RIGHT:
            return self.x + 1, self.y
        if self.direction == Direction.DOWN:
            return self.x, self.y + 1
        if self.direction == Direction.LEFT:
            return self.x - 1, self.y
        return None

    def change_direction(self):
        self.direction = Direction((self.direction.value + 1) % 4)

# part1
guard = Guard(start_x, start_y)
guard.walk()
print(sum([line.count("X") for line in matrix]))

# part2
# This part is dependable on part1!

# Only usefull to place objects where we actually walked
walked_paths = []
for i in range(height):
    for j in range(width):
        if matrix[i][j] == "X":
            walked_paths.append((j, i))

total_loops = 0
for mark_x, mark_y in walked_paths:
    # Reset loop counter
    object_count = {}

    # Reset matrix and place new object
    matrix = []
    for line in lines:
        matrix.append(list(line))
    matrix[mark_y][mark_x] = "#"

    # Escape and log if loop found
    guard = Guard(start_x, start_y)
    try:
        guard.walk()
    except ValueError as e:
        if e.args[0] == "PossibleLoopEncountered":
            total_loops += 1
        else:
            print(e)
print("Total loops", total_loops)

# for row in matrix:
#     print("".join(map(str, row)))


time_end = datetime.now()
print("Total time: ", time_end - time_start)
