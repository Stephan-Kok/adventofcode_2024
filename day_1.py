with open('day_1.input', 'r') as file:
    lines = file.readlines()
list1 = []
list2 = []
for line in lines:
    split = line.split("  ")
    list1.append(int(split[0]))
    list2.append(int(split[1]))

def part1():
    list1.sort()
    list2.sort()
    print(sum([abs(list1[i] - list2[i]) for i in range (len(list1))]))

def part2():
    print(sum([list1[i]*list2.count(list1[i]) for i in range(len(list1))]))

part1()
part2()
