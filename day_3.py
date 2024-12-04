import re
from datetime import datetime

time_start = datetime.now()

with open('day_3.input', 'r') as file:
    lines = file.readlines()

total_lines = "".join(lines)

mul_pattern = r"mul\([0-9]+,[0-9]+\)"
number_pattern = r"[0-9]+"

def part1():
    muls = re.findall(mul_pattern, total_lines).__str__()
    numbers = re.findall(number_pattern, muls)
    total = 0
    for i in range(0, len(numbers), 2):
        total += int(numbers[i]) * int(numbers[i+1])
    print(total)

def remove_parts(line):
    start = line.find("don't()")
    while start != -1:
        rest = line[start:]
        end = rest.find("do()")
        if end == -1:
            return line[:start]
        line = line[:start] + rest[end+4:]
        start = line.find("don't()")
    return line

def part2():
    fixed = remove_parts(total_lines)
    muls = re.findall(mul_pattern, fixed).__str__()
    numbers = re.findall(number_pattern, muls)
    total = 0
    for i in range(0, len(numbers), 2):
        total += int(numbers[i]) * int(numbers[i+1])
    print(total)

part1()
part2()

time_end = datetime.now()
print("Total time: ", time_end - time_start)
