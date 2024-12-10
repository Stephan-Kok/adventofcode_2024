from datetime import datetime

time_start = datetime.now()

with open('day_10.input', 'r') as file:
    lines = file.readlines()

class Trail:
    def __init__(self):
        self.matrix = []
        self.trailheads = []
        for y in range(len(lines)):
            line = []
            for x in range(len(lines[0]) - 1):
                value = int(lines[y][x])
                if value == 0:
                    self.trailheads.append((x,y))
                line.append(value)
            self.matrix.append(line)

        self.height = len(self.matrix)
        self.width = len(self.matrix[0])

    def print(self):
        for line in self.matrix:
            print(line)

        print(self.trailheads)

    def get_value(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.matrix[y][x]
        return None

    def next_steps(self, x , y):
        return [(self.get_value(x - 1, y), x - 1, y),
                (self.get_value(x, y - 1), x, y - 1),
                (self.get_value(x + 1, y), x + 1, y),
                (self.get_value(x, y + 1), x, y + 1)]

    def find_trail(self, x, y, trails, dept):
        if dept == 9:
            if (x, y) in trails:
                trails[(x,y)] += 1
            else:
                trails[(x,y)] = 1
            return

        steps = self.next_steps(x, y)
        for value, posx, posy in steps:
            if value == dept + 1:
                self.find_trail(posx, posy, trails, dept + 1)
        return

    def walk(self):
        part1_total = 0
        part2_total = 0
        for x, y in self.trailheads:
            trails = {}
            self.find_trail(x, y, trails, 0)
            # print("Trails", trails)
            part1_total += len(trails.keys())
            part2_total += sum([trails[key] for key in trails.keys()])
        return part1_total, part2_total
trail = Trail()
# print(trail.print())
part1, part2 = trail.walk()
print("Part1", part1)
print("Part2", part2)

print("Total time: ", datetime.now() - time_start)
