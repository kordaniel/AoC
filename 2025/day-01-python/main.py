from typing import List, Tuple

def filemap(filename, func = int, sep='\n'):
    with open(filename, 'r') as f:
        return list(map(func, f.read().strip().split(sep)))

test_input = [
    'L68',
    'L30',
    'R48',
    'L5',
    'R60',
    'L55',
    'L1',
    'L99',
    'R14',
    'L82'
]

def prob1(input: List[Tuple[str, int]]) -> int:
    dial = 50
    zeros_count = 0

    for dir, val in input:
        if dir == 'L':
            dial = (dial - val) % 100
        elif dir == 'R':
            dial = (dial + val) % 100
        else:
            print('ERROR')

        if dial == 0:
            zeros_count += 1

    return zeros_count

def prob2(input: List[Tuple[str, int]]):
    dial = 50
    zeros_count = 0

    for dir, val in input:
        zeros_count += val // 100
        val %= 100

        if dir == 'L':
            if dial != 0 and val > dial:
                zeros_count += 1
            dial = (dial - val) % 100
        elif dir == 'R':
            if dial != 0 and val > (100-dial):
                zeros_count += 1
            dial = (dial + val) % 100

        if dial == 0:
            zeros_count += 1

    return zeros_count

def main():
    line_parser = lambda r: (r[:1], int(r[1:]))
    input = filemap('input.txt', line_parser) if True else list(map(line_parser, test_input))
    print('Prob1: ', prob1(input))
    print('Prob2: ', prob2(input))

if __name__ == '__main__':
    main()
