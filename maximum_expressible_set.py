from ssl import ALERT_DESCRIPTION_BAD_RECORD_MAC
from find_injectable_sets import find_injectable_sets
from os import dup
from platform import node
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools
from find_expressible_sets import find_expressible_sets

def append_list(expressible_set):
    """
    Description: flatten the expresisble_sets list, produce a sigle list with all nodes in an expressible set

    Parameters:
    -----------
    expressible set: A List of lists, A signle expressible set
    """
    joined_list = []
    for i in range(len(expressible_set)):
        joined_list.extend(expressible_set[i])
    return joined_list


def maximum_expressible(expressible_set):   
    """ 
    Description: Find the maximum expressible sets when given an complete expressible sets

    Parameters:
    ------------
    expressible_set: A list of lists, the expressible sets, 
   
    Return
    ------------
    acc: A list of lists, the maximum expressible set. For example: [[['C2', 'B1'], ['A2']]], means C2B1 is expressible with A2
    acc_joined: A list of lists, with the format of maximum expressible set being appended, ['C2', 'B1', 'A2']
    """

    # accumulator used to store all the maximum expressible set
    acc = []
    # accumulator used to store all the flattened maximum expressible set
    acc_joined = []

    for each_expressible_set in expressible_set:
        joined = append_list(each_expressible_set)
        
        if(acc == []): #If the acc is empty put the first one into the accumulator
            acc.append(each_expressible_set)
            acc_joined.append(joined)

        # Initialized the boolean flag
        boolean_ifsubset = False
        for i, element in enumerate(acc_joined):
            if(set(joined).issubset(set(element))):
                # if(len(joined)==len(acc_joined[i]) and (joined_num_node - joined_num)<(len(acc_joined[i])-len(acc[i]))):
                #     acc.remove(acc[i])
                #     acc.append(each_expressible_set)
                #     acc_joined.append(joined)
                #     acc_joined.remove(element)
                boolean_ifsubset = False # If the joined element is a subset of the one in the list, keep the one in the list
                break
            else: #otherwise, remove the element in the list, set the flag
                if(set(element).issubset(set(joined))): 
                    acc.remove(acc[i])
                    acc_joined.remove(element)
                boolean_ifsubset = True
                
        if(boolean_ifsubset):   # add the joined expressible set and expressible set to the list
            acc.append(each_expressible_set)
            acc_joined.append(joined)
 
    return acc, acc_joined
if __name__ == "__main__":
    sprial_inflation = nx.DiGraph()
    sprial_inflation.add_edges_from([("X2", "C2"), ("Z2", "B2"), ("Y2", "A2"),
                            ("X1", "A2"), ("X1", "A1"), ("X1", "C1"), 
                            ("Y1", "A1"), ("Y1", "B1"), ("Y1", "B2"), 
                            ("Z1", "C1"), ("Z1", "B1"), ("Z1", "C2")])

    sprial_inflation_hidden = list(["X2", "Y2", "Z2", "X1", "Y1", "Z1"])

    injectable,maximum_injectable_sets1, dictionary = find_injectable_sets(sprial_inflation, sprial_inflation_hidden)
    expressible = find_expressible_sets(maximum_injectable_sets1, dictionary)
    print(f"here is the expressible set{expressible}")

    expressible_test4 = [[['B1', 'C2'], ['A2']], [['B1'], ['A2']]]
    acc,acc_joined= maximum_expressible(expressible)
    print(f"here is the maximum expressible set{acc},")
