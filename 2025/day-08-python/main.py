import heapq
import math
from typing import Callable, Dict, List, NamedTuple, Set, Tuple

test_input = [
    '162,817,812',
    '57,618,57',
    '906,360,560',
    '592,479,940',
    '352,342,300',
    '466,668,158',
    '542,29,236',
    '431,825,988',
    '739,650,466',
    '52,470,668',
    '216,146,977',
    '819,987,18',
    '117,168,530',
    '805,96,715',
    '346,949,466',
    '970,615,88',
    '941,993,340',
    '862,61,35',
    '984,92,344',
    '425,690,689'
]

class Point3D(NamedTuple):
    x: int
    y: int
    z: int

def filemap(filename: str, func: Callable = int, sep: str = '\n') -> List:
    with open(filename, 'r') as f:
        return list(map(func, f.read().strip().split(sep)))

def dist(a: Point3D, b: Point3D) -> float:
    return math.sqrt((a.x-b.x) ** 2 + (a.y-b.y) ** 2 + (a.z-b.z) ** 2)

def compute_distances(input: List[Point3D]) -> Tuple[Dict[int, Dict[int, float]], List[Tuple[float, Tuple[int, int]]]]:
    dist_graph: Dict[int, Dict[int, float]] = dict()
    distlist: List[Tuple[float, Tuple[int, int]]] = list()

    for i in range(len(input)):
        dist_graph[i] = dict()
        for j in range(i+1, len(input)):
            d = dist(input[i], input[j])
            dist_graph[i][j] = d
            distlist.append((d, (i, j)))

    heapq.heapify(distlist)
    return dist_graph, distlist

def prob1(input: List[Point3D], connections_cnt: int) -> int:
    _, distlist = compute_distances(input)
    circuits: List[Set[int]] = list()

    added_cnt = 0
    while added_cnt < connections_cnt:
        added_cnt += 1
        was_in_same_circuit = False
        _, (a, b) = heapq.heappop(distlist)

        matching_indexes = []
        for i, circuit in enumerate(circuits):
            if a in circuit:
                if b in circuit:
                    was_in_same_circuit = True
                    break
                matching_indexes.append(i)
            elif b in circuit:
                matching_indexes.append(i)

            if len(matching_indexes) == 2:
                break

        if was_in_same_circuit:
            continue

        if len(matching_indexes) == 0:
            circuits.append({a, b})
        elif len(matching_indexes) == 1:
            circuits[matching_indexes[0]].add(a)
            circuits[matching_indexes[0]].add(b)
        elif len(matching_indexes) == 2:
            circuits[matching_indexes[0]].add(a)
            circuits[matching_indexes[0]].add(b)
            circuits[matching_indexes[0]] |= circuits[matching_indexes[1]]
            del circuits[matching_indexes[1]]
        else:
            print("Logic error")

    circuit_sizes = sorted((len(s) for s in circuits), reverse=True)
    return math.prod(circuit_sizes[:3])

def prob2(input: List[Point3D]) -> int:
    distances, distlist = compute_distances(input)
    circuits: List[Set[int]] = list()

    orphan_nodes = set(distances.keys())
    last_added_pair = None

    while len(distlist) > 0:
        was_in_same_circuit = False
        matching_indexes = []
        _, (a, b) = heapq.heappop(distlist)

        for idx, circuit in enumerate(circuits):
            if a in circuit:
                if b in circuit:
                    was_in_same_circuit = True
                    break
                matching_indexes.append(idx)
            elif b in circuit:
                matching_indexes.append(idx)

            if len(matching_indexes) == 2:
                break

        if was_in_same_circuit:
            continue

        if len(matching_indexes) == 0:
            last_added_pair = (a, b)
            if a in orphan_nodes: orphan_nodes.remove(a)
            if b in orphan_nodes: orphan_nodes.remove(b)
            circuits.append({a, b})
        elif len(matching_indexes) == 1:
            last_added_pair = (a, b)
            if a in orphan_nodes: orphan_nodes.remove(a)
            if b in orphan_nodes: orphan_nodes.remove(b)
            circuits[matching_indexes[0]].add(a)
            circuits[matching_indexes[0]].add(b)
        elif len(matching_indexes) == 2:
            last_added_pair = (a, b)
            circuits[matching_indexes[0]] |= circuits[matching_indexes[1]]
            del circuits[matching_indexes[1]]
        else:
            print("Logic error")

    if last_added_pair is None:
        return -1

    j_box_a = input[last_added_pair[0]]
    j_box_b = input[last_added_pair[1]]

    return j_box_a.x * j_box_b.x


def main():
    use_test_input = False
    line_parser = lambda l: list(map(int, l.strip().split(',')))
    input = filemap('input.txt', line_parser) if not use_test_input else list(map(line_parser, test_input))
    input = list(map(lambda l: Point3D(*l), input))

    prob1_res = prob1(input, 10 if use_test_input else 1000)
    prob1_res = f'{prob1_res} ({"Correct" if prob1_res == 164475 else "Wrong, correct = 164475"})'
    print('Prob1:', prob1_res)

    prob2_res = prob2(input)
    prob2_res =f'{prob2_res} ({"Correct" if prob2_res == 169521198 else "Wrong, correct = 169521198"})'
    print('Prob2:', prob2_res)

if __name__ == '__main__':
    main()
