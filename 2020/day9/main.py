import sys
sys.path.insert(0, '..')

from helpers import filemap

# Part 1
def has_sum(arr, sum):
    '''
    Returns true if the array contains 2 elements with different value
    s.t the sum of these elements equals the argument sum.
    '''

    arr.sort()

    if sum > arr[-1] + arr[-2] or sum < arr[0] + arr[1]:
        return False

    l, r = 0, len(arr) - 1
    while True:
        cur_sum = arr[l] + arr[r]
        if cur_sum == sum:
            return arr[l] != arr[r]
        if l == r:
            return False
        if cur_sum < sum:
            l += 1
        else:
            r -= 1


# Part 2
def sub_sum(arr, sum):
    '''
    Searches the array for a contiguous set of numbers s.t the sum
    of the subset equals the argument sum and then returns the sum
    of the smallest and biggest element in the subset. This function
    expects that the array contains such a subset!
    '''
    l,r = 0,1
    cur_sum = arr[l] + arr[r]
    while cur_sum != sum:
        if cur_sum < sum:
            r += 1
            cur_sum += arr[r]
        else:
            cur_sum -= arr[l]
            l += 1
    # Subset
    subsum = arr[l:r + 1]

    return min(subsum) + max(subsum)



def main():
    # Training data
    data = [
        35,
        20,
        15,
        25,
        47,
        40,
        62,
        55,
        65,
        95,
        102,
        117,
        150,
        182,
        127,
        219,
        299,
        277,
        309,
        576
    ]
    preamble_len = 5

    # Actual data
    data = filemap('input.txt')
    preamble_len = 25

    # Part 1 answer, index and the value
    p1 = ()
    for i in range(preamble_len, len(data)):
        if not has_sum(data[i-preamble_len:i], data[i]):
            p1 = (i, data[i])
            break
    print('Part1:', p1)
    print('Part2:', sub_sum(data[0:p1[0]], p1[1]))

if __name__ == '__main__':
    main()
