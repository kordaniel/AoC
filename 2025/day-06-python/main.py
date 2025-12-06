from dataclasses import dataclass
import operator
import string
from typing import Callable, List

def filemap(filename: str, func: Callable = int, sep: str = '\n') -> List:
    with open(filename, 'r') as f:
        return list(map(func, f.read().split(sep)))

test_input = [
    '123 328  51 64 ',
    ' 45 64  387 23 ',
    '  6 98  215 314',
    '*   +   *   +  '
]

OPS_MAP = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

@dataclass
class ParsedInput:
    col_widths: List[int]
    lines: List[List[str]]
    operators: List[str]


def parse_input(lines: List[str]) -> ParsedInput:
    operators_line = lines[-1]
    operators = []
    col_widths = []
    str_values_lines = []

    i, j = 0, 1
    while True:
        if j == len(operators_line):
            operators.append(operators_line[i])
            col_widths.append(j-i)
            break
        if not operators_line[j] in string.whitespace:
            operators.append(operators_line[i])
            col_widths.append(j-i-1)
            i = j
        j += 1

    for line in lines[:-1]:
        str_values_lines.append([])
        start_i = 0
        for col_width in col_widths:
            end_i = start_i + col_width
            str_values_lines[-1].append(line[start_i:end_i])
            start_i = end_i + 1

    return ParsedInput(col_widths=col_widths, lines=str_values_lines, operators=operators)

def prob1(str_values_lines: List[List[str]], operators: List[str]) -> int:
    tot_sum = 0
    nums = zip(*str_values_lines) # Transpose matrix
    nums = (map(lambda n: n.strip(), row) for row in nums)
    nums = [list(map(int, row)) for row in nums]

    for i, op in enumerate(operators):
        col_result = nums[i][0]
        for n in nums[i][1:]:
            try:
                col_result = OPS_MAP[op](col_result, n)
            except:
                print('Error')
                continue
        tot_sum += col_result

    return tot_sum

def prob2(
        str_values_lines: List[List[str]],
        operators: List[str],
        col_widths: List[int]
) -> int:
    tot_sum = 0
    nums = list(zip(*str_values_lines)) # Transpose matrix

    for i, op in enumerate(operators):
        col_result = None
        for c in range(col_widths[i]-1, -1, -1):
            col_num = []
            for n in nums[i]:
                if n[c] == ' ':
                    continue
                col_num.append(n[c])

            if len(col_num) == 0:
                continue
            col_num = int(''.join(col_num))
            if col_result == None:
                col_result = col_num
            else:
                col_result = OPS_MAP[op](col_result, col_num)

        if col_result is not None:
            tot_sum += col_result

    return tot_sum

def main():
    input = parse_input(filemap('input.txt', str) if True else test_input)

    prob1_res = prob1(input.lines, input.operators)
    prob1_res = f'{prob1_res} ({"Correct" if prob1_res == 4076006202939 else "Wrong, correct = 4076006202939"})'
    print('Prob1:', prob1_res)

    prob2_res = prob2(input.lines, input.operators, input.col_widths)
    prob2_res =f'{prob2_res} ({"Correct" if prob2_res == 7903168391557 else "Wrong, correct = 7903168391557"})'
    print('Prob2:', prob2_res)

if __name__ == '__main__':
    main()
