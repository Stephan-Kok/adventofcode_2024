from datetime import datetime

time_start = datetime.now()

with open('day_5.input', 'r') as file:
    lines = file.readlines()

i = 0
rules: [(int, int)] = []
while len(lines[i]) == 6:
    x = int(lines[i][0:2])
    y = int(lines[i][3:5])
    rules.append((x,y))
    i += 1
# Skip next line
i+= 1

def part1():
    # Validate pages
    valid_pages = []
    for j in range(i, len(lines)):
        page = list(map(int,lines[j].split(",")))
        if valid_page(page):
            valid_pages.append(page)
        else:
            invalid_pages.append(page)

    # print(valid_pages)
    print(sum([page[int(len(page) / 2)] for page in valid_pages]))

def valid_page(page):
    for (first, second) in rules:
        if first in page and second in page:
            if page.index(first) > page.index(second):
                return False
    return True

invalid_pages: [[int]] = []
part1()

def part2():
    fixed_pages = []
    for page in invalid_pages:
        fixed_page = reorder_page(page)
        fixed_pages.append(fixed_page)
    # print(fixed_pages)
    print(sum([page[int(len(page) / 2)] for page in fixed_pages]))

def reorder_page(page: [int]):
    error = False
    for (first, second) in rules:
        if first in page and second in page:
            if page.index(first) > page.index(second):
                page.remove(second)
                page.append(second)
                error = True
    if error:
        reorder_page(page)
    return page
part2()

time_end = datetime.now()
print("Total time: ", time_end - time_start)
