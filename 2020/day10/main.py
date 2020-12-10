import sys
sys.path.insert(0, '..')

from helpers import filemap

def search_combinations(data, target_joltage, mem = dict()):
    if target_joltage in mem:
        return mem[target_joltage]

    # If the joltage of this node is in the range [0,3], then we have a valid
    # combination. But we still need to check if we can add an adapter.
    # The arg target_joltage is always positive!
    combinations = 0 if target_joltage > 3 else 1

    for joltage in data:
        if joltage >= target_joltage:
            continue
        if joltage < target_joltage - 3:
            break
        combinations += search_combinations(data, joltage, mem)

    mem[target_joltage] = combinations
    return combinations

def search(data, target_joltage):
    data = sorted(data)
    data.append(target_joltage)
    res = []
    if data[0] > 3 or data[0] < 1:
        return res

    res.append(data[0])
    for i in range(1, len(data)):
        res.append(data[i] - data[i-1])

    return res

def count_freq(data):
    res = {}
    for n in data:
        if not n in res:
            res[n] = 0
        res[n] = res[n] + 1
    return res

def search_perf(data, target_joltage):
    data = sorted(data)
    data.append(target_joltage)
    prev = 0
    diffs = {1: 0, 3: 0}

    for j in data:
        diff = j - prev
        if not diff in diffs:
            print('diff is:', diff)
            raise Exception('ERROR: MALFORMED DATA ERRRRRRRRRROORORORORORO')

        diffs[diff] = diffs[diff] + 1
        prev = j

    return diffs[1] * diffs[3]

def main():
    # Testing data
    data = [
        28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38,
        39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3
    ]
    data = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]
    # Actual data
    data = filemap('input.txt')

    dev_joltage = max(data) + 3
    #print(dev_joltage)

    # Part1
    res = search(data, dev_joltage)
    res_freq = count_freq(res)
    print('Part1:', res_freq[1] * res_freq[3])
    print('Part1:', search_perf(data, dev_joltage))

    # Part 2
    print('Part2:', search_combinations(sorted(data, reverse=True), dev_joltage))

if __name__ == '__main__':
    main()
