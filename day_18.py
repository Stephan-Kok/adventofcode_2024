import re
import time
from datetime import datetime
import copy
from typing import Tuple, Optional

time_start = datetime.now()


with open('day_18.input', 'r') as file:
    lines = file.readlines()

walls = {}
NUMBER_REGEX = r"[0-9]+"
Node = Tuple[Tuple[int, int], Optional['Node']]

def fill_walls_with(byte_drop: int, memory_space: int):
    walls.clear()
    for i in range(byte_drop):
        numbers = re.findall(NUMBER_REGEX, lines[i])
        walls[(int(numbers[0]), int(numbers[1]))] = True

    # Add area around memory_space0
    for x in range(-1, memory_space + 1):
        walls[(x, -1)] = True
        walls[(x, memory_space + 1)] = True
    for y in range(-1, memory_space + 1):
        walls[(-1, y)] = True
        walls[(memory_space + 1, y)] = True

class RamRun:
    linked_path_list: Node

    def __init__(self, end):
        self.pos = 0,0
        self.end = end, end
        self.steps = 0
        self.linked_path_list = ((0,0), None)

    def escape(self):
        ram_runs = [self]
        path = {self.pos: True}
        while len(ram_runs) != 0:
            new_ram_runs = []
            for ram_run in ram_runs:
                moves = ram_run.get_moves()
                for x, y in moves:

                    # Skip if wall
                    if (x, y) in walls:
                        continue
                    if (x, y) in path:
                        continue

                    new_ram_run = copy.copy(ram_run)
                    new_ram_run.pos = (x, y)
                    new_ram_run.steps += 1
                    new_ram_run.linked_path_list = (new_ram_run.pos, new_ram_run.linked_path_list)
                    path[new_ram_run.pos] = True
                    if new_ram_run.pos == new_ram_run.end:
                        return new_ram_run
                    new_ram_runs.append(new_ram_run)
            ram_runs = new_ram_runs
        return None

    def get_moves(self):
        x, y = self.pos
        return [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)
        ]
def get_nodes(node: Node):
    result = []
    (value, prev_node) = node
    while prev_node is not None:
        result.append(value)
        (value, prev_node) = prev_node
    result.append(value)
    return result

def fancy_print(ram_run: RamRun):
    node_path = get_nodes(ram_run.linked_path_list)
    for y in range(memory_space_size + 1):
        line = ""
        for x in range(memory_space_size + 1):
            if (x, y) in walls:
                line += "#"
                continue
            if (x, y) == ram_run.pos:
                line += "H"
                continue
            if (x, y) == ram_run.end:
                line += "E"
                continue
            if (x, y) in node_path:
                line += "O"
                continue
            line += "."
        print(line)
# Part1
bytes_corrupted_memory_space = 1024
memory_space_size = 70
fill_walls_with(bytes_corrupted_memory_space, memory_space_size)
ram_run = RamRun(memory_space_size)
fancy_print(ram_run)
result = ram_run.escape()
print()
fancy_print(result)
print("Part1", result.steps)

def binary_search(arr):
    left, right = 0, len(arr) - 1
    final = None
    while left != right:
        mid = left + (right - left) // 2
        result = test_memory(arr[mid])

        if result is None:
            # search left
            right = mid - 1
            final = mid
        else:
            # search right
            left = mid + 1
            final = mid
    # When the results meet we found the first cuttoff
    return arr[final]

def test_memory(i):
    bytes_corrupted_memory_space = i
    memory_space_size = 70
    fill_walls_with(bytes_corrupted_memory_space, memory_space_size)
    ram_run = RamRun(memory_space_size)
    return ram_run.escape()

# Part2
problem_space = [i for i in range(1025, len(lines))]
part2_index = binary_search(problem_space)
print("Part2", lines[part2_index])


# Without binary search
# for i in range(1025, len(lines)):
#     bytes_corrupted_memory_space = i
#     memory_space_size = 70
#     fill_walls_with(bytes_corrupted_memory_space, memory_space_size)
#     ram_run = RamRun(memory_space_size)
#     result = ram_run.escape()
#     if result is None:
#         print("Part2", lines[i - 1])
#         break

print("Total time: ", datetime.now() - time_start)
#Total time:  0:00:00.067605

