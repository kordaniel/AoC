import copy
from dataclasses import dataclass
from enum import Enum

from typing import Callable, List, Optional, Tuple

def filemap(filename: str, func: Callable = int, sep: str = '\n') -> List:
    with open(filename, 'r') as f:
        return list(map(func, f.read().strip().split(sep)))

test_input = [
    '0:',
    '###',
    '##.',
    '##.',
    '',
    '1:',
    '###',
    '##.',
    '.##',
    '',
    '2:',
    '.##',
    '###',
    '##.',
    '',
    '3:',
    '##.',
    '###',
    '##.',
    '',
    '4:',
    '###',
    '#..',
    '###',
    '',
    '5:',
    '###',
    '.#.',
    '###',
    '',
    '4x4: 0 0 0 0 2 0',
    '12x5: 1 0 1 0 2 2',
    '12x5: 1 0 1 0 3 2'
]

class Orientation(Enum):
    N = 0
    E = 1
    S = 2
    W = 3
    VF = 4
    HF = 5

class Shape:
    fill_i_val = 0

    def __init__(self, coords: List[str]):
        if any(len(coords) != len(row) for row in coords):
            print('Error: encountered a not square sized shape')

        self.__cells_cnt = sum(sum(1 if x == '#' else 0 for x in y) for y in coords)
        self.__side_len = len(coords)

        orientation_n = [[x == '#' for x in y] for y in coords]

        transpose = list(map(list, zip(*orientation_n)))
        flip_v = orientation_n[::-1]
        flip_h = [row[::-1] for row in orientation_n]

        orientation_e = [row[::-1] for row in transpose]
        orientation_s = [[x for x in y[::-1]] for y in orientation_n[::-1]]
        orientation_w = list(map(list, zip(*flip_h)))

        self.__coords = [
            orientation_n,
            orientation_e,
            orientation_s,
            orientation_w,
            flip_v,
            flip_h
        ]

    @property
    def cells_cnt(self) -> int:
        return self.__cells_cnt

    def get_orientation(self, orientation: Orientation) -> List[List[bool]]:
        return self.__coords[orientation.value]

    def fits(self, grid: List[List[Optional[int]]], orientation: Orientation, y: int, x: int) -> bool:
        for dy in range(self.__side_len):
            for dx in range(self.__side_len):
                if self.get_orientation(orientation)[dy][dx] and grid[y+dy][x+dx] is not None:
                    return False
        return True

    def place_if_fits(self, grid: List[List[Optional[int]]], orientation: Orientation) -> Tuple[int, int]:
        for i in range(len(grid) + 1 - self.__side_len):
            for j in range(len(grid[i]) + 1 - self.__side_len):
                if self.fits(grid, orientation, i, j):
                    for y in range(self.__side_len):
                        for x in range(self.__side_len):
                            if self.get_orientation(orientation)[y][x]:
                                grid[i+y][j+x] = Shape.fill_i_val

                    Shape.fill_i_val += 1
                    return (i, j)

        return (-1, -1)

    def remove_from_grid(self, grid: List[List[Optional[int]]], orientation: Orientation, y: int, x: int):
        oriented = self.get_orientation(orientation)
        for i in range(y, y+self.__side_len):
            for j in range(x, x+self.__side_len):
                if not oriented[i-y][j-x]:
                    continue
                if grid[i][j] is None:
                    print('error, removing non existing shape coord')
                grid[i][j] = None

    def __str__(self) -> str:
        return '\n'.join((''.join('#' if x else '.' for x in row)
             for row in self.__coords[Orientation.N.value]
        ))

    @staticmethod
    def print_shape(coords: List[List[bool]]):
        print('\n'.join(
            (''.join('#' if x else '.' for x in row)
             for row in coords)
        ))


@dataclass
class Region:
    height: int
    width: int
    present_idxs_cnt: List[int]

@dataclass
class InputData:
    present_shapes: List[Shape]
    regions: List[Region]


def print_grid(grid: List[List[Optional[int]]]):
    print('\n'.join((''.join(str(x) if x is not None else '.' for x in row) for row in grid)))

