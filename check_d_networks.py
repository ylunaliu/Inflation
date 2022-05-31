from platform import node
import networkx as nx
import numpy as np
import itertools
from toolz import unique

def d_separation_list(graph, hidden_nodes):
    # Graph is a directed graph object
    # hidden_nodes is a list contains the hidden variables in the from ["a", "b" ...]
    nodes = list(graph.nodes)
    
    if(hidden_nodes!=[]):
        for node in hidden_nodes:
            nodes.remove(node)

    # Get all combination of two nodes
    combination = list(itertools.combinations(nodes,2))

    # Get all combibation for set Z
    def powerset(input):
        output = sum([list(map(list, itertools.combinations(input, i))) for i in range(len(input) + 1)], [])
        return output
    d_separation_list1 = []
    # Get all the nodes:
    for i in range(len(combination)):
        # Now I get a pair of nodes I can regenerate the powerset for the nodes
        new_nodes = remove_element_list(list(combination[i]), list(nodes))
        sets_z = powerset(new_nodes)
        for_each_d_separation= []
        for j in range(len(sets_z)):
            if(nx.d_separated(graph, {combination[i][0]}, {combination[i][1]}, set(sets_z[j]))==True):
                for_each_d_separation.append([[combination[i][0]], [combination[i][1]], sets_z[j]])
        d_separation_list1.extend(for_each_d_separation)

    return d_separation_list1

def remove_element_list(list1, list2):
    new_sets = list(set(list2).difference(list1))
    return new_sets


def make_z_not_overlap_with_nodes(pair, sets_z):
    new_set = sets_z
    for element in pair:
        if element in new_set:
            new_set.remove(element)

    return new_set

if __name__ == "__main__":
    

    sprial_inflation = nx.DiGraph()
    sprial_inflation.add_edges_from([("X2", "C2"), ("Z2", "B2"), ("Y2", "A2"),
                                ("X1", "A2"), ("X1", "A1"), ("X1", "C1"), 
                                ("Y1", "A1"), ("Y1", "B1"), ("Y1", "B2"), 
                                ("Z1", "C1"), ("Z1", "B1"), ("Z1", "C2")])
    sprial_inflation_hidden = list(["X2", "Y2", "Z2", "X1", "Y1", "Z1"])

    # unrelated_confounders = nx.DiGraph()
    # unrelated_confounders.add_edges_from([("U1", "A"), ("U1", "D"), ("U2", "B"), ("U2", "D"), ("D", "A"), ("D", "B")])
    # unrelated_confounders_hidden = list(["U1", "U2"])

    # unrelated_confounders2 = nx.DiGraph()
    # unrelated_confounders2.add_edges_from([("U1", "A"), ("U1", "D"), ("U2", "B"), ("U2", "D"), ("D#", "A"), ("D#", "B")])
    # unrelated_confounders_hidden2 = list(["U1", "U2"])

    ring_six_inflation = nx.DiGraph()
    ring_six_inflation.add_edges_from([("X1", "A1"), ("X1", "B1"), ("Y1", "B1"), ("Y1", "C1"), 
                                       ("Z1", "C1"), ("Z1", "A2"), ("X2", "A2"), ("X2", "B2"),
                                       ("Y2", "B2"), ("Y2", "C2"), ("Z2", "C2"), ("Z2", "A1")])
    ring_six_inflation_hidden = list(["X1", "X2", "Y1", "Y2", "Z1", "Z2"])
    d = d_separation_list(sprial_inflation, sprial_inflation_hidden)
    print(d)

