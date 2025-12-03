from typing import Dict, List, Tuple

# NOTE: Tuples of various length that contain integers are lazily typed just as Tuple instead of Iterable

def filemap(filename, func = int, sep='\n'):
    with open(filename, 'r') as f:
        return list(map(func, f.read().strip().split(sep)))

test_input = [
    "987654321111111",
    "811111111111119",
    "234234234234278",
    "818181911112111"
]

# Part 1, brute force
#def compute_bank_max_joltage(bank: Tuple) -> int:
#    max_joltage = 0
#    for l in range(0, len(bank)):
#        for r in range(l+1, len(bank)):
#            max_joltage = max(max_joltage, 10*bank[l] + bank[r])
#    return max_joltage

def compute_bank_n_batts_max_joltage(bank: Tuple, n: int, cache: Dict[Tuple[int, Tuple], int]) -> int:
    if (n, bank) in cache:
        return cache[(n, bank)]
    if n == 1:
        m = max(bank)
        cache[(n, bank)] = m
        return m
    if n > len(bank):
        return 0

    max_joltage = 0

    for i in range(0, len(bank)-1):
        current = 10 ** (n-1) * bank[i]
        rest = compute_bank_n_batts_max_joltage(bank[i+1:], n-1, cache)
        if rest == 0:
            continue
        current += rest
        max_joltage = max(max_joltage, current)

    cache[(n, bank)] = max_joltage
    return max_joltage

def compute_n_batts_combined_max_joltage(input: List[Tuple], n_batteries: int):
    cache = dict()
    total_joltage = 0
    for bank in input:
        total_joltage += compute_bank_n_batts_max_joltage(bank, n_batteries, cache)
    return total_joltage

def main():
    line_parser = lambda l: tuple(map(int, (c for c in l)))
    input = filemap('input.txt', line_parser) if True else list(map(line_parser, test_input))

    prob1_res = compute_n_batts_combined_max_joltage(input, 2)
    prob1_res = f'{prob1_res} ({"Correct" if prob1_res == 16993 else "Wrong, correct = 16993"})'
    print('Prob1:', prob1_res)

    prob2_res = compute_n_batts_combined_max_joltage(input, 12)
    prob2_res =f'{prob2_res} ({"Correct" if prob2_res == 168617068915447 else "Wrong, correct = 168617068915447"})'
    print('Prob2:', prob2_res)

if __name__ == '__main__':
    main()
