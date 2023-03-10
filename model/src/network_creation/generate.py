from itertools import count
import random
from typing import Any, Callable, Hashable, Iterator
import networkx as nx
from functools import partial, reduce
import matplotlib.pyplot as plt

import numpy as np

dist_exponential = partial(np.random.exponential, scale = 1)

def generate_scale_free_network(node_num:int, edge_num:int, distribution_function: Callable):

    probability_array = distribution_function(size = node_num)

    probability_array = probability_array / np.sum(probability_array)

    edge_distribution = np.floor(probability_array * edge_num)

    edge_distribution[edge_distribution == 0] = 1

    remaining_edges: int = edge_num -  sum(edge_distribution)

    edge_distribution += np.random.multinomial(remaining_edges, probability_array)

    return edge_distribution

def edge_distribution_to_agent_list(id_generator: Iterator, edges) -> list[int]:
    return reduce(lambda lst, count: lst + [next(id_generator)] * int(count), ## aggregate
                    edges,      ## list of appearance
                    [])         ## init empty list

def edge_distribution_to_bipartite_network(
    edges1: np.ndarray,
    edges2: np.ndarray,
    bipartite_name: tuple[Hashable, Hashable]):
    """
    Converts edge distribution of a bipartite network to a bipartite network graph.

    Args:
    edges1 (np.ndarray): Edge distribution for bipartite set 1.
    edges2 (np.ndarray): Edge distribution for bipartite set 2.
    bipartite_name (tuple[Hashable, Hashable]): Tuple containing the names for bipartite sets 1 and 2.

    Returns:
    nx.Graph: A bipartite network graph constructed from the input edge distributions.

    Raises:
    ValueError: If the sum of edges in the two input edge distributions are not equal.

    """
    if np.sum(edges1) != np.sum(edges2):
        raise ValueError("Numbers of edges does not match!")

    id_generator = count()
    bipartite_1_agent_count_list = edge_distribution_to_agent_list(id_generator, edges1)
    bipartite_2_agent_count_list = edge_distribution_to_agent_list(id_generator, edges2)
    random.shuffle(bipartite_1_agent_count_list)
    random.shuffle(bipartite_2_agent_count_list)

    G = nx.Graph()
    G.add_nodes_from(set(bipartite_1_agent_count_list), bipartite = bipartite_name[0])
    G.add_nodes_from(set(bipartite_2_agent_count_list), bipartite = bipartite_name[1])

    G.add_edges_from(zip(bipartite_1_agent_count_list, bipartite_2_agent_count_list))

    one_set = set(bipartite_1_agent_count_list)
    return one_set, G




if __name__ == '__main__':

    node_n = 30
    avg_edge = 5
    total_edge = node_n * avg_edge

    distribution_function = partial(np.random.exponential, scale=1)
    edges1 = generate_scale_free_network(node_n, total_edge, distribution_function)
    edges2 = generate_scale_free_network(node_n, total_edge, distribution_function)

    node_1, G = edge_distribution_to_bipartite_network(edges1, edges2, ("buyer", "seller"))

    pos = nx.bipartite_layout(G, node_1)

    nx.draw(
        G,
        pos = pos,
        node_color = ['r'] * node_n + ['b'] * node_n,
        alpha = 0.5,
        node_size =[ deg * 40 for deg in dict(G.degree).values()]
    )
    plt.show()