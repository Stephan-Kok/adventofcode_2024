from datetime import datetime
import numpy as np
import re

time_start = datetime.now()

with open('day_13.input', 'r') as file:
    lines = file.readlines()

class ClawMachine:
    NUMBER_REGEX = r"[0-9]+"

    def __init__(self, part2 = False):
        self.machines = []
        for i in range(0, len(lines), 4):
            button_a = re.findall(self.NUMBER_REGEX, lines[i])
            button_b = re.findall(self.NUMBER_REGEX, lines[i + 1])
            prize = re.findall(self.NUMBER_REGEX, lines[i + 2])
            if part2:
                machine = (int(button_a[0]), int(button_b[0]), 10000000000000 + int(prize[0])), (int(button_a[1]), int(button_b[1]), 10000000000000 + int(prize[1]))
            else:
                machine = (int(button_a[0]), int(button_b[0]), int(prize[0])), (int(button_a[1]), int(button_b[1]), int(prize[1]))
            self.machines.append(machine)
    # ax * c1 + bx * c2 = px
    # ay * c1 + by * c2 = py
    # This can be solved using linear algebra
    # Example: https://www.mathcentre.ac.uk/resources/Engineering%20maths%20first%20aid%20kit/latexsource%20and%20diagrams/5_6.pdf
    def find_solutions(self):
        solutions = []
        for (ax, bx, px), (ay, by, py) in self.machines:
            A = np.array([[ax, bx],
                          [ay, by]])
            B = np.array([px, py])
            # Solving for c1 and c2
            solution = np.linalg.solve(A, B)
            c1, c2 = solution

            c1_int = int(c1.round())
            c2_int = int(c2.round())
            if ax * int(c1_int) + bx * int(c2_int) == px and ay * int(c1_int) + by * int(c2_int) == py:
                solutions.append(c1_int*3 + c2_int)
        return sum(solutions)


claw_machine = ClawMachine()
print("Part1", claw_machine.find_solutions())
claw_machine = ClawMachine(True)
print("Part2", claw_machine.find_solutions())

print("Total time: ", datetime.now() - time_start)


