from datetime import datetime
from enum import Enum

time_start = datetime.now()

with open('day_15.input', 'r') as file:
    lines = file.readlines()

class Direction(Enum):
    UP = "^"
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"

class Warehouse:
    robot: (int, int)
    boxes: [(int, int)]
    walls: [(int, int)]
    moves: [Direction]

    def __init__(self, part2 = False):
        self.boxes = []
        self.walls = []
        i = 0
        while len(lines[i]) != 1:
            for x in range(len(lines[i])):
                if lines[i][x] == "@":
                    if part2:
                        self.robot = x * 2, i
                    else:
                        self.robot = x, i
                if lines[i][x] == "O":
                    if part2:
                        self.boxes.append((x * 2, i))
                        # self.boxes.append((x * 2 + 1, i))
                    else:
                        self.boxes.append((x, i))
                if lines[i][x] == "#":
                    if part2:
                        self.walls.append((x * 2, i))
                        self.walls.append((x * 2 + 1, i))
                    else:
                        self.walls.append((x, i))
            i += 1
        self.height = i
        self.width = len(lines[i - 1]) - 1

        self.moves = []
        for i in range(i, len(lines)):
            self.moves += [Direction(v) for v in lines[i][:-1]]

    def has_box(self, x, y):
        if (x, y) in self.boxes:
            return True
        return False

    def has_wall(self, x, y):
        if (x, y) in self.walls:
            return True
        return False

    def get_step(self, direction, x, y):
        if direction == Direction.UP:
            return x, y - 1
        if direction == Direction.RIGHT:
            return x + 1, y
        if direction == Direction.DOWN:
            return x, y + 1
        if direction == Direction.LEFT:
            return x - 1, y

    def move(self):
        for direction in self.moves:
            x, y  = self.robot
            new_x, new_y = self.get_step(direction, x, y)

            tmp_x, tmp_y = new_x, new_y
            if self.has_wall(tmp_x, tmp_y):
                continue

            box_found = False
            while self.has_box(tmp_x, tmp_y):
                box_found = True
                tmp_x, tmp_y = self.get_step(direction, tmp_x, tmp_y)

            if self.has_wall(tmp_x, tmp_y):
                continue

            # No wall and no box
            self.robot = new_x, new_y
            if box_found:
                self.boxes.remove((new_x, new_y))
                self.boxes.insert(0,(tmp_x, tmp_y))

    def getGPS(self):
        total = 0
        for x, y in self.boxes:
            total += 100 * y + x
        return total

    def has_box2(self, x, y):
        if (x, y) in self.boxes:
            return True, x, y
        if (x - 1, y) in self.boxes:
            return True, x - 1, y
        return False, None, None

    def has_wall2(self, x, y):
        if (x, y) in self.walls:
            return True
        return False

    def move2(self):
        for direction in self.moves:
            # clear_screen()
            # self.fancy_print2()

            x, y  = self.robot
            new_x, new_y = self.get_step(direction, x, y)

            tmp_x, tmp_y = new_x, new_y
            if self.has_wall2(tmp_x, tmp_y):
                continue

            has_box, box_x, box_y = self.has_box2(tmp_x, tmp_y)
            boxes = [(box_x, box_y)]

            # Check for other boxes that boxes hit
            if has_box and self.recursive_box_check(boxes, direction):
                continue

            # No wall and no box
            self.robot = new_x, new_y
            if has_box:
                for box_x, box_y in boxes:
                    self.boxes.remove((box_x, box_y))
                    self.boxes.append(self.get_step(direction, box_x, box_y))

    def recursive_box_check(self, boxes, direction):
        for box_x, box_y in boxes:
            tmp_x, tmp_y = self.get_step(direction, box_x, box_y)

            if self.has_wall2(tmp_x, tmp_y):
                return True
            has_box, new_box_x, new_box_y = self.has_box2(tmp_x, tmp_y)
            if has_box and (new_box_x, new_box_y) not in boxes:
                boxes.append((new_box_x, new_box_y))

            tmp_x, tmp_y = self.get_step(direction, box_x + 1, box_y)
            if self.has_wall2(tmp_x, tmp_y):
                return True
            has_box, new_box_x, new_box_y = self.has_box2(tmp_x, tmp_y)
            if has_box and (new_box_x, new_box_y) not in boxes:
                boxes.append((new_box_x, new_box_y))
        return False


    def fancy_print(self):
        matrix = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                if y == 0 or y == self.height or x == 0 or x == self.width:
                    line.append("#")
                    continue
                if self.has_box(x, y):
                    line.append("0")
                    continue
                if self.has_wall(x, y):
                    line.append("#")
                    continue
                line.append(".")
            matrix.append(line)
        matrix[self.robot[1]][self.robot[0]] = "@"

        for line in matrix:
            v = ""
            for l in line:
                v += l
            print(v)

    def fancy_print2(self):
        matrix = []
        for y in range(self.height):
            line = []
            x = -1
            while (len(line) < self.width * 2):
                x += 1
                if y == 0 or y == self.height or x == 0 or x == self.width * 2:
                    line.append("#")
                    continue
                if self.has_box(x, y):
                    line.append("[")
                    line.append("]")
                    x += 1
                    continue
                if self.has_wall(x, y):
                    line.append("#")
                    continue
                line.append(".")
            matrix.append(line)
        matrix[self.robot[1]][self.robot[0]] = "@"

        for line in matrix:
            v = ""
            for l in line:
                v += l
            print(v)


warehouse = Warehouse()
warehouse.fancy_print()
print("Before")
warehouse.move()
print("after")
warehouse.fancy_print()
print("part1", warehouse.getGPS())


warehouse2 = Warehouse(True)
print("Before")
warehouse2.fancy_print2()
warehouse2.move2()
print("after")
warehouse2.fancy_print2()

print("part1", warehouse.getGPS())
print("part2", warehouse2.getGPS())

print("Total time: ", datetime.now() - time_start)
