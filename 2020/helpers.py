from functools import reduce


def filemap(filename, func = int, sep='\n'):
    '''
    Reads in the filename and returns a list with all the rows mapped by
    the function func, which defaults to int(). That is returns
    a list containing one integer for every row of the file with def arguments.
    '''
    with open(filename, 'r') as f:
        return list(map(func, f.read().strip().split(sep)))

DIRECTIONS = dict(zip('ESWN', reduce(   # ( (0,1), (1,0), (0,-1), (-1,0) )
    lambda x, y: x + y, map(            # ( ((0,1), (1,0)), ((0,-1), (-1,0)) )
        lambda c: ((c[1], c[0]), c),
            ((y,0) for y in (1,-1))     # ( (1,0), (-1,0) )
        )
    )
))

def init_diags():
    dirs = list(DIRECTIONS.keys())
    for a in ('N', 'S'):
        for b in ('W', 'E'):
            A = DIRECTIONS[a]
            B = DIRECTIONS[b]
            DIRECTIONS[''.join((a, b))] = (A[0] + B[0], A[1] + B[1])

def initialize():
    init_diags()


def main():
    initialize()
    print(DIRECTIONS)


if __name__ == '__main__':
    main()
else:
    initialize()
