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

def create_support(nodes, bit):
    """
    given list of sorted nodes, create all possible support given number of bits
    """
    return np.array(list(itertools.product([0,1],repeat=len(nodes))))

def create_not_possible_support_given_injectable_sets(injectable_set, marginal, bits):
    """
    input: A injectable set
           The injectable set's marginals on the support
    output: The not possible support
    """
    mariginal_all_support = create_support(injectable_set, bits)
    not_possible = np.array(list(set(map(tuple,mariginal_all_support)).difference(set(map(tuple,marginal)))))
    return not_possible

def create_dictionary_for_all_injectable_set_not_possible(injectable_sets, dictionary_injectable):
    """
    input: Injectable_sets: maximum injectable sets
           Dictionary_injectable_sets: A dictionary where is key is str(injectable_set) and value is the marginals
    
    outpur: A dictionary with key as the injectable set and value as the not possible marginals
    """
    dictionary_not_possible = {}
    for injectable_set in injectable_sets:
        # For each injectable_set, we need to find the not possible marginal
        marginals = dictionary_injectable[str(injectable_set)]
        not_possible = create_not_possible_support_given_injectable_sets(injectable_set, marginals, 2)
        dictionary_not_possible[str(injectable_set)] = not_possible
        
    return dictionary_not_possible

def cut_marginal_from_orginal_support(all_support, cutting_index):
    combined_marginals = []
    all_support_copy = list(all_support).copy()
    all_support_copy = np.array(all_support_copy)
    for i in range(len(cutting_index)):
        # print(f"here is the cutting index{cutting_index[i]} with {type(cutting_index[i])}")
        # print(all_support_copy)
        combined_marginals.append(all_support_copy[:,cutting_index[i]])

    # print(f"here is the combined marginals{np.array(combined_marginals).T}")
    return np.array(combined_marginals).T

def removing_infeasible_support(not_possible_supports, all_support, cutting_index):

    marginals = cut_marginal_from_orginal_support(all_support, cutting_index)
    # print(f"here is the cutting index:{cutting_index}")
    # print(f"here is the marginal{marginals}, with length{len(marginals)}")
    index_to_be_remove = []

    for not_possible_support in not_possible_supports:
        for index, element in enumerate(marginals):
           if(np.array_equal(element, not_possible_support)):
                index_to_be_remove.append(index)
 
    index_to_be_remove = set(index_to_be_remove)
    index_to_be_remove = np.array(list(index_to_be_remove))

    # print(f"index_to_be_remove{index_to_be_remove} and number of support {len(index_to_be_remove)}")
    return index_to_be_remove


def remove_from_index(all_support, index_to_keep):
    support_to_keep = []
    # print(f"here is the single index{index_to_keep[2]}")
    for index in index_to_keep:
        # print(f"here is the index{index}")
        # print(f"corresponding support{all_support[index]}")
        support_to_keep.append(list(all_support)[index])
    # print(f"here is the support_to_keep{len(support_to_keep)}")
    
    return np.array(support_to_keep)

def rule_out_infeasible_due_to_injectable_sets(dictionary_not_possible, injectable_sets, all_support, node_support):
    """
    Input: A dictionary with key as injectable set and value as the not possible support
           The maximum injectable sets
           The complete support for all_support
    Output: The remaining feasible support
    """
    index_to_be_remove = []
    for injectable_set in injectable_sets:
        # print(f"here is th injectable_set{injectable_set}")
        cutting_index = []
        not_possible_support = dictionary_not_possible[str(injectable_set)]
        # print(type(not_possible_support))
        # print(f"here is the not possible support{not_possible_support}")
        # print(not_possible_support[0])
        #Need to look for the index based on injectable_set
        for i in range(len(injectable_set)):
            cutting_index.append(list(node_support).index(injectable_set[i]))
        index_to_be_remove.extend(removing_infeasible_support(not_possible_support,all_support,cutting_index))
        # print(f"here is the index to be reomve{np.array(index_to_be_remove)} and the length: {len(index_to_be_remove)}")

    index_to_be_remove = list(set(index_to_be_remove))
    index_to_be_remove = np.array(index_to_be_remove)
    index = np.arange(0,len(all_support),1)
    index2 = np.array(list(set(index)^set(index_to_be_remove)))
    # Find the 

    support_compatible = remove_from_index(all_support, index2)
    return support_compatible
    # print(len(all_support1))
        #


    # marginals = cut_marginal_from_orginal_support(all_support, cutting_index)
    # print(marginals)
    # print(np.where(marginals==[0, 0]))
