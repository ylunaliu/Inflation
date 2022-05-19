from venv import create
from find_injectable_sets import find_injectable_sets
from os import dup
from platform import node
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools
from find_expressible_sets import find_expressible_sets
from sympy.physics.quantum import TensorProduct
from maximum_expressible_set import maximum_expressible
from create_all_support import create_support
import create_all_support

# Now I have the injectable sets and the expressible sets
sprial_inflation = nx.DiGraph()
sprial_inflation.add_edges_from([("X2", "C2"), ("Z2", "B2"), ("Y2", "A2"),
                            ("X1", "A2"), ("X1", "A1"), ("X1", "C1"), 
                            ("Y1", "A1"), ("Y1", "B1"), ("Y1", "B2"), 
                            ("Z1", "C1"), ("Z1", "B1"), ("Z1", "C2")])

sprial_inflation_hidden = list(["X2", "Y2", "Z2", "X1", "Y1", "Z1"])

injectable_sets_max, injectable_sets1, dictionary = find_injectable_sets(sprial_inflation, sprial_inflation_hidden)
expressible = find_expressible_sets(injectable_sets1, dictionary)
# print(expressible)
maximum_expressible_sets = maximum_expressible(expressible)
# print(f"here is the maximum injectable_sets {injectable_sets_max}")
# print(f"here is the maximum_expressible_sets {maximum_expressible_sets}")
sprial2 = sprial_inflation.copy()
sprial2.remove_nodes_from(sprial_inflation_hidden)


def break_marginal(support):
    # Given a support, break to marginal for different nodes
    marginal_original_node = []
    for i in range(support.shape[1]):
        marginal_original_node.append(support[:,i])
    return np.array(marginal_original_node)

w_support = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
orginal_node = ["A", "B", "C"]

marginal_original_node = break_marginal(w_support)
# slices of support for each node
dictionary_margin = dict(zip(orginal_node, marginal_original_node))

# Now I need to get all combinations of marginal for nodes in injectable sets 
injectable = ["A1", "B1"]

def find_marginal_support_given_injectable_set(injectable_set):
    marginal_injectable_set = []
    for element in injectable_set:
        marginal_injectable_set.append(dictionary_margin[element[0]])
    marginal_injectable_set= np.array(marginal_injectable_set).T
    return marginal_injectable_set

def dictionary_marginal(injectable_sets):
    key_dictionary_marginal = {}
    for every_injectable_set in injectable_sets:
        key_dictionary_marginal[str(every_injectable_set)] = find_marginal_support_given_injectable_set(every_injectable_set)
    return key_dictionary_marginal

key_dictionary_marginal= dictionary_marginal(injectable_sets_max)
# print(key_dictionary_marginal)
# print(key_dictionary_marginal[str(injectable_sets1[1])])
node_support = np.sort(np.array(sprial2.nodes))
supports = create_support(node_support,2)
# print(supports)

# Now I have all the support, and I have a way to get the marginals for each injectable sets, I need to find the non compatibe injectable sets
# print(injectable_sets1[1])

# Now I have the dictionary for storing the not possible marginal for all the maximum injectable sets
dictionary_not_possible = create_all_support.create_dictionary_for_all_injectable_set_not_possible(injectable_sets_max, key_dictionary_marginal)
# print(dictionary_not_possible)

create_all_support.rule_out_infeasible_due_to_injectable_sets(dictionary_not_possible, injectable_sets_max, supports, node_support)


