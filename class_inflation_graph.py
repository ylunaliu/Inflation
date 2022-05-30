from os import dup
from platform import node
import string
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools
from itertools import chain
import find_injectable_sets
class Inflation_graph:
    def __init__(self, graph, hidden_nodes):
        self.nodes = list(graph.nodes)
        self.hidden_nodes = hidden_nodes
        self.graph = graph
        self.observednodes = np.sort(list(set(self.nodes).difference(self.hidden_nodes)))
        self.number_of_nodes = len(self.observednodes)
        self.maximum_injectable_sets = find_injectable_sets.find_injectable_sets(graph, self.hidden_nodes)[0]
        self.injectable_sets = find_injectable_sets.find_injectable_sets(graph, self.hidden_nodes)[1]
        self.ancestor_dic = find_injectable_sets.find_injectable_sets(graph, self.hidden_nodes)[2]


if __name__ == "__main__":
    sprial_inflation = nx.DiGraph()
    sprial_inflation.add_edges_from([("X2", "C2"), ("Z2", "B2"), ("Y2", "A2"),
                            ("X1", "A2"), ("X1", "A1"), ("X1", "C1"), 
                            ("Y1", "A1"), ("Y1", "B1"), ("Y1", "B2"), 
                            ("Z1", "C1"), ("Z1", "B1"), ("Z1", "C2")])

    sprial_inflation_hidden = list(["X2", "Y2", "Z2", "X1", "Y1", "Z1"])

    inflation = Inflation_graph(sprial_inflation, sprial_inflation_hidden)
    print(inflation.ancestor_dic)
