from distutils.command import check
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
import utiles_expressible

# Now I have the injectable sets and the expressible sets
sprial_inflation = nx.DiGraph()
sprial_inflation.add_edges_from([("X2", "C2"), ("Z2", "B2"), ("Y2", "A2"),
                            ("X1", "A2"), ("X1", "A1"), ("X1", "C1"), 
                            ("Y1", "A1"), ("Y1", "B1"), ("Y1", "B2"), 
                            ("Z1", "C1"), ("Z1", "B1"), ("Z1", "C2")])

sprial_inflation_hidden = list(["X2", "Y2", "Z2", "X1", "Y1", "Z1"])

injectable_sets_max, injectable_sets1, dictionary = find_injectable_sets(sprial_inflation, sprial_inflation_hidden)
expressible = find_expressible_sets(injectable_sets1, dictionary)
maximum_expressible_sets, acc_joined = maximum_expressible(expressible)


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

# # Now I need to get all combinations of marginal for nodes in injectable sets 

def find_marginal_support_given_injectable_set(injectable_set,dictionary_marginal):
    marginal_injectable_set = []
    # print(f"here is the injectable set{injectable_set}")
    for element in injectable_set:
        # print(f"here is the element{element}")
        marginal_injectable_set.append(dictionary_marginal[element[0]])
        # print(f"here is checking for dictionary{dictionary_marginal[element[0]]}")
    marginal_injectable_set= np.array(marginal_injectable_set).T
    marginal_injectable_set = np.array(list(((map(np.asarray, set(map(tuple, marginal_injectable_set)))))))
    return marginal_injectable_set

def dictionary_marginal(injectable_sets):
    key_dictionary_marginal = {}
    for every_injectable_set in injectable_sets:
        key_dictionary_marginal[str(every_injectable_set)] = find_marginal_support_given_injectable_set(every_injectable_set,dictionary_margin)
    return key_dictionary_marginal

key_dictionary_marginal= dictionary_marginal(injectable_sets_max)
node_support = np.sort(np.array(sprial2.nodes))
supports = create_support(node_support,2)

# Now I have all the support, and I have a way to get the marginals for each injectable sets, I need to find the non compatibe injectable sets
# print(injectable_sets1[1])

# Now I have the dictionary for storing the not possible marginal for all the maximum injectable sets
dictionary_not_possible = create_all_support.create_dictionary_for_all_injectable_set_not_possible(injectable_sets_max, key_dictionary_marginal)
# print(dictionary_not_possible)

support_compatible = create_all_support.rule_out_infeasible_due_to_injectable_sets(dictionary_not_possible, injectable_sets_max, supports, node_support)

def dictionary_marginal_expressible(expressble_sets,dictionary_margin):
    key_dictionary_marginal_expressible = {}
    for i, every_expressible_set in enumerate(expressble_sets):
        separate_marginals_expressible = find_marginals_expressible_set(every_expressible_set, dictionary_margin)
        key_dictionary_marginal_expressible[str(expressble_sets[i])] = utiles_expressible.marginals_expressible_full(separate_marginals_expressible, len(every_expressible_set))
    return key_dictionary_marginal_expressible

def find_marginals_expressible_set(expressible_set, dictionary_margin):
    """
    Given an expressible set in the form [['A2', "B2"], ['C2']]
    return an array contains the marginals
    """
    list4 = []
    for injectable in expressible_set:
        # #injecable chou be ["A1", "B1"] or [A1]
        # for node in injectable:
        #     print(node)
        list4.append(find_marginal_support_given_injectable_set(injectable, dictionary_margin))
    
    return(list4)
            
#Now I have the feasible support, I have to check them against marginals of the expressible sets

# test_expressible_sets1= [['A2', 'B2'], ['C2']]
# separate_marginals_expressible = find_marginals_expressible_set(test_expressible_sets1)
# utiles_expressible.marginals_expressible_full(separate_marginals_expressible, len(test_expressible_sets1))


key_dictionary_marginal_expressible = dictionary_marginal_expressible(maximum_expressible_sets, dictionary_margin)
# print(key_dictionary_marginal_expressible)
# print(key_dictionary_marginal_expressible[str(maximum_expressible_sets[0])])
# print()

marginals_compatible = break_marginal(support_compatible)

def find_marginal_support_given_joined_expressible_set(expressible_set, expressible_set_joined, dictionary_marginal):
    marginal_injectable_set = []
    # print(f"here is the expressible set{expressible_set}")
    # print(f"here is the joined expressible set{expressible_set_joined}")
    for i, element in enumerate(expressible_set_joined):
        # print(f"here is the element{element}")
        marginal_injectable_set.append(dictionary_marginal[element])
        # print(f"here is checking for dictionary{dictionary_marginal[element]}")
    marginal_injectable_set= np.array(marginal_injectable_set).T
    marginal_injectable_set = np.array(list(((map(np.asarray, set(map(tuple, marginal_injectable_set)))))))
    return marginal_injectable_set

def make_dictionary_for_compatible_expressible_marginals(expressible_sets, expressible_sets_joined, dictionary_margin_compatible_all_nodes):
    dictionary = {}
    for i, expressible_set in enumerate(expressible_sets):
        marginal_expressible_compatible = find_marginal_support_given_joined_expressible_set(expressible_set, expressible_sets_joined[i], dictionary_margin_compatible_all_nodes)
        dictionary[str(expressible_set)] = marginal_expressible_compatible
    return dictionary

def check_for_contracdition(dictionary_marginals_compatible, dictionary_marginals_expreesbile, expressible_sets):
    is_expressible_not_compelete = []
    for expressible_set in expressible_sets:
        is_expressible_not_compelete.append(len(dictionary_marginals_compatible[str(expressible_set)])< len(dictionary_marginals_expreesbile[str(expressible_set)]))
    
    if(True in is_expressible_not_compelete):
        print("We reach a contraction, the support is not compatible with given inflation")
        return False
    else:
        print("No condraction found for the support given this inflation")
        return True
# slices of support for each node
dictionary_margin_compatibe_all_nodes = dict(zip(node_support, marginals_compatible))


# Ok, now I need to take the compatible supports and produce their marginals as dictionay
dictionay_comptible = make_dictionary_for_compatible_expressible_marginals(maximum_expressible_sets, acc_joined, dictionary_margin_compatibe_all_nodes)


# Now I have two dictionaries, one is for the marginals of expressible sets for the compatible support and one is marginals of the expressible sets
# marginal = find_marginal_support_given_injectable_set(["A"])

# print(marginal)