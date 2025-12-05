from typing import Callable, List, Tuple

# NOTE: Python 3.8, type system has no support for proper generics

def filemap(filename: str, func: Callable = int, sep: str = '\n') -> List:
    with open(filename, 'r') as f:
        return list(map(func, f.read().strip().split(sep)))

test_input = [
    '3-5',
    '10-14',
    '16-20',
    '12-18',
    '',
    '1',
    '5',
    '8',
    '11',
    '17',
    '32'
]

def parse_input(input: List[str]) -> Tuple[List[Tuple[int, int]], List[int]]:
    id_ranges = []
    ids = []
    parsing_ranges = True

    for line in input:
        if line == '':
            parsing_ranges = False
            continue
        if parsing_ranges:
            id_ranges.append(tuple(map(int, line.split('-'))))
        else:
            ids.append(int(line))

    id_ranges.sort()
    combined = id_ranges[:1]

    for low, high in id_ranges[1:]:
        if low <= combined[-1][1]:
            combined[-1] = (combined[-1][0], max(combined[-1][1], high))
        else:
            combined.append((low, high))

    return (combined, sorted(ids))

def prob1(fresh_id_ranges: List[Tuple[int, int]], ids: List[int]) -> int:
    fresh_ids_cnt = 0
    min_id_i = 0

    for id in ids:
        for i in range(min_id_i, len(fresh_id_ranges)):
            low, high = fresh_id_ranges[i]
            if low <= id <= high:
                fresh_ids_cnt += 1
                min_id_i = i
                break

    return fresh_ids_cnt

def prob2(fresh_id_ranges: List[Tuple[int, int]]) -> int:
    return sum(high-low+1 for low, high in fresh_id_ranges)

def main():
    input = parse_input(filemap('input.txt', str) if True else test_input)

    prob1_res = prob1(input[0], input[1])
    prob1_res = f'{prob1_res} ({"Correct" if prob1_res == 690 else "Wrong, correct = 690"})'
    print('Prob1:', prob1_res)

    prob2_res = prob2(input[0])
    prob2_res =f'{prob2_res} ({"Correct" if prob2_res == 344323629240733 else "Wrong, correct = 344323629240733"})'
    print('Prob2:', prob2_res)

if __name__ == '__main__':
    main()
