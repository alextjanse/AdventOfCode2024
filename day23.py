from typing import Iterator

def get_data() -> dict[str, list[str]]:
    '''Parse the input data into a dictionary that stores all the
    edge data. Store each edge twice, for (e1, e2) and (e2, e1).'''
    network: dict[str, set[str]] = dict()
    with open('data/day23.txt', encoding='utf-8') as file:
        for connection in file.read().splitlines():
            [a, b] = connection.split('-')
            if a not in network:
                network[a] = set()
            if b not in network:
                network[b] = set()
            network[a].add(b)
            network[b].add(a)
    return network

def solve_part_1(network: dict[str, set[str]]) -> None:
    '''Find all cliques of size 3 by looping over all possible n1, n2, n3,
    where they are in alphabetical order. Then filter on the once containing
    a node beginning with 't'.'''
    result = 0
    for n1 in network.keys():
        for n2 in filter(lambda n: n > n1, network[n1]):
            for n3 in filter(lambda n: n > n2, network[n1].intersection(network[n2])):
                # n3 is both neighbor of n1 and n2, so (n1, n2, n3) is a clique
                if any(map(lambda id: id[0] == 't', (n1, n2, n3))):
                    result += 1
    print(result)

def get_maximal_clique(node: str, network: dict[str, set[str]], pool: set[str] = None) -> list[str]:
    '''Get the maximal clique containing a given node. Use recursion to
    all possible sub-cliques.'''
    if pool is None:
        # Only on the first call, can't set default value to an assignment
        pool = network[node]
    maximal_clique = []
    for nb in filter(lambda n: node < n, pool):
        new_clique = get_maximal_clique(nb, network, network[nb].intersection(pool))
        if len(new_clique) > len(maximal_clique):
            maximal_clique = new_clique
    return [node] + maximal_clique

def solve_part_2(network: dict[str, set[str]]):
    '''Find the maximum clique by finding the maximal clique for each node.'''
    maximal_clique = []
    for v in network.keys():
        new_clique = get_maximal_clique(v, network)
        if len(new_clique) > len(maximal_clique):
            maximal_clique = new_clique
    print(','.join(maximal_clique))

if __name__ == '__main__':
    network = get_data()
    solve_part_1(network)
    solve_part_2(network)