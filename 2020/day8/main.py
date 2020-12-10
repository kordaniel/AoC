import sys
sys.path.insert(0, '..')

from helpers import filemap

# Part1
def walk(code):
    ''' Executes the instructions, stops when reach infinite loop and returns the value'''
    idx, accumulator = 0, 0
    visited = set()
    while True:
        if idx in visited:
            break
        visited.add(idx)
        instruction, arg = code[idx]
        if instruction == 'jmp':
            idx += arg
            continue
        if instruction == 'acc':
            accumulator += arg
        idx += 1
    return accumulator

# Part2
def walk_fix(code):
    ''' Executes the instructions and tries to fix the code so that it won't end
    up in an infinite loop'''
    idx, end_idx = 0, len(code)
    end_reached = False
    while not end_reached and idx < end_idx:
        code_arg = code[idx]
        if code_arg[0] == 'acc':
            idx += 1
            continue
        elif code_arg[0] == 'jmp':
            code[idx] = ('nop', code_arg[0])
        elif code_arg[0] == 'nop':
            code[idx] = ('jmp', code_arg[1])
        end_reached = can_reach_end(code)
        if not end_reached:
            code[idx] = code_arg
        else:
            return end_reached
        idx += 1
    raise Exception('ERRORRORORROROROROR')


def can_reach_end(code):
    end_idx = len(code)
    idx, accumulator = 0, 0
    visited = set()
    while True:
        if idx == end_idx:
            return True, accumulator
        if idx in visited:
            return False
        visited.add(idx)
        instruction, arg = code[idx]
        if instruction == 'jmp':
            idx += arg
            continue
        if instruction == 'acc':
            accumulator += arg
        idx += 1
    return accumulator

def main():
    # Test data
    data = [
        ('nop', 0),
        ('acc', 1),
        ('jmp', 4),
        ('acc', 3),
        ('jmp', -3),
        ('acc', -99),
        ('acc', 1),
        ('jmp', -4),
        ('acc', 6)
    ]
    data = filemap('input.txt', lambda s: s.split())
    data = list(map(lambda l: (l[0], int(l[1])), data))
    #print(data)

    # Part 1
    print('Part1:', walk(data))
    # Part 2
    print('Part2:', walk_fix(data))


if __name__ == '__main__':
    main()
