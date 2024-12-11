from datetime import datetime
from functools import lru_cache

time_start = datetime.now()

with open('day_11.input', 'r') as file:
    lines = file.readlines()

@lru_cache(maxsize=None)
def stone_blink_times(stone, blinks):
    stones = [stone]
    for blink in range(blinks):
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
                continue
            string = str(stone)
            size = len(string)
            if size % 2 == 0:
                new_stones.append(int(string[:size // 2]))
                new_stones.append(int(string[size // 2:]))
                continue
            new_stones.append(stone * 2024)
        stones = new_stones
    return stones

class PlutonianPebbles:
    def __init__(self):
        self.stones = [int(v) for v in lines[0][:-1].split(" ")]

    def blinks_75_times(self):
        stones = self.stones
        dic = {}
        for blink in range(75 // 5):
            tmp_dic = {}
            for stone in stones:
                dict_count = 1
                if stone in dic:
                    dict_count = dic[stone]
                resulting_stones = stone_blink_times(stone, 5)
                for key in resulting_stones:
                    if key in tmp_dic:
                        tmp_dic[key] += dict_count
                    else:
                        tmp_dic[key] = dict_count
            if blink == 25 // 5:
                print("part1", sum(dic.values()))
            dic = tmp_dic
            stones = dic.keys()
        print("part2", sum(dic.values()))

PlutonianPebbles().blinks_75_times()

print("Total time: ", datetime.now() - time_start)
print(stone_blink_times.cache_info())
