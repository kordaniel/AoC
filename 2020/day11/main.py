import sys
sys.path.insert(0, '..')

from helpers import filemap, DIRECTIONS

def is_in_bounds(y, x, y_len, x_len):
    return 0 <= y < y_len and \
            0 <= x < x_len

# Part 1 rules
def p1_requirements(model, y, x, y_len, x_len):
    '''
    Adjacent seats only.
    '''
    neighbours = 8
    adj_neighbr = {True: 0, False: 0}

    for coords in DIRECTIONS.values():
        dy = y + coords[0]
        dx = x + coords[1]

        if not is_in_bounds(dy, dx, y_len, x_len):
            neighbours -= 1
            continue

        if model[dy][dx] is None:
            neighbours -= 1
            continue

        adj_neighbr[model[dy][dx]] += 1

    return (model[y][x] and adj_neighbr[True] > 3) or \
            (not model[y][x] and adj_neighbr[False] == neighbours)


# Part 2 rules
def p2_requirements(model, y, x, y_len, x_len):
    '''
    All seats in the row.
    '''
    rows = {True: 0, False: 0} # Sum of all seats in all 8 directions,
                               # True is taken, false empty
    for direction in DIRECTIONS.values():
        dy = y
        dx = x
        while True:
            dy += direction[0]
            dx += direction[1]
            if not is_in_bounds(dy, dx, y_len, x_len):
                rows[False] += 1
                break
            if model[dy][dx] is None:
                continue

            rows[model[dy][dx]] += 1
            break

    return (model[y][x] and rows[True] > 4) or \
            (not model[y][x] and rows[False] == 8)


def predict(model, handle_coord):
    '''
    Simulate the process of people picking their seats based on the rules
    by the function handle_coord. "Predict" the final equilibriant situation.
    '''
    MAX_ITERATIONS = 200
    i = 0

    # Dont alter the original map.
    model = list(map(lambda y: [mapper(c) for c in y], model))
    y_len, x_len = len(model), len(model[0])
    coords = [-1] # Cords of seats to be flipped based on handle_coord result

    while coords:
        i += 1
        if i > MAX_ITERATIONS:
            raise Exception('Infinite loop in prediction?')

        coords = list()

        for y in range(y_len):
            for x in range(x_len):
                if model[y][x] is None: continue
                if handle_coord(model, y, x, y_len, x_len):
                    coords.append((y, x))

        for y, x in coords:
            model[y][x] = not model[y][x]

    return model


def map_as_str(model):
    return '\n'.join((''.join(r) for r in model))

def count_occurences(model, seat_type = True):
    '''Counts the occurences of seat_type in the 2d map'''
    return len([c for y in model for c in y if c == seat_type])

def mapper(c):
    '''
    Maps the seats and empty floor coords into True/False or None
    '''
    if c == '.': return None        # Empty space
    if c == 'L': return False       # Empty seat = False
    if c == '#': return True        # Taken seat = True
    raise Exception('BAD INPutTTT')

def mapper_reverse(c):
    if c is None: return '.'
    return '#' if c else 'L'

def main():
    #  Testing data
    data = [
        'L.LL.LL.LL',
        'LLLLLLL.LL',
        'L.L.L..L..',
        'LLLL.LL.LL',
        'L.LL.LL.LL',
        'L.LLLLL.LL',
        '..L.L.....',
        'LLLLLLLLLL',
        'L.LLLLLL.L',
        'L.LLLLL.LL'
    ]

    data = list(map(lambda r: [c for c in r], data))

    # Actual data
    data = filemap('input.txt', lambda r: [c for c in r])

    data_p1 = predict(data, p1_requirements)
    data_p2 = predict(data, p2_requirements)

    #print('Map for P1:')
    #print(map_as_str(map(lambda y: [mapper_reverse(x) for x in y], data_p1)))

    #print()
    #print('Map for P2:')
    #print(map_as_str(map(lambda y: [mapper_reverse(x) for x in y], data_p2)))

    print('P1 occupied seats:', count_occurences(data_p1))
    print('P2 occupied seats:', count_occurences(data_p2))


if __name__ == '__main__':
    main()
