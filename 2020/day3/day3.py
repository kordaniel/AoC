import sys
sys.path.insert(0, '..')

from helpers import filemap
from functools import reduce

def travel(map, dy, dx):
    ''' Travels the map with dx and dy steps and counts how many trees are
        encountered amongst the route.
    '''
    y_max, x_max = len(map), len(map[0])
    x = 0
    trees = 0

    for y in range(0, y_max, dy):
        if map[y][x] == '#': #Tree
            trees += 1
        x = (x + dx) % x_max

    return trees

def travel_many(map, jumps = ((1, 3), )):
    ''' Travels the map with all slopes specified in the argument jumps and
        multiplies all the encountered trees from the different routes.
        jumps argument is a tuple containing tuples with
        (y_movement, x_movement) in coords.
    '''
    return reduce(lambda x, y: x * y,
                    [travel(map, dir[0], dir[1]) for dir in jumps])


def main():
    data = filemap('input.txt', lambda s: s)
    print('Part1:', travel_many(data))
    print('Part2:', travel_many(data, ((1, 1), (1, 3), (1, 5), (1, 7), (2, 1))))


if __name__ == '__main__':
    main()
