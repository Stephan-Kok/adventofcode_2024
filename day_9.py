from datetime import datetime

time_start = datetime.now()

with open('day_9.input', 'r') as file:
    lines = file.readlines()

def get_disk():
    disk = []
    counter = 0
    for i in range(0, len(lines[0]) - 2, 2):
        disk += [counter for v in range(int(lines[0][i]))]
        counter += 1
        disk += ["." for v in range(int(lines[0][i + 1]))]
    disk += [counter for v in range(int(lines[0][-2]))]
    return disk

def part1(disk):
    total = 0
    counter = 0
    pos = -1
    # result = ""
    for i in range(len(disk)):
        if i - pos > len(disk):
            break

        v = disk[i]
        if isinstance(v, int):
            total += v * counter
            # result += str(v)
        else:
            total += disk[pos] * counter
            # result += str(disk[pos])
            pos -= 1
            while not isinstance(disk[pos], int):
                pos -= 1
        counter += 1
    # print(result)
    # print(counter)
    return total

# returns Tuple[id, size, is_free_space]
def get_tuple_disk():
    disk: [tuple[str, int, bool]] = []
    counter = 0
    for i in range(0, len(lines[0]) - 2, 2):
        disk.append((counter, int(lines[0][i]), False))
        counter += 1
        disk.append((".", int(lines[0][i + 1]), True))
    disk.append((counter, int(lines[0][-2]), False))
    return disk


def attempt_swap(tuple_size, tuple_id, index, tuple_disk):
    # Find free space before the index of the current tuple
    for i in range(index):
        _, tmp_tuple_size, tmp_tuple_free = tuple_disk[i]
        if tmp_tuple_free and tmp_tuple_size >= tuple_size:
            if tmp_tuple_size == tuple_size:
                # Equal swap
                tuple_disk[index] = (".", tuple_size, True)
                tuple_disk[i] = (tuple_id, tuple_size, False)
                return False
            else:
                # there will be leftover free space
                tuple_disk[i] = (".", tmp_tuple_size - tuple_size, True)
                tuple_disk[index] = (".", tuple_size, True)
                tuple_disk.insert(i, (tuple_id, tuple_size, False))
                return True

    return False

def part2():
    tuple_disk = get_tuple_disk()
    reverse_disk = tuple_disk.copy()
    reverse_disk.reverse()

    array_size = len(reverse_disk)
    max_diff = 0
    for i in range(array_size):
        id, size, is_free = reverse_disk[i]
        if is_free:
            continue

        # Index keeps changing since adding new lists
        cutoff = array_size - i - max_diff - 3 if array_size - i - max_diff - 3 > 0 else 0
        index = tuple_disk.index((id, size, is_free), cutoff)
        if attempt_swap(size, id, index, tuple_disk):
            max_diff += 1

    # Done just calculate hash
    total = 0
    counter = 0
    for id, size, free in tuple_disk:
        if (free):
            counter += size
        else:
            for i in range(size):
                total += id * counter
                counter += 1
    return total

r1 = part1(get_disk())
print("Part1", r1)
print("part1 time: ", datetime.now() - time_start)
r2 = part2()
print("Part2", r2)

time_end = datetime.now()
print("Total time: ", time_end - time_start)
