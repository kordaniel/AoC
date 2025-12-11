from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

def filemap(filename: str, func: Callable = int, sep: str = '\n') -> List:
    with open(filename, 'r') as f:
        return list(map(func, f.read().strip().split(sep)))

test_input_1 = [
    'aaa: you hhh',
    'you: bbb ccc',
    'bbb: ddd eee',
    'ccc: ddd eee fff',
    'ddd: ggg',
    'eee: out',
    'fff: out',
    'ggg: out',
    'hhh: ccc fff iii'
]

test_input_2 = [
    'svr: aaa bbb',
    'aaa: fft',
    'fft: ccc',
    'bbb: tty',
    'tty: ccc',
    'ccc: ddd eee',
    'ddd: hub',
    'hub: fff',
    'eee: dac',
    'dac: fff',
    'fff: ggg hhh',
    'ggg: out',
    'hhh: out'
]

@dataclass
class ParsedInput:
    graph: Tuple[List[int], ...]
    node_idx_map: Dict[str, Optional[int]]

def parse_input(raw_input: List[str]) -> ParsedInput:
    parsed_graph = dict()
    for line in raw_input:
        node, edges = line.split(': ')
        if node in parsed_graph:
            print('error')
        parsed_graph[node] = list(edges.split())

    graph = tuple([] for _ in range(len(parsed_graph)+1)) # + 1 for 'out' node
    i = 0
    node_to_i = dict()
    node_to_i['out'] = i
    i += 1

    for node in parsed_graph:
        node_to_i[node] = i
        i += 1

    for node, edges in parsed_graph.items():
        graph[node_to_i[node]].extend([node_to_i[e] for e in edges if e in node_to_i])

    node_idx_map = {
        'you': node_to_i.get('you', None),
        'svr': node_to_i.get('svr', None),
        'dac': node_to_i.get('dac', None),
        'fft': node_to_i.get('fft', None),
        'out': node_to_i.get('out', None)
    }

    return ParsedInput(graph, node_idx_map)

def prob1(graph: Tuple[List[int], ...], node_idx_map: Dict[str, Optional[int]]) -> int:
    tot_paths_cnt = 0

    if node_idx_map['you'] is None or node_idx_map['out'] is None:
        raise RuntimeError('Invalid input for prob 1')

    edges = [graph[node_idx_map['you']]]
    out_edge = node_idx_map['out']

    while len(edges) > 0:
        cur_edge = edges.pop()
        for next_edge in cur_edge:
            if next_edge == out_edge:
                tot_paths_cnt += 1
            else:
                edges.append(graph[next_edge])

    return tot_paths_cnt

def prob2(graph: Tuple[List[int], ...], node_idx_map: Dict[str, Optional[int]]) -> int:
    svr = node_idx_map['svr']
    dac = node_idx_map['dac']
    fft = node_idx_map['fft']
    out = node_idx_map['out']
    cache = dict()

    # check svr directly to silence pylance error
    if svr is None or any([i is None for i in (dac, fft, out)]):
        raise RuntimeError('Invalid input for prob 2')

    def dfs_closure(node: int, dac_seen: bool, fft_seen: bool) -> int:
        if node == out:
            return 1 if dac_seen and fft_seen else 0

        tot_path_cnt = 0
        for edge in graph[node]:
            is_dac_edge = dac_seen or edge == dac
            is_fft_edge = fft_seen or edge == fft
            if (edge, is_dac_edge, is_fft_edge) in cache:
                edge_cnt = cache[(edge, is_dac_edge, is_fft_edge)]
            else:
                edge_cnt = dfs_closure(edge, is_dac_edge, is_fft_edge)
                cache[(edge, is_dac_edge, is_fft_edge)] = edge_cnt
            tot_path_cnt += edge_cnt

        return tot_path_cnt

    return dfs_closure(svr, False, False)

def main():
    use_test_input = False
    input1 = parse_input(filemap('input.txt', str) if not use_test_input else test_input_1)

    prob1_res = prob1(input1.graph, input1.node_idx_map)
    prob1_res = f'{prob1_res} ({"Correct" if prob1_res == 788 else "Wrong, correct = 788"})'
    print('Prob1:', prob1_res)

    input2 = parse_input(filemap('input.txt', str) if not use_test_input else test_input_2)
    prob2_res = prob2(input2.graph, input2.node_idx_map)
    prob2_res =f'{prob2_res} ({"Correct" if prob2_res == 316291887968000 else "Wrong, correct = 316291887968000"})'
    print('Prob2:', prob2_res)

if __name__ == '__main__':
    main()
