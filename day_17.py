import re
from datetime import datetime

time_start = datetime.now()

with open('day_17.input', 'r') as file:
    lines = file.readlines()

class Program:
    NUMBER_REGEX = r"[0-9]+"
    a: int
    b: int
    c: int
    program: [int]

    def __init__(self):
        self.a = int(re.findall(self.NUMBER_REGEX,lines[0])[0])
        self.b = int(re.findall(self.NUMBER_REGEX,lines[1])[0])
        self.c = int(re.findall(self.NUMBER_REGEX,lines[2])[0])
        self.program = [int(v) for v in re.findall(self.NUMBER_REGEX, lines[4])]
        self.out = []

    def get_combo_operand(self, value: int):
        if 0 <= value <= 3:
            return value
        if value == 4:
            return self.a
        if value == 5:
            return self.b
        if value == 6:
            return self.c
        raise ValueError("Value " + str(value) + " should not appear in program")

    def execute_instruction_with_operant(self, instruction: int, operant: int):
        if instruction == 0:
            self.a = self.a // (2 ** self.get_combo_operand(operant))
            return None
        if instruction == 1:
            self.b = self.b ^ operant
            return None
        if instruction == 2:
            self.b = self.get_combo_operand(operant) % 8
            return None
        if instruction == 3:
            if self.a == 0:
                return None
            return operant
        if instruction == 4:
            self.b = self.b ^ self.c
            return
        if instruction == 5:
            self.out.append(self.get_combo_operand(operant) % 8)
            return
        if instruction == 6:
            self.b = self.a // (2 ** self.get_combo_operand(operant))
            return
        if instruction == 7:
            self.c = self.a // (2 ** self.get_combo_operand(operant))
            return

    def fancy_print(self):
        print("Register A:", self.a)
        print("Register B:", self.b)
        print("Register C:", self.c)
        print("Program:", self.program)
        print("Out:", self.out)

    def execute_program(self):
        i = 0
        while i < len(self.program):
            result = self.execute_instruction_with_operant(self.program[i], self.program[i + 1])
            if result is not None:
                i = result
            else:
                i += 2
                
    def test_for_value_a(self, a):
        self.out = []
        self.a = a
        self.b = 0
        self.c = 0
        self.execute_program()
        return self

    def find_a(self):
        a = 0
        self.test_for_value_a(a)
        # Start with matching only the last one and then continue left
        index = -1
        solutions = [a]

        # After writing out the program you will see that for each a // 8 != 0 you will get a new character in the output
        while True:
            solutions_so_far = []
            # For each possible solution
            for a_val in solutions:
                # There are only 8 possible options because of the % 8
                for i in range(0,8):
                    # We want to check the next index so we have to multiply the last answer by 8 to get the new output character
                    a_to_test = a_val * 8 + i
                    self.test_for_value_a(a_to_test)

                    # Done exit
                    if self.out == self.program:
                        return a_to_test

                    # If the output matches with the current amount of indexes in the program we are matching
                    if self.out == self.program[index:]:
                        solutions_so_far.append(a_to_test)
            # All these solutions are will give the program from end till index
            solutions = solutions_so_far
            index -= 1



program = Program()
# program.fancy_print()
program.execute_program()
# program.fancy_print()
print("part1", "".join([str(v)+"," for v in program.out[:-1]])+str(program.out[-1]))
result = program.find_a()
program.fancy_print()
print("part2", result)

print("Total time: ", datetime.now() - time_start)
#Total time:  0:00:00.011822

