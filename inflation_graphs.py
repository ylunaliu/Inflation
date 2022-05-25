from os import dup
from platform import node
import string
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools
from itertools import chain

from sqlalchemy import intersect
import utiles_reject_forbidden_events
import utiles
import class_inflation_graph
def intersect2D(a, b):
  """
  Find row intersection between 2D numpy arrays, a and b.
  Returns another numpy array with shared rows
  """
  return np.array([x for x in set(tuple(x) for x in a) & set(tuple(x) for x in b)])

def non_forbidden_given_more_graphs(list_of_graphs, list_of_hidden_nodes, support, original_nodes):
    #TODO: In this case it is only compatible with the same number of nodes, need to make it more general to be compatible with 
    #      different inflation graphs
    
    # The thing with the combination of supports is that more nodes more combinations, should I just take the maximum number of nodes and get all the supports from there?
    # Or I can generate non forbidden support for all inflation then compare instead of ruling out from the last graph
    non_forbidden_events_all_graphs = []
    numebr_of_nodes_all_graphs = []
    for i, graph in enumerate(list_of_graphs):
        non_forbidden_event, number_of_nodes = find_non_forbidden_events(graph, list_of_hidden_nodes[i], support, original_nodes)
        non_forbidden_events_all_graphs.append(non_forbidden_event)
        numebr_of_nodes_all_graphs.append(number_of_nodes)

    # print(non_forbidden_events_all_graphs[0][:,0:3])
    print(non_forbidden_events_all_graphs)
    
    test1 = intersect2D(non_forbidden_events_all_graphs[0], non_forbidden_events_all_graphs[1])
    print(test1)
    test2 = []
    for element in test1:
        for i in non_forbidden_events_all_graphs[2]:
            if(np.array_equal(element[0:3], i)):
                test2.append(element)
    print(np.array(test2))
    # for i in range(len(non_forbidden_events_all_graphs)):
    #     s


def find_non_forbidden_events(graph, hidden_nodes, support, original_nodes):
    graph_object = class_inflation_graph.Inflation_graph(graph, hidden_nodes)
    number_of_nodes = graph_object.number_of_nodes
    print(f"here is the number of nodes{number_of_nodes}")
    # Break down the marginals
    marginal_original_node = utiles.break_marginal(support)

    # Make dictionary for each of the marginals
    dictionary_margin = dict(zip(original_nodes, marginal_original_node))

    injectable_sets_dictionary_marginals= utiles.dictionary_marginal_injectable(graph_object.maximum_injectable_sets, dictionary_margin)
    
    supports = utiles_reject_forbidden_events.create_support(graph_object.observednodes,np.unique(support)) #maybe should move 1 level up
    print(f"here is the support{supports}")
       
    # Not possible marginal for all the maximum injectable sets
    dictionary_not_possible = utiles_reject_forbidden_events.create_dictionary_for_all_injectable_set_not_possible(graph_object.maximum_injectable_sets, injectable_sets_dictionary_marginals, np.unique(support))

    # Generate all non-forbidden event
    event_non_forbidden = utiles_reject_forbidden_events.rule_out_forbidden_events_due_to_injectable_sets(dictionary_not_possible, graph_object.maximum_injectable_sets, supports, graph_object.observednodes)
    display_events = np.vstack((graph_object.observednodes, event_non_forbidden))
    print(f"here is the non_forbidden events:{display_events}")
    return event_non_forbidden, number_of_nodes

if __name__ == "__main__":
    # Given an inflation graph
    sprial_inflation = nx.DiGraph()
    sprial_inflation.add_edges_from([("X2", "C2"), ("Z2", "B2"), ("Y2", "A2"),
                            ("X1", "A2"), ("X1", "A1"), ("X1", "C1"), 
                            ("Y1", "A1"), ("Y1", "B1"), ("Y1", "B2"), 
                            ("Z1", "C1"), ("Z1", "B1"), ("Z1", "C2")])

    sprial_inflation_hidden = list(["X2", "Y2", "Z2", "X1", "Y1", "Z1"])

    cut_inflation = nx.DiGraph()
    cut_inflation.add_edges_from([("Y2", "A1"), ("X1", "A1"), ("X1", "C1"), ("Z1", "C1"), ("Z1", "B1"), ("Y1", "B1")])
    cut_inflation_hidden = list(["Y1", "Y2", "X1", "Z1"])


    ring_six_inflation = nx.DiGraph()
    ring_six_inflation.add_edges_from([("X1", "A1"), ("X1", "B1"), ("Y1", "B1"), ("Y1", "C1"), 
                                       ("Z1", "C1"), ("Z1", "A2"), ("X2", "A2"), ("X2", "B2"),
                                       ("Y2", "B2"), ("Y2", "C2"), ("Z2", "C2"), ("Z2", "A1")])
    ring_six_inflation_hidden = list(["X1", "X2", "Y1", "Y2", "Z1", "Z2"])


    w_support = np.array([[1, 0, 0],[0, 1, 0], [0, 0, 1]])
    orginal_node = ["A", "B", "C"]

    list_of_graphs = list([sprial_inflation, ring_six_inflation, cut_inflation])
    print(len(list_of_graphs))
    print(list_of_graphs)
    list_of_hidden_nodes = list([sprial_inflation_hidden, ring_six_inflation_hidden, cut_inflation_hidden])

    non_forbidden_given_more_graphs(list_of_graphs, list_of_hidden_nodes, w_support, orginal_node)