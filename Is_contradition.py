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
from utiles_reject_forbidden_events import create_support
import utiles_reject_forbidden_events
import utiles

def is_condraction_for_support_given_inflation(the_support_to_test, inflation_graph, inflation_graph_hidden_nodes, orginal_nodes):

    # Find it's injectable set
    injectable_sets_max, injectable_sets1, dictionary = find_injectable_sets(inflation_graph, inflation_graph_hidden_nodes)
    # print(f"This is the maximum injectable set{injectable_sets_max}")

    # Find it's expressible_sets
    expressible = find_expressible_sets(injectable_sets1, dictionary)
    # print(f"This is the maximum expressible set{expressible}")

    # Find it's maximum expressible_sets
    maximum_expressible_sets, acc_joined = maximum_expressible(expressible)

    # Basically I need name of the nodes
    sprial2 = inflation_graph.copy()
    sprial2.remove_nodes_from(inflation_graph_hidden_nodes)

    # Break down the marginals
    marginal_original_node = utiles.break_marginal(the_support_to_test)

    # Make dictionary for each of the marginals
    dictionary_margin = dict(zip(orginal_nodes, marginal_original_node))

    # Dictionary for checking the marginals for injectabke sets
    injectable_sets_dictionary_marginals= utiles.dictionary_marginal_injectable(injectable_sets_max, dictionary_margin)
    # print(f"this is the marginals for injectble sets{injectable_sets_dictionary_marginals}")

    # Create all supports that's possible for the given inflation
    node_support = np.sort(np.array(sprial2.nodes))
    supports = create_support(node_support,np.unique(the_support_to_test))

    # Not possible marginal for all the maximum injectable sets
    dictionary_not_possible = utiles_reject_forbidden_events.create_dictionary_for_all_injectable_set_not_possible(injectable_sets_max, injectable_sets_dictionary_marginals, np.unique(the_support_to_test))
    print(f"here is the not possible marginals {dictionary_not_possible}")
    # Generate all non-forbidden event
    event_non_forbidden = utiles_reject_forbidden_events.rule_out_forbidden_events_due_to_injectable_sets(dictionary_not_possible, injectable_sets_max, supports, node_support)
    print(event_non_forbidden)
    dictionary_event_non_forbidden = dict(zip(node_support, event_non_forbidden))
    display_events = np.vstack((node_support, event_non_forbidden))
    print(f"This is the nonforbidden events:\n {display_events}")

    # Dictionary contain the marginals for all the expressible sets
    key_dictionary_marginal_expressible = utiles.dictionary_marginal_expressible(maximum_expressible_sets, dictionary_margin)
    # print(f"this is the marginals for expressible sets{key_dictionary_marginal_expressible}")

    # Break down the marginals
    marginals_nonforbidden_event = utiles.break_marginal(event_non_forbidden)

    # Create the dictionary for marginals for all the compatible support
    dictionary_margin_compatibe_all_nodes = dict(zip(node_support,  marginals_nonforbidden_event ))
    dictionay_non_forbidden_events = utiles.make_dictionary_for_nonforbidden_expressible_marginals(maximum_expressible_sets, acc_joined, dictionary_margin_compatibe_all_nodes)
    # print(f"this is the marginals for expressible sets on non forbi{dictionay_non_forbidden_events}")

    is_contradition = utiles.check_for_contracdition(dictionay_non_forbidden_events, key_dictionary_marginal_expressible, maximum_expressible_sets)

    return injectable_sets_dictionary_marginals, dictionary_not_possible, injectable_sets_max, event_non_forbidden
if __name__ == "__main__":
    # Given an inflation graph
    spiral_inflation = nx.DiGraph()
    spiral_inflation.add_edges_from([("X2", "C2"), ("Z2", "B2"), ("Y2", "A2"),
                                ("X1", "A2"), ("X1", "A1"), ("X1", "C1"),
                                ("Y1", "A1"), ("Y1", "B1"), ("Y1", "B2"),
                                ("Z1", "C1"), ("Z1", "B1"), ("Z1", "C2")])
    spiral_inflation_hidden = list(["X2", "Y2", "Z2", "X1", "Y1", "Z1"])

    # cut_inflation = nx.DiGraph()
    # cut_inflation.add_edges_from([("Y2", "A2"), ("X1", "A2"), ("X1", "C1"), ("Z1", "C1"), ("Z1", "B1"), ("Y1", "B1")])
    # cut_inflation_hidden = list(["Y1", "Y2", "X1", "Z1"])

    w_support = np.array([[0, 0, 1], [0,1,0], [1,0,0]])
    orginal_node = ["A", "B", "C"]


    # ring_six_inflation = nx.DiGraph()
    # ring_six_inflation.add_edges_from([("X1", "A1"), ("X1", "B1"), ("Y1", "B1"), ("Y1", "C1"), 
    #                                    ("Z1", "C1"), ("Z1", "A2"), ("X2", "A2"), ("X2", "B2"),
    #                                    ("Y2", "B2"), ("Y2", "C2"), ("Z2", "C2"), ("Z2", "A1")])
    # ring_six_inflation_hidden = list(["X1", "X2", "Y1", "Y2", "Z1", "Z2"])
    injectable_sets_dictionary_marginals, dictionary_not_possible, injectable_sets_max, event_non_forbidden= is_condraction_for_support_given_inflation(w_support, spiral_inflation, spiral_inflation_hidden, orginal_node)
    
    # constraint_injectable_1 = []
    # constraint_injectable_0 = []
    
    # for injectable_set in injectable_sets_max:
    #     # print(dictionary_not_possible[str(injectable_set)])
    #     for marginals in injectable_sets_dictionary_marginals[str(injectable_set)]:
    #         constraint_injectable_1.append([injectable_set, list(marginals)])
    #     for marginals2 in dictionary_not_possible[str(injectable_set)]:
    #         constraint_injectable_0.append([injectable_set, list(marginals2)])
        