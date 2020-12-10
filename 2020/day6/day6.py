import sys
sys.path.insert(0, '..')

from functools import reduce
from helpers   import filemap

def main():
    groups = filemap('input.txt', lambda s: s, '\n\n')
    # Test data => Part 1: 11 & Part 2: 6
    #groups = [
    #    'abc',
    #    'a\nb\nc',
    #    'ab\nac',
    #    'a\na\na\na\na',
    #    'b'
    #]
    yes_tot     = 0 # Part 1
    yes_answers = 0 # Part 2
    all_answers = set()

    for g in groups:
        # Part 2
        grp_answers = map(lambda pa: set((c for c in pa)), g.split())
        result = reduce(lambda x, y: x.intersection(y), grp_answers)
        yes_answers += len(result)

        # Part 1
        yes_tot += len(set((c for c in g if c != '\n')))

    print('part1:', yes_tot)
    print('part2:', yes_answers)

if __name__ == '__main__':
    main()
