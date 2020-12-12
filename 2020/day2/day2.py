import sys
sys.path.insert(0, '..')

from helpers import filemap

def passwd_has_correct_amount_of_req_char(l):
    # Validator for part one
    req, passwd = l
    min_req, max_req = map(int, req.split()[0].split('-'))
    char = req.split()[1]
    return min_req <= len([c for c in passwd if c == char]) <= max_req

def passwd_has_correct_char_in_specific_indx(l):
    ''' "Exactly one of these positions must contain the given letter!"
         Positions start indexing from 1, not 0.
    '''
    # Validator for part two. Offset index in lambdafunction.
    req, passwd = l
    first_req, second_req = map(lambda v: int(v) - 1, req.split()[0].split('-'))
    char = req.split()[1]
    return (passwd[first_req] == char or passwd[second_req] == char) \
            and (passwd[first_req] != passwd[second_req])

def valid_lines_count(data, func):
    return sum([func(l) for l in data])


def main():
    lines = filemap('input.txt', lambda s: s.split(': '))

    valid_passwds_p1 = valid_lines_count(lines, passwd_has_correct_amount_of_req_char)
    valid_passwds_p2 = valid_lines_count(lines, passwd_has_correct_char_in_specific_indx)

    print('Part1:', valid_passwds_p1)
    print('Part2:', valid_passwds_p2)


if __name__ == '__main__':
    main()
