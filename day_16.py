import time
from datetime import datetime
from enum import Enum
import copy
from typing import Tuple, Optional

time_start = datetime.now()

with open('day_16.input', 'r') as file:
    lines = file.readlines()

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

walls = {}
path = {}
Node = Tuple[Tuple[int, int], Optional['Node']]

def get_nodes(node: Node):
    result = []
    (value, prev_node) = node
    while prev_node is not None:
        result.append(value)
        (value, prev_node) = prev_node
    result.append(value)
    return result


class ReindeerPosition:
    reindeer: (int, int)
    end: (int, int)
    points: int
    linked_path_list: Node
    direction: Direction

    def __init__(self):
        self.points = 0
        self.direction = Direction.RIGHT
        self.height = len(lines)
        # self.path = []
        self.width = len(lines[0]) - 1
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or x == self.width or y == 0 or y == self.height:
                    walls[(x, y)] = True
                if lines[y][x] == "#":
                    walls[(x, y)] = True
                if lines[y][x] == "S":
                    self.reindeer = (x, y)
                if lines[y][x] == "E":
                    self.end = (x, y)

    def fancy_print(self):
        path = get_nodes(self.linked_path_list)

        for y in range(self.height):
            line = ""
            for x in range(self.width):
                if (x, y) in walls:
                    line += "#"
                    continue
                if (x, y) == self.reindeer:
                    line += "S"
                    continue
                if (x, y) == self.end:
                    line += "E"
                    continue
                if (x, y) in path:
                    line += '\033[93m' + "*" + '\033[0m'
                    continue
                line += "."
            print(line)

    def get_moves(self):
        x, y = self.reindeer
        if self.direction == Direction.UP:
            return [
                (x, y - 1, Direction.UP, 1),
                (x + 1, y, Direction.RIGHT, 1001),
                (x - 1, y, Direction.LEFT, 1001),
            ]
        if self.direction == Direction.RIGHT:
            return [
                (x + 1, y, Direction.RIGHT, 1),
                (x, y + 1, Direction.DOWN, 1001),
                (x, y - 1, Direction.UP, 1001),
            ]
        if self.direction == Direction.DOWN:
            return [
                (x, y + 1, Direction.DOWN, 1),
                (x - 1, y, Direction.LEFT, 1001),
                (x + 1, y, Direction.RIGHT, 1001),
            ]
        if self.direction == Direction.LEFT:
            return [
                (x - 1, y, Direction.LEFT, 1),
                (x, y - 1, Direction.UP, 1001),
                (x, y + 1, Direction.DOWN, 1001),
            ]
        return None

    def escape(self):
        mazes = [self]
        best = None
        finishers = []
        # self.path.append(self.reindeer)
        self.linked_path_list = (self.reindeer, None)
        while len(mazes) != 0:
            new_mazes = []
            for maze in mazes:
                moves = maze.get_moves()
                for x, y, direction, cost in moves:
                    # Skip if wall
                    if (x, y) in walls:
                        continue

                    # Skip if already visited with lower cost
                    previous_cost = path.get((x,y))
                    if previous_cost is not None:
                        if previous_cost < maze.points + cost:
                            # print(path[(x,y)], maze.points + cost)
                            # To find multiple paths of same cost it can be that one still has to turn
                            if previous_cost != maze.points + cost - 1000:
                                continue
                    else:
                        previous_cost = maze.points + cost
                    path[(x, y)] = min(previous_cost, maze.points + cost)

                    # make copy of reindeer position and add for next iteration
                    maze_copy = copy.copy(maze)
                    maze_copy.points += cost
                    maze_copy.reindeer = (x, y)
                    maze_copy.linked_path_list = ((x, y), maze_copy.linked_path_list)
                    maze_copy.direction = direction

                    # At the end of maze!
                    if maze_copy.reindeer == maze_copy.end:
                        finishers.append(maze_copy)
                        if best is None or best.points >= maze.points:
                            best = maze_copy
                            continue
                        else:
                            # This should no longer happen since we already skip higher cost paths
                            # This is back because of part2 adjustments
                            # print("Finished but worse", best.points, maze_copy.points)
                            continue
                    new_mazes.append(maze_copy)
            mazes = new_mazes
            # print("Step", len(mazes))
        return best, finishers

maze = ReindeerPosition()
# maze.fancy_print()
result, finishers = maze.escape()
result.fancy_print()
# print("part1", result.points)

seats = []
for finisher in finishers:
    if finisher.points != result.points:
        continue

    path = get_nodes(finisher.linked_path_list)
    for seat in path:
        if seat not in seats:
            seats.append(seat)

print("part1", result.points)
print("part2", len(seats))
print("Total time: ", datetime.now() - time_start)
# Total time:  0:03:24.122824
