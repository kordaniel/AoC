from typing import Callable, List, NamedTuple, Set

def filemap(filename: str, func: Callable = int, sep: str = '\n') -> List:
    with open(filename, 'r') as f:
        return list(map(func, f.read().strip().split(sep)))

class Point2D(NamedTuple):
    x: int
    y: int

test_input = [
    '7,1',
    '11,1',
    '11,7',
    '9,7',
    '9,5',
    '2,5',
    '2,3',
    '7,3'
]

def print_grid(red_coords, green_coords = []):
    grid = [['.' for _ in range(14)] for _ in range(9)]

    for coords in red_coords:
        grid[coords[1]][coords[0]] = '#'

    for row in grid:
        print(''.join(row))
    print()

    for coords in green_coords:
        x, y = coords
        if grid[y][x] != '.':
            continue
        grid[y][x] = 'X'

    for row in grid:
        print(''.join(row))

def compute_rect_size(a: Point2D, b: Point2D) -> int:
    return (abs(b[0] - a[0]) + 1) * (abs(b[1] - a[1]) + 1)

def prob1(red_tiles_coords: List[Point2D]) -> int:
    grid_max_size = 0

    for i in range(0, len(red_tiles_coords)):
        for j in range(i+1, len(red_tiles_coords)):
            grid_max_size = max(grid_max_size, compute_rect_size(red_tiles_coords[i], red_tiles_coords[j]))

    return grid_max_size

def compute_polygon_boundaries_coords(red_tiles_coords: List[Point2D]) -> Set[Point2D]:
    green_tiles_coords = set()

    for i in range(len(red_tiles_coords)):
        prev = red_tiles_coords[i]
        next = red_tiles_coords[((i+1) % len(red_tiles_coords))]

        if prev.x == next.x:
            for y in range(min(prev.y, next.y), max(prev.y, next.y)+1):
                green_tiles_coords.add(Point2D(prev.x, y))
        elif prev.y == next.y:
            for x in range(min(prev.x, next.x), max(prev.x, next.x)+1):
                green_tiles_coords.add(Point2D(x, prev.y))
        else:
            print('Invalid input on line:', i)

    return green_tiles_coords

def prob2(red_tiles_coords: List[Point2D]) -> int:
    max_rect_size = 0
    green_tiles_poly_bounds = compute_polygon_boundaries_coords(red_tiles_coords)
    #print_grid(red_tiles_coords, green_tiles_poly_bounds)

    def rect_is_inside_polygon(a: Point2D, b: Point2D) -> bool:
        x_min = min(a[0], b[0])
        x_max = max(a[0], b[0])
        y_min = min(a[1], b[1])
        y_max = max(a[1], b[1])
        count = 0

        for g_x, g_y in green_tiles_poly_bounds:
                if x_min < g_x < x_max and y_min < g_y < y_max:
                    return False

        for corner_coords in ((x_min, y_min), (x_min, y_max), (x_max, y_min), (x_max, y_max)):
            if corner_coords in green_tiles_poly_bounds:
                count += 1

        return count != 4

    for i in range(0, len(red_tiles_coords)):
        for j in range(i+1, len(red_tiles_coords)):
            rect_size = compute_rect_size(red_tiles_coords[i], red_tiles_coords[j])
            if rect_size <= max_rect_size:
                continue
            if not rect_is_inside_polygon(red_tiles_coords[i], red_tiles_coords[j]):
                continue
            max_rect_size = rect_size

    return max_rect_size

def main():
    line_parser = lambda l: Point2D(*map(int, l.split(',')))
    input = filemap('input.txt', line_parser) if True else list(map(line_parser, test_input))

    prob1_res = prob1(input)
    prob1_res = f'{prob1_res} ({"Correct" if prob1_res == 4748826374 or prob1_res == 50 else "Wrong, correct = 4748826374"})'
    print('Prob1:', prob1_res)

    prob2_res = prob2(input)
    prob2_res =f'{prob2_res} ({"Correct" if prob2_res == 1554370486 or prob2_res == 24 else "Wrong, correct = 1554370486"})'
    print('Prob2:', prob2_res)

if __name__ == '__main__':
    main()
