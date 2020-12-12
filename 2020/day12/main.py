import sys
sys.path.insert(0, '..')

from helpers import filemap

def calculate_endpoint_manhattan_distance(nav_instructions):
    ''' Calculates the manhattan distance from start to where the ship
        ends up when navigating according to Part 1 nav_instructions
    '''
    direction = 90
    y, x = 0, 0
    directions = {
        # Dictionary containing functions for moving the ferry
        # forward in the current direction.
        0:   lambda d, v, y, x: (d, (y - v), x),
        90:  lambda d, v, y, x: (d, y, (x + v)),
        180: lambda d, v, y, x: (d, (y + v), x),
        270: lambda d, v, y, x: (d, y, (x - v))
    }
    handle_instruction = {
        # Dictionary containing the functions to rotate and move
        # the ferry in NSEW directions.
        'N': lambda d, v, y, x: (d, y - v, x),
        'S': lambda d, v, y, x: (d, y + v, x),
        'E': lambda d, v, y, x: (d, y, x + v),
        'W': lambda d, v, y, x: (d, y, x - v),
        'L': lambda d, v, y, x: ((d - v) % 360, y, x),
        'R': lambda d, v, y, x: ((d + v) % 360, y, x),
        'F': directions
    }

    for action, val in nav_instructions:
        func = handle_instruction[action]
        if not callable(func):
            # Key must be 'F' and we need to get the correct lambda lambda
            # function from the inner dict
            func = func[direction]
        direction, y, x = func(direction, val, y, x)

    return abs(x) + abs(y)

def calc_waypoint_manhattan_distance(nav_instructions):
    ''' Calculates the manhattan distance from start to where the ship
        ends up when navigating according to Part 2 nav_instructions
    '''
    wp_y, wp_x = -1, 10 # Waypoint coords in relation to the ship
    y, x = 0, 0
    handle_instruction = {
        'N': lambda v, y, x, wp_y, wp_x: (y, x, wp_y - v, wp_x),
        'S': lambda v, y, x, wp_y, wp_x: (y, x, wp_y + v, wp_x),
        'E': lambda v, y, x, wp_y, wp_x: (y, x, wp_y, wp_x + v),
        'W': lambda v, y, x, wp_y, wp_x: (y, x, wp_y, wp_x - v),
        'F': lambda v, y, x, wp_y, wp_x: (y + v * wp_y, x + v * wp_x, wp_y, wp_x)
    }

    for action, val in nav_instructions:
        if action in handle_instruction:
            y, x, wp_y, wp_x = handle_instruction[action](val, y, x, wp_y, wp_x)
        elif action in 'LR':
            if val % 90 != 0:
                raise Exception('BAD INPUT, input angle is not 90 degrees!')
            if action == 'R':
                for _ in range(val // 90): # number of turns
                    wp_y, wp_x = wp_x, -wp_y
            elif action == 'L':
                turns = val / 90
                for _ in range(val // 90):
                    wp_y, wp_x = -wp_x, wp_y
        else:
            raise Exception('MISFORMED INPUT')

    return abs(y) + abs(x)


def main():
    # Test data
    #data = ['F10', 'N3', 'F7', 'R90', 'F11']
    #data = list(map(lambda s: (s[0], int(s[1:])), data))
    # Actual data
    data = filemap('input.txt', lambda s: (s[0], int(s[1:]) ) )

    print('Part1:', calculate_endpoint_manhattan_distance(data))
    print('Part2:', calc_waypoint_manhattan_distance(data))


if __name__ == '__main__':
    main()
