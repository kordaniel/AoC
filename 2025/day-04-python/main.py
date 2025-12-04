from enum import Enum
from typing import List

class Cell(Enum):
    EMPTY = 0
    ROLL = 1

def filemap(filename, func = int, sep='\n'):
    with open(filename, 'r') as f:
        return list(map(func, f.read().strip().split(sep)))

test_input = [
    '..@@.@@@@.',
    '@@@.@.@.@@',
    '@@@@@.@.@@',
    '@.@@@@..@.',
    '@@.@@@@.@@',
    '.@@@@@@@.@',
    '.@.@.@.@@@',
    '@.@@@.@@@@',
    '.@@@@@@@@.',
    '@.@.@@@.@.'
]

def count_adjacent_rolls(grid: List[List[Cell]], y: int, x: int) -> int:
    rolls_cnt = 0
    for dy in range(max(0, y-1), min(len(grid), y+2)):
        for dx in range(max(0, x-1), min(len(grid[dy]), x+2)):
            if dy == y and dx == x:
                continue
            if grid[dy][dx] == Cell.ROLL:
                rolls_cnt += 1
    return rolls_cnt


def prob1(input: List[List[Cell]]) -> int:
    can_access_cnt = 0
    for y in range(len(input)):
        for x in range(len(input[y])):
            if input[y][x] == Cell.ROLL and count_adjacent_rolls(input, y, x) < 4:
                can_access_cnt += 1
    return can_access_cnt


def remove_roll(grid: List[List[int]], y: int, x: int):
    for dy in range(max(0, y-1), min(len(grid), y+2)):
        for dx in range(max(0, x-1), min(len(grid[dy]), x+2)):
            grid[dy][dx] = max(0, grid[dy][dx]-1)

def remove_all_rolls(grid: List[List[Cell]], neighbours_map: List[List[int]]) -> int:
    removed_rolls_cnt = 0
    done = False
    while not done:
        done = True
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == Cell.ROLL and neighbours_map[y][x] < 4:
                    grid[y][x] = Cell.EMPTY
                    remove_roll(neighbours_map, y, x)
                    removed_rolls_cnt += 1
                    done = False
    return removed_rolls_cnt

def prob2(input: List[List[Cell]]) -> int:
    adjacent_rolls_cnt_map = list()
    for y in range(len(input)):
        adjacent_rolls_cnt_map.append([])
        for x in range(len(input[y])):
            adjacent_rolls_cnt_map[y].append(count_adjacent_rolls(input, y, x))

    return remove_all_rolls(input, adjacent_rolls_cnt_map)

def main():
    line_parser = lambda l: list((Cell.ROLL if c == '@' else Cell.EMPTY for c in l))
    input = filemap('input.txt', line_parser) if True else list(map(line_parser, test_input))

    prob1_res = prob1(input)
    prob1_res = f'{prob1_res} ({"Correct" if prob1_res == 1411 else "Wrong, correct = 1411"})'
    print('Prob1:', prob1_res)

    prob2_res = prob2(input)
    prob2_res =f'{prob2_res} ({"Correct" if prob2_res == 8557 else "Wrong, correct = 8557"})'
    print('Prob2:', prob2_res)

if __name__ == '__main__':
    main()
