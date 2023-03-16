from src.model import TestModel, ThesisModel
from src.schedule import TestScheduler, ThesisScheduler
from src.network_creation import (
    edge_distribution_to_bipartite_network,
    generate_degree_from_prob_list,
    get_probability_array_for_agents,
    generate_cross_broader_bipartite)
import numpy as np
from functools import partial
from itertools import count
"""
Logging configuration
"""
import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger('structure')
logger.setLevel(logging.DEBUG)

# custom_scheduler = TestScheduler
# model = TestModel(N=30, scheduler_constructor=custom_scheduler)


node_n = 10
avg_edge = 5
total_edge = node_n * avg_edge

distribution_function = partial(np.random.exponential, scale=1)
edges = []
population = [1,1,0.5, 0.5]
for i in range(4):
    edges.append(generate_degree_from_prob_list(
    int( total_edge * population[i]),
    get_probability_array_for_agents( int( node_n * population[i]), distribution_function)))

id_generator = count()
node_1, G1 = edge_distribution_to_bipartite_network(edges[0], edges[1], ("buyer", "seller"), id_generator, country = "home")
node_2, G2 = edge_distribution_to_bipartite_network(edges[2], edges[3], ("buyer", "seller"), id_generator, country = "foreign")

node_refs, combined = generate_cross_broader_bipartite(G1, G2, international_level=0.8)

custom_scheduler = ThesisScheduler
model = ThesisModel(N=30, cross_border_payment_network=combined)
for i in range(5):
    model.step()