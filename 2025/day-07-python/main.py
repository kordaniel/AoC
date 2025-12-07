import copy
from enum import Enum
from typing import Callable, Dict, List, Tuple

def filemap(filename: str, func: Callable = int, sep: str = '\n') -> List:
    with open(filename, 'r') as f:
        return list(map(func, f.read().strip().split(sep)))

test_input = [
    '.......S.......',
    '...............',
    '.......^.......',
    '...............',
    '......^.^......',
    '...............',
    '.....^.^.^.....',
    '...............',
    '....^.^...^....',
    '...............',
    '...^.^...^.^...',
    '...............',
    '..^...^.....^..',
    '...............',
    '.^.^.^.^.^...^.',
    '...............'
]

CellEnum = Enum('Cell', 'BEAM EMPTY SPLITTER START')
CELL_ENUM_MAP = {
    '.': CellEnum.EMPTY,
    CellEnum.EMPTY: '.',
    '^': CellEnum.SPLITTER,
    CellEnum.SPLITTER: '^',
    'S': CellEnum.START,
    CellEnum.START: 'S',
    '|': CellEnum.BEAM,
    CellEnum.BEAM: '|'
}

def print_grid(grid: List[List[CellEnum]]):
    for row in grid:
        print(''.join(CELL_ENUM_MAP[x] for x in row))

def parse_input_line(line: str):
    try:
        return [CELL_ENUM_MAP[c] for c in line]
    except Exception as e:
        print("Encountered not supported character in input:", e)
        return []

def prob1(grid: List[List[CellEnum]]) -> int:
    tot_splits_count = 0
    for x in range(len(grid[0])):
        if grid[0][x] == CellEnum.START:
            grid[1][x] = CellEnum.BEAM

    for y in range(len(grid)-1):
        for x in range(len(grid[y])):
            if grid[y][x] == CellEnum.BEAM:
                if grid[y+1][x] == CellEnum.SPLITTER:
                    tot_splits_count += 1
                    if x > 0 and grid[y+1][x-1] == CellEnum.EMPTY:
                        grid[y+1][x-1] = CellEnum.BEAM
                    if x < len(grid[y+1])-1 and grid[y+1][x+1] == CellEnum.EMPTY:
                        grid[y+1][x+1] = CellEnum.BEAM
                else:
                    grid[y+1][x] = CellEnum.BEAM

    return tot_splits_count

def prob2(grid: List[List[CellEnum]], pos: Tuple[int, int], cache: Dict[Tuple[int, int], int]) -> int:
    if pos in cache:
        return cache[pos]

    y, x = pos

    if y == len(grid) - 1:
        return 1

    tot = 0
    if grid[y][x] == CellEnum.EMPTY or grid[y][x] == CellEnum.START:
        tot = prob2(grid, (y+1, x), cache)
    elif grid[y][x] == CellEnum.SPLITTER:
        if x > 0:
            tot += prob2(grid, (y, x-1), cache)
        if x < len(grid[y]) - 1:
            tot += prob2(grid, (y, x+1), cache)

    cache[pos] = tot
    return tot

def main():
    input = filemap('input.txt', parse_input_line) if True else list(map(parse_input_line, test_input))

    prob1_res = prob1(copy.deepcopy(input))
    prob1_res = f'{prob1_res} ({"Correct" if prob1_res == 1672 else "Wrong, correct = 1672"})'
    print('Prob1:', prob1_res)

    prob2_res = prob2(input, (0, input[0].index(CellEnum.START)), dict())
    prob2_res =f'{prob2_res} ({"Correct" if prob2_res == 231229866702355 else "Wrong, correct = 231229866702355"})'
    print('Prob2:', prob2_res)

if __name__ == '__main__':
    main()
