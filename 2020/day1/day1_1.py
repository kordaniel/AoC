with open('input.txt', 'r') as f:
    lines = [int(v) for v in f.read().splitlines()]

lines.sort()
value = 2020
found = False

for l in range(len(lines)):
    if found: break
    for r in range(l, len(lines)):
        if found: break
        sum = lines[l] + lines[r]
        if sum > value:
            break
        for x in range(len(lines)):
            if found: break
            if sum + lines[x] < value:
                continue
            if sum + lines[x] > value:
                break
            print(lines[l], '+', lines[r], '+', lines[x], '=', value)
            print('product:', lines[l]*lines[r]*lines[x])
            found = True
