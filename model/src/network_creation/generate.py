from itertools import count
import random
from typing import Annotated, Any, Callable, Hashable, Iterator
import networkx as nx
from functools import partial, reduce
import matplotlib.pyplot as plt

import numpy as np

dist_exponential = partial(np.random.exponential, scale = 1)

def get_probability_array_for_agents(node_num:int, distribution_function: Callable):
    """
    Returns the probability for each `node_num` agents of being picked
    """
    probability_array = distribution_function(size = node_num)
    probability_array = probability_array / np.sum(probability_array)
    return probability_array

def generate_degree_from_prob_list(edge_num:int, probability_array, must_have_one: bool=True):
    """
    Generate a list(np.array) of degree according to the probability of connection for each agents, and with a given total number of edges.
    """
    node_num = len(probability_array)
    edge_distribution = np.floor(probability_array * edge_num)

    if must_have_one:
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
    bipartite_name: tuple[Hashable, Hashable],
    id_generator: Iterator):
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


def generate_cross_broader_bipartite(graph1: nx.Graph, graph2: nx.Graph, international_level:float = 0.5) -> nx.Graph:
    """
    Given two graphs of country-side buyer-seller networks, generate a cross-broader
    transaction network.

    The distribution of cross-broader transactions follows the scale-free
    network characteristics, where the higher the degree one node has, the
    higher the probability of getting picked as a foreign seller.
    """
    country_1_nodes = graph1.nodes(data=True)
    country_2_nodes = graph2.nodes(data=True)

    country_1_buyers = [i for i,n in country_1_nodes if n['bipartite'] == 'buyer']
    country_1_sellers = [i for i,n in country_1_nodes if n['bipartite'] == 'seller']
    country_2_buyers = [i for i,n in country_2_nodes if n['bipartite'] == 'buyer']
    country_2_sellers = [i for i,n in country_2_nodes if n['bipartite'] == 'seller']

    average_edge_before_cross_boarder: int = np.floor(np.mean([graph1.number_of_edges(), graph2.number_of_edges()]))

    edges_to_create = np.round(average_edge_before_cross_boarder * international_level)

    ## match 1b 2s
    b1_degree : list[int] = [graph1.degree(n) for n in country_1_buyers]
    s2_degree : list[int]= [graph2.degree(n) for n in country_2_sellers]

    b1_prob = b1_degree / np.sum(b1_degree)
    s2_prob = b1_degree / np.sum(s2_degree)

    b1_out_edges = generate_degree_from_prob_list(edges_to_create, b1_prob, must_have_one=False)
    s2_out_edges = generate_degree_from_prob_list(edges_to_create, s2_prob, must_have_one=Falae)

    b1_out_edges




    ## match 1s 2b




if __name__ == '__main__':

    node_n = 30
    avg_edge = 5
    total_edge = node_n * avg_edge

    distribution_function = partial(np.random.exponential, scale=1)
    edges = []
    population = [1,1,0.5, 0.5]
    for i in range(4):
        edges.append(generate_degree_from_prob_list(
        total_edge * int(population[i]),
        get_probability_array_for_agents(node_n * int(population[i]), distribution_function)))

    id_generator = count()
    node_1, G1 = edge_distribution_to_bipartite_network(edges[0], edges[1], ("buyer", "seller"), id_generator)
    node_2, G2 = edge_distribution_to_bipartite_network(edges[2], edges[3], ("buyer", "seller"), id_generator)
    # pos = nx.bipartite_layout(G, node_1)

    # nx.draw(
    #     G,
    #     pos = pos,
    #     node_color = ['r'] * node_n + ['b'] * node_n,
    #     alpha = 0.5,
    #     node_size =[ deg * 40 for deg in dict(G.degree).values()]
    # )
    # plt.show()

    combined = generate_cross_broader_bipartite(G1, G2)

    nx.draw(combined)