from os import dup
from platform import node
import string
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools
from itertools import chain


def find_injectable_sets(graph, hidden_nodes):

    # Get all the nodes from graph
    nodes = list(graph.nodes)

    #Get all the observed nodes
    nodes_observed = remove_element_list(hidden_nodes, nodes)
    
    nodes_ancestor = []
    for node in nodes_observed:
        ancestors = list(nx.ancestors(graph, node))
        split_index = []
        split_key = []
        for i in range(len(ancestors)):
            splita = split(ancestors[i])
            split_key.append(splita[0])
            split_index.append(splita[1])
            diction = dict(zip(split_key, split_index))
        nodes_ancestor.append(diction)
  
    # Get the arrays of ancestor correspond to each nodes
    nodes_ancestor = np.array(list(nodes_ancestor))

    # Dictionary key:node, value: ancestor
    dictionary = dict(zip(nodes_observed, nodes_ancestor))

    # Get all combination that could be useful to construct the subgraph for injectable sets
    combinations = list(itertools.combinations(nodes_observed,2))

    # Build a subgraph for injectable graph
    sprial_injectable = nx.Graph()
    sprial_injectable.add_nodes_from(nodes_observed)

    injectable_pair = []
    for sets in combinations:
        # Ancestor_1 is a dictionary {'Z': '1', 'X': '1'}
        ancestor_1 = dictionary[sets[0]]
        ancestor_1_key = [*ancestor_1]
        # print([*ancestor_1])
        ancestor_2 = dictionary[sets[1]]
        ancestor_2_key = [*ancestor_2]
        # print(ancestor_2)
        if(not set(ancestor_1_key).isdisjoint(ancestor_2_key)):
            # Find the duplicate 
            duplicate_node = list(set(ancestor_2_key).intersection(ancestor_1_key))
            # print(f'The duplicate_node for {sets} is {duplicate_node}')
            index_node = []
            boolean_set = []
            for node in duplicate_node:
                boolean_set.append(ancestor_1[node]!=ancestor_2[node])
            if(not True in boolean_set):
                injectable_pair.append(sets)
    
    sprial_injectable.add_edges_from(injectable_pair)
    injectable_sets = list(nx.find_cliques(sprial_injectable))
    result = np.unique(list(chain.from_iterable(injectable_sets)))
    for element in result:
        injectable_sets.append([element])

    return injectable_sets, dictionary



def split(word):
    return [char for char in word]

def remove_element_list(list1, list2):
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
    injectable_sets, dictionary = find_injectable_sets(sprial_inflation, sprial_inflation_hidden)
    print(injectable_sets)
    
