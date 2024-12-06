from datetime import datetime
import multiprocessing
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

class Guard:
    direction = Direction.UP
    x: int
    y: int
    matrix: [[str]]
    object_count: dict # Loop counter hack

    def __init__(self, x, y, matrix):
        self.x = x
        self.y = y
        self.matrix = matrix
        self.object_count = {}

    def walk(self):
        (x, y) = self.next_move()
        obstruction = self.check_obstructions(x, y)
        while obstruction != Obstructions.FREE:
            while obstruction == Obstructions.OBJECT:
                self.change_direction()
                (x, y) = self.next_move()
                obstruction = self.check_obstructions(x, y)
            self.move(x, y)
            (x, y) = self.next_move()
            obstruction = self.check_obstructions(x, y)
        self.matrix[self.y][self.x] = "X"
        # print("Motherfucker free")

    def move(self, x, y):
        self.matrix[self.y][self.x] = "X"
        self.matrix[y][x] = "^"
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

    def check_obstructions(self, pos_x: int, pos_y: int):
        if pos_x < 0 or pos_x > width - 1 or pos_y < 0 or pos_y > height - 1:
            return Obstructions.FREE
        if self.matrix[pos_y][pos_x] == ".":
            return Obstructions.OPEN
        if self.matrix[pos_y][pos_x] == "#":
            # Loop counter hack for part2
            index = "X:" + str(pos_x) + "Y:" + str(pos_y)
            self.object_count[index] = self.object_count.get(index, 0) + 1
            if self.object_count[index] > 5:
                raise ValueError("PossibleLoopEncountered")
            return Obstructions.OBJECT
        if self.matrix[pos_y][pos_x] == "X":
            return Obstructions.OPEN
        return None

# part1
guard = Guard(start_x, start_y, matrix)
guard.walk()
print(sum([line.count("X") for line in guard.matrix]))

# part2
# This part is dependable on part1!

# Only usefull to place objects where we actually walked
walked_paths = []
for i in range(height):
    for j in range(width):
        if guard.matrix[i][j] == "X":
            walked_paths.append((j, i))

def part2(mark_x, mark_y):
    # Reset matrix and place new object
    matrix = []
    for line in lines:
        matrix.append(list(line))
    matrix[mark_y][mark_x] = "#"

    # Escape and log if loop found
    guard = Guard(start_x, start_y, matrix)
    try:
        guard.walk()
    except ValueError as e:
        if e.args[0] == "PossibleLoopEncountered":
            return True
        else:
            print(e)
    return False

def collect_result(result):
    if (result):
        results.append(result)

if __name__ == '__main__':
    with multiprocessing.Manager() as manager:
        # Shared list to collect results
        results = manager.list()

        with multiprocessing.Pool(processes=8) as pool:
            for mark_x, mark_y in walked_paths:
                pool.apply_async(part2, args=(mark_x, mark_y), callback=collect_result)

            pool.close()
            pool.join()

        # Summing all results
        print("Total loops:", len(results))

time_end = datetime.now()
print("Total time: ", time_end - time_start)
