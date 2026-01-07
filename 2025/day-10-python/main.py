from dataclasses import dataclass
import heapq

from typing import Callable, List, Set, Tuple

def filemap(filename: str, func: Callable = int, sep: str = '\n') -> List:
    with open(filename, 'r') as f:
        return list(map(func, f.read().strip().split(sep)))

@dataclass
class Machine:
    indicator_ligths: Tuple[bool, ...]
    wiring_schematics: List[Set[int]]
    joltage_requirements: List[int]


test_input = [
    '[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}',
    '[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}',
    '[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}'
]

def parse_input_line(line: str):
    l, r = line.index('['), line.index(']')
    indicator_lights = tuple(False if c == '.' else True for c in line[l+1:r])

    wiring_schematics = []
    l = line.index('(')
    r = l+1
    while r < len(line):
        if line[r] == ')':
            wiring_schematics.append(set(int(c) for c in line[l+1:r].split(',')))
            r += 1
            while r < len(line):
                if line[r] == '(':
                    l = r
                    break
                r +=1
        r += 1

    l, r = line.find('{'), line.find('}')
    joltage_requirements = list(int(c) for c in line[l+1:r].split(','))

    return Machine(
        indicator_ligths=indicator_lights,
        wiring_schematics=wiring_schematics,
        joltage_requirements=joltage_requirements
    )

def prob1_dijkstra(indicators: Tuple[bool, ...], schematics: List[Set[int]]) -> int:
    cache = dict()
    heap = []
    min_presses = 1 << 63
    heapq.heappush(heap, (0, tuple(False for _ in range(len(indicators)))))

    while len(heap) > 0:
        presses, indicators_state = heapq.heappop(heap)
        if indicators == indicators_state:
            min_presses = min(min_presses, presses)

        for schema in schematics:
            next_indicators = tuple(not indicators_state[i] if i in schema else indicators_state[i] for i in range(len(indicators)))
            if not next_indicators in cache or presses+1 < cache[next_indicators]:
                cache[next_indicators] = presses+1
                heapq.heappush(heap, (presses+1, next_indicators))

    return min_presses

def prob1(input: List[Machine]) -> int:
    tot_presses = 0
    for machine in input:
        presses = prob1_dijkstra(machine.indicator_ligths, machine.wiring_schematics)
        tot_presses += presses
    return tot_presses

def prob2(input: List[Machine]) -> int:
    return -1

def main():
    input = filemap('input.txt', parse_input_line) if True else list(map(parse_input_line, test_input))

    prob1_res = prob1(input)
    prob1_res = f'{prob1_res} ({"Correct" if prob1_res == 507 else "Wrong, correct = 507"})'
    print('Prob1:', prob1_res)

    prob2_res = prob2(input) # 10 + 12 + 11 = 33
    prob2_res =f'{prob2_res} ({"Correct" if prob2_res == 33 else "Wrong, correct = 33"})'
    print('Prob2: (TODO: Implement linear equation solver for integer solutions?):', prob2_res)

if __name__ == '__main__':
    main()