def parse_input(raw_input: List[str]) -> InputData:
    start_idxs = [l for l, row in enumerate(raw_input) if row.endswith(':')]
    end_idxs = [raw_input.index('', i) for i in start_idxs]

    slices = [(l, r) for l,r in zip(start_idxs, end_idxs)]
    present_shapes: List[Shape] = [Shape([]) for _ in range(len(slices))]

    for i, (l, r) in enumerate(slices):
        present_idx = int(raw_input[l][:-1])
        if i != present_idx:
            print('error parsing input')
        present_shapes[present_idx] = Shape(raw_input[l+1:r])

    regions = []
    for row in raw_input[end_idxs[-1]+1:]:
        size, indexes_cnt = row.split(': ')
        width, length = (int(n) for n in size.split('x'))
        regions.append(Region(
            height=length,
            width=width,
            present_idxs_cnt=[int(i) for i in indexes_cnt.split()]
        ))

    return InputData(
        regions=regions,
        present_shapes=present_shapes
    )


def prob1(input_test: InputData, input: InputData) -> int:
    def can_fit(
            present_shapes: List[Shape],
            grid: List[List[Optional[int]]],
            indices_cnt: List[Tuple[int, int]]
    ) -> bool:
        if all([cnt == 0 for _, cnt in indices_cnt]):
            return True

        for i in range(len(indices_cnt)):
            shape_i, cnt = indices_cnt[i]

            if cnt == 0:
                continue

            for orientation in Orientation:
                did_fit_coords = present_shapes[shape_i].place_if_fits(grid, orientation)
                if did_fit_coords == (-1, -1):
                    continue

                next_indices_cnt = copy.deepcopy(indices_cnt)
                next_indices_cnt[i] = (shape_i, cnt-1)

                all_fitted = can_fit(present_shapes, copy.deepcopy(grid), next_indices_cnt)
                if all_fitted:
                    return True
                else:
                    present_shapes[shape_i].remove_from_grid(grid, orientation, did_fit_coords[0], did_fit_coords[1])

        return False

    test_input_fits_cnt = 0
    fits_cnt = 0

    print('Calibrating approximation of required extra empty cells count against test input, this can take a few minutes..')
    for i, region in enumerate(input_test.regions):
        grid: List[List[Optional[int]]] = [[None for _ in range(region.width)] for _ in range(region.height)]
        indicies = [(i, cnt) for i,cnt in enumerate(region.present_idxs_cnt) if cnt > 0]
        did_fit = can_fit(input_test.present_shapes, grid, indicies)
        if did_fit:
            test_input_fits_cnt += 1
        print(i+1, '/', len(input_test.regions), 'completed. All presents fitted:', did_fit)

    # Approximate required extra_cells count for every shape
    extra_cells = -1
    while fits_cnt != test_input_fits_cnt:
        extra_cells += 1
        fits_in_area = []
        for region in input_test.regions:
            size = region.height * region.width
            presents_required_size = 0
            for i, cnt in enumerate(region.present_idxs_cnt):
                presents_required_size += cnt * (input.present_shapes[i].cells_cnt + extra_cells)
            fits_in_area.append(presents_required_size < size)
        fits_cnt = sum(fits_in_area)

    # Run approximation for real input
    fits_cnt = 0
    for region in input.regions:
        size = region.height * region.width
        req_size = 0
        for i, cnt in enumerate(region.present_idxs_cnt):
            req_size += cnt * (input.present_shapes[i].cells_cnt + extra_cells)
        if req_size <= size:
            fits_cnt += 1

    return fits_cnt


def prob2(input) -> int:
    return -1

def main():
    input = parse_input(filemap('input.txt', str))
    input_test = parse_input(test_input)

    prob1_res = prob1(input_test, input)
    prob1_res = f'{prob1_res} ({"Correct" if prob1_res == 472 else "Wrong, correct = 472"})'
    print('Prob1:', prob1_res)

    prob2_res = prob2(input)
    prob2_res =f'{prob2_res} ({"Correct" if prob2_res == -1 else "Wrong, correct = -1"})'
    print('Prob2:', prob2_res)

if __name__ == '__main__':
    main()
