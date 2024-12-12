from datetime import datetime

time_start = datetime.now()

with open('day_12.input', 'r') as file:
    lines = file.readlines()

# This class defines a side for part2
class Side:
    start: tuple[int,int]
    end: tuple[int,int]

    def __init__(self, start_x, start_y, end_x, end_y):
        self.start = (start_x, start_y)
        self.end = (end_x, end_y)
        if start_x - end_x == 0:
            self.direction = "v"
        elif start_y - end_y == 0:
            self.direction = "h"
        else:
            raise ValueError("Cannot happen")

    def add_side(self, new_side):
        if self.direction == new_side.direction:
            if self.start == new_side.end:
                self.start = new_side.start
                return True
            if self.end == new_side.start:
                self.end = new_side.end
                return True
        return False

    def __repr__(self):
        return self.direction + ":" + str(self.start) + ":" + str(self.end)

class GardenGroup:
    garden: [[tuple[str, bool]]]
    height: int
    width: int

    def __init__(self):
        self.garden = []
        for line in lines:
            self.garden.append([(plant, False) for plant in line[:-1]])
        self.height = len(self.garden)
        self.width = len(self.garden[0])

    def find_plant(self, plant: str, x: int, y: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            tmp_plant, is_found = self.garden[y][x]
            if tmp_plant == plant:
                return x, y, is_found
        return None

    def get_plants_near(self, plant: str, x: int, y: int):
        found = [
            (self.find_plant(plant, x + 1, y), "r"),
            (self.find_plant(plant, x, y + 1), "d"),
            (self.find_plant(plant, x - 1, y), "l"),
            (self.find_plant(plant, x, y - 1), "u")
        ]
        return [(item, direction) for item, direction in found if item is not None]


    def find_plant_area(self, plant: str, x: int, y: int):
        if self.garden[y][x][1]:
            return 0, 0
        self.garden[y][x] = (plant, True)
        plants = self.get_plants_near(plant, x, y)
        area = 4 - len(plants)
        count = 1
        for (xpos, ypos, is_found), direction in plants:
            if not is_found:
                new_area, new_count = self.find_plant_area(plant, xpos, ypos)
                area += new_area
                count += new_count
        return area, count

    def find_garden_area(self):
        plants_area = []
        for y in range(self.height):
            for x in range(self.width):
                plant, is_found = self.garden[y][x]
                if not is_found:
                    plants_area.append(((plant, x,y), self.find_plant_area(plant, x, y)))
        # print(plants_area)
        return sum([area * occurrence for (plant, (area, occurrence)) in plants_area])

    def find_plant_side(self, plant: str, x: int, y: int):
        # Skip if plant already done
        if self.garden[y][x][1]:
            return [], 0

        # Set plant done
        self.garden[y][x] = (plant, True)

        # Get plants near
        plants_near = self.get_plants_near(plant, x, y)
        plants, direction = [plant for plant, _ in plants_near], [direction for _, direction in plants_near]

        # Only add sides where no plant is near
        sides = []
        if "r" not in direction:
            sides.append(Side(x + 1, y, x + 1, y + 1))
        if "d" not in direction:
            sides.append(Side(x + 1, y + 1, x, y + 1))
        if "l" not in direction:
            sides.append(Side(x, y + 1, x, y))
        if "u" not in direction:
            sides.append(Side(x, y, x + 1, y))

        # Recursive do all near plants to find total space
        count = 1
        for xpos, ypos, is_found in plants:
            if not is_found:
                new_sides, new_count = self.find_plant_side(plant, xpos, ypos)
                for new_side in new_sides:
                    if not self.add_side_if_already_exists(sides, new_side):
                        sides.append(new_side)
                count += new_count
        return sides, count

    def add_side_if_already_exists(self, sides: [Side], new_side: Side):
        for side in sides:
            if side.add_side(new_side):
                return True
        return False

    def find_garden_sides(self):
        plant_sides = []
        for y in range(self.height):
            for x in range(self.width):
                plant, is_found = self.garden[y][x]
                if not is_found:
                    plant_sides.append(((plant, x,y), self.find_plant_side(plant, x, y)))
        # print(plant_sides)
        return sum([len(sides) * occurrence for (plant, (sides, occurrence)) in plant_sides])


garden_group = GardenGroup()
print("Part1", garden_group.find_garden_area())
garden_group = GardenGroup()
print("Part2", garden_group.find_garden_sides())

print("Total time: ", datetime.now() - time_start)


