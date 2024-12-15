from datetime import datetime
import numpy as np
import re

time_start = datetime.now()

with open('day_14.input', 'r') as file:
    lines = file.readlines()

print("Total time: ", datetime.now() - time_start)


class RestroomRedoubt:
    NUMBER_REGEX = r"[+\-0-9]+"

    def __init__(self):
        self.width = 101
        self.height = 103
        # self.width = 11
        # self.height = 7

        self.robots = []
        for line in lines:
            numbers = re.findall(self.NUMBER_REGEX, line)
            # (px, py), (vx, vy)
            self.robots.append(((int(numbers[0]), int(numbers[1])), (int(numbers[2]), int(numbers[3]))))

    def move(self, steps):
        new_robots = []
        for (px, py), (vx, vy) in self.robots:
            px = (px + (vx * steps)) % self.width
            py = (py + (vy * steps)) % self.height
            new_robots.append(((px, py), (vx, vy)))
        self.robots = new_robots

    def count(self):
        q1, q2, q3, q4 = 0, 0, 0, 0
        for (px, py), (vx, vy) in self.robots:
            if px == self.width // 2 or py == self.height // 2:
                continue
            if px < self.width // 2 and py < self.height // 2:
                q1 += 1
            if px > self.width // 2 and py < self.height // 2:
                q2 += 1
            if px < self.width // 2 and py > self.height // 2:
                q3 += 1
            if px > self.width // 2 and py > self.height // 2:
                q4 += 1
        print(q1, q2, q3, q4)
        return q1 * q2 * q3 * q4

    def print(self):
        restroom = self.get_matrix()
        for line in restroom:
            print_line = ""
            for v in line:
                if v == 0:
                    print_line += " ."
                else:
                    print_line += " " + str(v)
            print(print_line)

    def get_matrix(self):
        restroom = [[0 for x in range(self.width)] for y in range(self.height)]
        for (px, py), (vx, vy) in self.robots:
            restroom[py][px] += 1
        return restroom

    def make_tree(self):
        tree = []
        tree_height = (self.height // 5) * 4
        middle_height = self.height // 2
        for y in range(self.height):
            line = []
            if (y < 80):
                cutoff = int(self.width / 2 * (y / 80.0))
                for x in range(0, (self.width // 2) - cutoff):
                    line.append(0)
                for x in range((self.width // 2) - cutoff, (self.width // 2) + cutoff):
                    line.append(1)
                for x in range((self.width // 2) + cutoff, self.width):
                    line.append(0)
            else:
                for x in range(0, (self.width // 2) - 4):
                    line.append(0)
                for x in range((self.width // 2) - 4, (self.width // 2) + 4):
                    line.append(1)
                for x in range((self.width // 2) + 4, self.width):
                    line.append(0)

            tree.append(line)
        return tree

def fancy_print(matrix):
    for line in matrix:
        print_line = ""
        for v in line:
            if v == 0:
                print_line += " ."
            else:
                print_line += " " + str(v)
        print(print_line)

# restroom = RestroomRedoubt()
# fancy_print(restroom.make_tree())
# exit()


# restroom = RestroomRedoubt()
# print(restroom.robots)
# restroom.print()
# print("New")
# restroom.move(100)
# restroom.print()
# print("part1", restroom.count())

# with open('tree.txt', 'r') as file:
#     tree = file.readlines()

def compare_matrices(matrix1, matrix2):
    # Ensure matrices are the same size
    if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
        print("matrix1", len(matrix1), len(matrix1[0]))
        print("matrix2", len(matrix2), len(matrix2[0]))
        raise ValueError("Matrices are not the same size.")

    total_elements = len(matrix1) * len(matrix1[0])
    matching_elements = 0

    for i in range(len(matrix1)):
        for j in range(len(matrix1[i])):
            if matrix1[i][j] == matrix2[i][j]:
                matching_elements += 1

    match_percentage = (matching_elements / total_elements) * 100
    return match_percentage

restroom = RestroomRedoubt()
restroom.move(7858)
fancy_print(restroom.get_matrix())

with open('tree.txt', 'r') as file:
    tree = file.readlines()

tree = [[int(v) for v in line[:-1]] for line in tree]

# Compare matrices
restroom = RestroomRedoubt()
# tree = restroom.make_tree()
highest = 0
count = 0
while True:
    count += 1
    restroom.move(1)
    match_percentage = compare_matrices(restroom.get_matrix(), tree)
    if match_percentage > highest:
        highest = match_percentage
        print("New highest", highest, count)

    # if match_percentage > 80:
    #     fancy_print(restroom.get_matrix())
    #     print(f"The matrices match by {match_percentage:.2f}%.")



# import os
# import time
#
# def clear_screen():
#     # Check the operating system and execute the appropriate command
#     if os.name == 'nt':  # For Windows
#         os.system('cls')
#     else:  # For Unix/Linux/MacOS
#         os.system('clear')

# Example usage
# restroom = RestroomRedoubt()
# restroom.move(20)
# steps = 0
# while True:
#     restroom.move(1)
#     clear_screen()
#     print(steps)
#     restroom.print()
#     steps+= 1
#     time.sleep(0.1)
#     # if steps % 10 == 0:
#     #     time.sleep(0.2)


print("Total time: ", datetime.now() - time_start)
