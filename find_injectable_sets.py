from os import dup
from platform import node
import string
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools
from itertools import chain


def find_injectable_sets(graph, hidden_nodes):
    """ 
    Description: Find all injectable sets when given an inflation graph and it's hidden_nodes

    Paramaters:
    ------------
    graph: A networkx directed graph object <class 'networks.classes.digraph.DiGraph'>

    hidden_nodes: A list of hidden nodes. <class 'list'> in the format ["node1", "node2", "node3"]
   
    Return
    ------------
    injectable_sets_max:  A list of lists containing the maximum injectable_sets <class 'list'> in the format [[injectable_set1], [injectable_set2]]

    injectable_sets: A list of lists containg all the injectable sets <class 'list'>

    dictionary: A dictionary containing all the observed nodes and it's ancestor.
        - Key: string, name of the node
        - Value: dictionary, all the ancestors
            - The ancestors is divide into Letter and index
        TODO: !!! Need to generalize this at some point, not compatibe with index greater than 10
    """

    # Get all the nodes from graph
    nodes = list(graph.nodes)

    # Get all the observed nodes
    nodes_observed = remove_element_list(hidden_nodes, nodes)
    
    # Get all the ancestors for every node with splitting
    nodes_ancestor = []
    for node in nodes_observed:
        ancestors = list(nx.ancestors(graph, node))
        split_index = []
        split_key = []
        for i in range(len(ancestors)):
            split_node = split(ancestors[i]) # Split the nodes, if I need to do TODO at some point need to modify the split function 
            split_key.append(split_node[0])
            split_index.append(split_node[1])
            diction = dict(zip(split_key, split_index))
        nodes_ancestor.append(diction)

  
    # Get the arrays of ancestor correspond to each nodes
    nodes_ancestor = np.array(list(nodes_ancestor))

    # Dictionary key:node, value: ancestor
    dictionary = dict(zip(nodes_observed, nodes_ancestor))

    # Get all combination that could be useful to construct the subgraph for injectable sets
    combinations = list(itertools.combinations(nodes_observed,2))

    # Build a subgraph for injectable graph
    subgraph_injectable = nx.Graph()
    subgraph_injectable.add_nodes_from(nodes_observed)

    # Find injectable pair
    injectable_pair = []
    for sets in combinations:
        # Ancestor_1 is a dictionary {'Z': '1', 'X': '1'}
        ancestor_1 = dictionary[sets[0]]
        ancestor_1_key = [*ancestor_1] # Get all the keys

        ancestor_2 = dictionary[sets[1]]
        ancestor_2_key = [*ancestor_2]

        # If there share the ancestor, check for the index
        if(not set(ancestor_1_key).isdisjoint(ancestor_2_key)):
            # Find the duplicate, need further checking for index 
            duplicate_node = list(set(ancestor_2_key).intersection(ancestor_1_key))
            boolean_set = []
            for node in duplicate_node:
                boolean_set.append(ancestor_1[node]!=ancestor_2[node])
            if(not True in boolean_set):
                injectable_pair.append(sets)
    
    # Add edges if two nodes are injectable
    subgraph_injectable.add_edges_from(injectable_pair)

    # Find cliques, if cliques -> it's a injectable set
    injectable_sets = list(nx.find_cliques(subgraph_injectable))

    # Not sure if this is necessary, TODO: Double check with Elie for injectable set and expressible set if the if statement is needed
    for injectable_set in injectable_sets:
        if(len(injectable_sets)==1):
            injectable_sets.remove(injectable_set)

    # This is the maximum injectable sets
    injectable_sets_max = injectable_sets.copy() 

    # This is all injectable sets
    result = np.unique(list(chain.from_iterable(injectable_sets)))
    for element in result:
        injectable_sets.append([element])

    return injectable_sets_max, injectable_sets, dictionary



def split(word):
    """
    Descrption: used to split the node name

    Parameter:
    ------------
    word: str

    Return:
    ------------
    A list containing all characters of the word
    """
    return [char for char in word]

def remove_element_list(list1, list2):
    """
    Descrption: used to remove list1 from list2

    Parameter:
    ------------
    list1: list
    list2: list

    Return:
    ------------
    A list after remove list1 from list2
    """
    new_sets = list(set(list2).difference(list1))

    return new_sets
if __name__ == "__main__":
    sprial_inflation = nx.DiGraph()
    sprial_inflation.add_edges_from([("X2", "C2"), ("Z2", "B2"), ("Y2", "A2"),
                                ("X1", "A2"), ("X1", "A1"), ("X1", "C1"), 
                                ("Y1", "A1"), ("Y1", "B1"), ("Y1", "B2"), 
                                ("Z1", "C1"), ("Z1", "B1"), ("Z1", "C2")])
    sprial_inflation_hidden = list(["X2", "Y2", "Z2", "X1", "Y1", "Z1"])

    cut_inflation = nx.DiGraph()
    cut_inflation.add_edges_from([("Y2", "A2"), ("X1", "A2"), ("X1", "C1"), ("Z1", "C1"), ("Z1", "B1"), ("Y1", "B1")])
    cut_inflation_hidden = list(["Y1", "Y2", "X1", "Z1"])
    injectable_sets_max, injectable_sets, dictionary = find_injectable_sets(sprial_inflation, sprial_inflation_hidden)
    print(dictionary)
    
