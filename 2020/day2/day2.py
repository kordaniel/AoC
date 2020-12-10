with open('input.txt', 'r') as f:
    lines = f.read().splitlines()

validCount = 0

def handleLine(l):
    # Part one
    req, passwd = l.split(':')
    min_req, max_req = req.split()[0].split('-')
    min_req, max_req = int(min_req), int(max_req)
    char = req.split()[1]

    count = 0
    for c in passwd:
        #print(c)
        if c == char:
            count += 1
        if count > max_req:
            return False

    return count >= min_req


def handle_line(l):
    # Part 2
    req, passwd = l.split(': ') # Cut blank away
    first_req, second_req = req.split()[0].split('-')
    first_req, second_req = int(first_req)-1, int(second_req)-1
    char = req.split()[1]
    return (passwd[first_req] == char or passwd[second_req] == char) and (passwd[first_req] != passwd[second_req])

for r in lines:
    #print(r)
    if handle_line(r):
        validCount += 1

print('Valid lines count:', validCount)
