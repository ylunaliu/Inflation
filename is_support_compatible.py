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

def break_marginal(support):
    # Given a support, break to marginal for different nodes
    marginal_original_node = []
    for i in range(support.shape[1]):
        marginal_original_node.append(support[:,i])
    return np.array(marginal_original_node)


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

def dictionary_marginal(injectable_sets, dictionary_margin):
    key_dictionary_marginal = {}
    for every_injectable_set in injectable_sets:
        key_dictionary_marginal[str(every_injectable_set)] = find_marginal_support_given_injectable_set(every_injectable_set,dictionary_margin)
    return key_dictionary_marginal


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
        list4.append(find_marginal_support_given_injectable_set(injectable, dictionary_margin))
    
    return(list4)
            

def find_marginal_support_given_joined_expressible_set(expressible_set, expressible_set_joined, dictionary_marginal):
    marginal_injectable_set = []
    for i, element in enumerate(expressible_set_joined):
        marginal_injectable_set.append(dictionary_marginal[element])
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
        print("We reach a contradition, the support is not compatible with given inflation")
        return False
    else:
        print("No contradtion found for the support given this inflation")
        return True

