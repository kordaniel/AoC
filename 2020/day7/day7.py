import sys
sys.path.insert(0, '..')

from helpers import filemap

def parse_data(data):
    can_go_in = dict()

    for rule in data:
        rule = rule.replace(' bags', '').replace(' bag', '')
        if rule[-1] != '.':
            raise Exception('BAD INPUT')
        rule = rule[:-1]
        outer, inner = rule.split(' contain ')
        inner = inner.split(', ')
        for color in inner:
            if not color[:1].isdigit():
                continue
            if not outer in can_go_in:
                can_go_in[outer] = set()
            can_go_in[outer].add((color[2:], int(color[0])))

    return can_go_in

def count(possibilities, color, target_color):
    if color == target_color:
        return 1
    if color not in possibilities:
        return 0

    for inner_color in possibilities[color]:
        if inner_color[0] == target_color or \
                count(possibilities, inner_color[0], target_color) > 0:
            return 1

    return 0

# Part 2
def count_p2(possibilities, color):
    sum = 1
    if color not in possibilities:
        return sum

    for inner_color in possibilities[color]:
        sum += inner_color[1] * count_p2(possibilities, inner_color[0])

    return sum

def main():
    # Part 1 testing data
    data = (
        'light red bags contain 1 bright white bag, 2 muted yellow bags.',
        'dark orange bags contain 3 bright white bags, 4 muted yellow bags.',
        'bright white bags contain 1 shiny gold bag.',
        'muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.',
        'shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.',
        'dark olive bags contain 3 faded blue bags, 4 dotted black bags.',
        'vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.',
        'faded blue bags contain no other bags.',
        'dotted black bags contain no other bags.'
    )
    # Part 2 testing data
    data = (
        'shiny gold bags contain 2 dark red bags.',
        'dark red bags contain 2 dark orange bags.',
        'dark orange bags contain 2 dark yellow bags.',
        'dark yellow bags contain 2 dark green bags.',
        'dark green bags contain 2 dark blue bags.',
        'dark blue bags contain 2 dark violet bags.',
        'dark violet bags contain no other bags.'
    )

    data = filemap('input.txt', lambda s: s, '\n')
    #print(data)
    possibilities = parse_data(data)

    # Part 1
    target_color = 'shiny gold'
    sum = 0
    for outer_color in possibilities:
        if outer_color == target_color:
            continue
        sum += count(possibilities, outer_color, target_color)
    print('Part1:', sum)
    # Part 1 end

    # Part 2
    print('Part2', count_p2(possibilities, target_color) - 1)

if __name__ == '__main__':
    main()
