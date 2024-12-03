with open('day_2.input', 'r') as file:
    lines = file.readlines()

def increase_check(level):
    for i in range(1, len(level)):
        if level[i] == level[i - 1] + 1:
            continue
        elif level[i] == level[i - 1] + 2:
            continue
        elif level[i] == level[i - 1] + 3:
            continue
        return False
    return True

def decrease_check(level):
    for i in range(1, len(level)):
        if level[i] == level[i - 1] - 1:
            continue
        elif level[i] == level[i - 1] - 2:
            continue
        elif level[i] == level[i - 1] - 3:
            continue
        return False
    return True

def part1():
    total = 0
    for line in lines:
        level = [int(i) for i in line.split(" ")]
        increase = level[0] < level[1]
        if increase:
            result = increase_check(level)
        else:
            result = decrease_check(level)

        print(level, result)
        if result:
            total += 1
    print(total)


def increase_check2(level):
    counter = 0
    for i in range(1, len(level)):
        if level[i] == level[i - 1] + 1:
            continue
        elif level[i] == level[i - 1] + 2:
            continue
        elif level[i] == level[i - 1] + 3:
            continue

        counter += 1
        if counter > 1:
            return False
    return True

def decrease_check2(level):
    counter = 0
    for i in range(1, len(level)):
        if level[i] == level[i - 1] - 1:
            continue
        elif level[i] == level[i - 1] - 2:
            continue
        elif level[i] == level[i - 1] - 3:
            continue

        counter += 1
        if counter > 1:
            return False
    return True

def part2():
    total = 0
    for line in lines:
        level = [int(i) for i in line.split(" ")]
        increase = level[0] < level[1]
        if increase:
            result = increase_check2(level)
        else:
            result = decrease_check2(level)

        print(level, result)
        if result:
            total += 1
    print(total)
part2()
