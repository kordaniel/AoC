import sys
sys.path.insert(0, '..')

from helpers import filemap

def handle_row(row):
    '''
    l,r = index of row
    s_l, s_r = index of seat
    '''
    l, r = 0, 127
    s_l, s_r = 0, 7
    for i in range(7):
        if row[i] == 'F':
            r = (l+r) // 2
        elif row[i] == 'B':
            l = (l+r) // 2 + 1
        else:
            raise Exception('Invalid input')
    if l != r:
        raise Exception('INVALID INPUT OR CALCULATION')


    for i in range(7, 10):
        if row[i] == 'L':
            s_r = (s_r + s_l) // 2
        elif row[i] == 'R':
            s_l = (s_r + s_l) // 2 + 1
        else:
            raise Exception('Invlaid row input')
    if s_l != s_r:
        raise Exception('INVALID SEAT INPUT OR CALCULATION')

    return l * 8 + s_l

def main():
    lines = filemap('input.txt', lambda s: s)
    seat_ids = sorted([handle_row(r) for r in lines])

    print('Part1:', max(seat_ids)) # Part 1

    # Part 2
    for i in range(1, len(seat_ids) - 1):
        if seat_ids[i] - seat_ids[i - 1] != 1:
            print('Part2:', seat_ids[i] - 1)
            break

if __name__ == '__main__':
    main()
