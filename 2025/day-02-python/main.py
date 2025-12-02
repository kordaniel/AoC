from typing import Callable, List, Tuple

def filemap(filename, func = int, sep='\n'):
    with open(filename, 'r') as f:
        return list(map(func, f.read().strip().split(sep)))

test_input = [
    "11-22",
    "95-115",
    "998-1012",
    "1188511880-1188511890",
    "222220-222224",
    "1698522-1698528",
    "446443-446449",
    "38593856-38593862",
    "565653-565659",
    "824824821-824824827",
    "2121212118-2121212124",
]

def is_part1_invalid_id(id: int) -> bool:
    as_str = str(id)
    id_len = len(as_str)
    if id_len % 2 != 0:
        return False
    half_id_len = id_len // 2

    a = as_str[:half_id_len]
    b = as_str[half_id_len:]

    return a == b

def is_part2_invalid_id(id: int) -> bool:
    as_str = str(id)
    id_len = len(as_str)

    for i in range(1, id_len // 2 + 1):
        slice = as_str[0:i]
        for j in range(i, id_len+1, i):
            if slice != as_str[j:j+i]:
                break
        if j == id_len:
            return True

    return False

def count_invalid_ids(input: List[Tuple[int, int]], invalid_id_predicate: Callable[[int], bool]) -> int:
    invalid_ids_sum = 0

    for (start, end) in input:
        for id in range(start, end+1):
            if invalid_id_predicate(id):
                invalid_ids_sum += id

    return invalid_ids_sum

def main():
    line_parser = lambda l: tuple(map(int, l.split('-')))
    line_separator = ','
    input = filemap('input.txt', line_parser, line_separator) if True else list(map(line_parser, test_input))

    prob1_res = count_invalid_ids(input, is_part1_invalid_id)
    prob1_res = f'{prob1_res} ({"Correct" if prob1_res == 35367539282 else "Wrong, correct = 35367539282"})'
    print('Prob1:', prob1_res)

    prob2_res = count_invalid_ids(input, is_part2_invalid_id)
    prob2_res =f'{prob2_res} ({"Correct" if prob2_res == 45814076230 else "Wrong, correct = 45814076230"})'
    print('Prob2:', prob2_res)

if __name__ == '__main__':
    main()
