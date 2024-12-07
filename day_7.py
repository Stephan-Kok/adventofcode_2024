from datetime import datetime
import re
import operator

time_start = datetime.now()

with open('day_7.input', 'r') as file:
    lines = file.readlines()

data = []
number_pattern = r"^[0-9]+"
for line in lines:
    result = re.match(number_pattern, line).group(0)
    total = int(result)
    numbers = [int(v) for v in line[len(result) + 2:].split(" ")]
    data.append((total, numbers))

def get_combinations(array_a, b, operators: [operator]):
    return [fun(a,b) for fun in operators for a in array_a]


result = 0
operators = [operator.add, operator.mul]
for total, numbers in data:
    problem_space = len(numbers) ** len(operators)

    prev = [numbers[0]]
    for i in range(1, len(numbers)):
        next = numbers[i]
        prev = get_combinations(prev, next, operators)

    if total in prev:
        result += total

print("Part1", result)

def concatenation(a, b):
    return int(str(a)+str(b))

result = 0
operators = [operator.add, operator.mul, concatenation]
for total, numbers in data:
    problem_space = len(numbers) ** len(operators)

    prev = [numbers[0]]
    for i in range(1, len(numbers)):
        next = numbers[i]
        prev = get_combinations(prev, next, operators)

    if total in prev:
        result += total

print("part2", result)

time_end = datetime.now()
print("Total time: ", time_end - time_start)
