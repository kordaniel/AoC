with open('input.txt', 'r') as f:
    lines = f.read().splitlines()

def travel(map, dx = 3, dy = 1):
    # Part one
    y_max, x_max = len(map), len(map[0])
    y, x = 0, 0
    trees = 0
    while y < y_max:
        if map[y][x] == '#': #Tree
            trees += 1
        x = (x+dx) % x_max
        y += dy

    return trees

def travel_many(map):
    # Part 2
    # (y_movement, x_movement) in coords
    jumps = ((1,1), (3,1), (5,1), (7,1), (1,2))
    trees_total = 1

    for directions in jumps:
        trees_total *= travel(map, directions[0], directions[1])

    return trees_total

print(travel(lines))
print(travel_many(lines))
