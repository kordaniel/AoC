import sys
sys.path.insert(0, '..')

from helpers import filemap
from functools import reduce

def find_two_elements_with_sum(data, sum):
    ''' Returns the index of the two elements that sum up to sum.
        Returns -1 for both indexes if such elements does not exist.
    '''
    l, r = 0, len(data) - 1
    cur_sum = data[l] + data[r]

    while cur_sum != sum:
        if cur_sum < sum:
            l +=1
        else:
            r -= 1
        if (l > r):
            return -1, -1
        cur_sum = data[l] + data[r]

    return l, r

def find_three_elements_with_sum(data, sum):
    ''' Returns the index of three elements that sum up to sum.
        Returns -1 for all 3 indexes if such elements does not exits.
    '''
    for i in range(len(data)):
        l, r = find_two_elements_with_sum(data, sum - data[i])
        if l != -1 and r != -1:
            return l, r, i
    return -1, -1, -1

def product_of_elements(data, indexes):
    return reduce(lambda x, y: x * y, [data[i] for i in indexes])


def main():
    # Testing data
    #data = sorted([1721, 979, 366, 299, 675, 1456]) #P1: 514579, P2: 241861950

    # Actual data
    data = sorted(filemap('input.txt'))
    target_sum = 2020

    p1_indx = find_two_elements_with_sum(data, target_sum)
    p2_indx = find_three_elements_with_sum(data, target_sum)

    print('Part1:', product_of_elements(data, p1_indx))
    print('Part2:', product_of_elements(data, p2_indx))


if __name__ == '__main__':
    main()
