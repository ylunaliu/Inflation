from sympy import evaluate, sec
from maximum_expressible_set import append_list
from ssl import ALERT_DESCRIPTION_BAD_RECORD_MAC
from os import dup
from platform import node
import sys
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools
from utiles_reject_forbidden_events import create_support
import utiles
from utiles import break_marginal
import check_d_networks
np.set_printoptions(threshold=sys.maxsize)

def all_d_separate_relations(d_separation_relations: list, marginals_dic):
    """
    Description: get the final containors, the largerst wrappers, for each d-separation-relaion, we get all combinations of value that the d-separation relation
                can take, then for each combinations, we get the value that the elements of the d-separation can take, then for each element, we get the events that
                satisfy the condition.
                List(All d-separation)relation) with size (num of d-separation-relations) of List(Combinations) with size(num(combinations)) of List(elements) with size 4 with List(events statsfy combinations)
    
    Parameters:
    ------------
    d-separation-relations: All d-separation relations to consider
    marginals_dic: A dictionary of marginals for the non-forbidden events
    """
    container = []
    for each_d_separation_relation in d_separation_relations:
        all = generate_formula_given_d_separation(each_d_separation_relation)
        second = all[1]
        combination_marginals,length = generate_combinations(second)
        container.append(get_all_possiblility(length, all, marginals_dic, event_non_forbidden,combination_marginals))
    return container

def generate_formula_given_d_separation(d_separation_relation: list):
    """
    Description: If A and B are d-separated by CD, the d_separation_relation should be in the format: [['A'], ['B'], ['C', 'D']]
                 The formula will be P(CD)P(ABCD) = P(ACD)P(BCD), there is always four elements of it. It will returns 
                 [["C", "D"], ["A", "B", "C", "D"], ["A", "C", "D], ["B", "C", "D"]]
    
    Parameters:
    ------------
    d_separation_relation: A list with the d-separation condition to considered [['A'], ['B'], ['C', 'D']]

    Return
    ------------
    list containing the four elements from the d-separation relations: P(CD)P(ABCD) = P(ACD)P(BCD)
                                                                       [["C", "D"], ["A", "B", "C", "D"], ["A", "C", "D], ["B", "C", "D"]]
    """
    first_element =  np.sort(d_separation_relation[2])
    second_element = np.sort(append_list(d_separation_relation))
    third_element = np.sort(append_list(list([d_separation_relation[0], d_separation_relation[2]])))
    fourth_element = np.sort(append_list(list([d_separation_relation[1], d_separation_relation[2]])))
    return list([first_element, second_element, third_element, fourth_element])

def get_marginals_non_forbidden_events(events, nodes:list):
    """
    Description: break the marginals for the non forbidden events according to the nodes

    Parameters:
    ------------
    events: A 2D numpy array, the non_forbidden events
    nodes: The visible nodes for the inflation graph

    Return
    ------------
    marginals_non_forbidden_dictionary: The dictionary contains the node and the marginals for that nodes
    """
    marginals_non_forbidden = break_marginal(events)
    marginals_non_forbidden_dictionary = dict(zip(nodes, marginals_non_forbidden))
    return marginals_non_forbidden_dictionary

def get_all_possiblility(length, list_of_elements, marginals_dic_elements, events_non_forbidden, combination_marginals):
    """
    Description: get all possibility of the value that the formula can take

    Parameters:
    ------------
    length: The number of combinations that second element that the d-separation relation can take
    list_of_elements: The list for the four elements for a d-separation relation
    marginals_dic_elements: the marginals of non-forbidden events for the observed nodes
    events_non_forbidden: the non-forbidden events
    combination_marginals: the marginals for the nodes in second elements

    Return:
    ------------
    containers: A list contain all the events with all possible combination 
                For example, P(CD)P(ABCD) = P(ACD)P(BCD), it will contains the events from A=a1, b=b1, c=c1, d=d1 to A=a16, B = b16, C=c16, D=d16
    """
    containers = []
    for i in range(length):
        events_for_formula = get_events_given_formula(list_of_elements, marginals_dic_elements, i, events_non_forbidden, combination_marginals)
        containers.append(events_for_formula)

    return containers

def get_events_given_formula(list_of_elements, marginals_dic_elements, i, events_non_forbidden, combination_maginals):
    """
    Description: For the four elements for a d-separation relation, for each elements find the events that satisfy the condition

    Parameters:
    ------------
    list_of_elements: The list for the four elements for a d-separation relation
    marginals_dic_elements: the marginals of non-forbidden events for the observed nodes
    i: the index to which of the combination we are looking for
    events_non_forbidden: the non-forbidden events
    combination_marginals: the marginals for the nodes in second elements

    Return:
    ------------
    results: A list contains [[all possible events for element1], [all possible events for element2], [all possible events for element3],  [all possible events for element4]]
             For example, P(CD)P(ABCD) = P(ACD)P(BCD) with A=a1, B=b1, C=c1, D=d1
             [[all possible events for C=c1, D=d1], [all possible events for A=a1, B=b1, C=c1, D=d1], [all possible events for A=a1, C=c1, D=d1], [all possible events for B=b1, C=c1, D=d1]
    """
    results = []
    # Loop through the elements
    for element in list_of_elements:
        print(f"This is the elemnt {element}")
        value_of_element = []
        # Get the specific value that this element can take from combination_marginals
        for item in element:
            value_item = combination_maginals[item][i]
            value_of_element.append(value_item)
        print(f"This is the value of element{value_of_element}")

        # Get the marginals for that element in the non-forbidden events
        marginals_element = utiles.find_marginal_support_given_set_with_repitation(element, marginals_dic_elements)
        some_events = find_events_satisfy_condition(value_of_element, marginals_element, events_non_forbidden)
        # print(f"here is the all events statisfy the conditions{some_events} for {element} equal to {value_of_element}")
        results.append(some_events)
        
    print(f"here is the result for the elements {list_of_elements}, the result{results}")

    return results


def find_events_satisfy_condition(value_of_element: np.ndarray, marginals_element, events_non_forbidden):
    """
    Description: Given one element in the d-separation equation, find all events in the non-forbidden event that satisfy the condition

    Parameters:
    ------------
    value_of_element: A list contain the value of items in one element, for example if we concerned with P(CD) in P(CD)P(ABCD) = P(ACD)P(BCD)
                      This will be P(C=c, D=d). [c, d]
    marginals_elements: continue with last example, this will be the marginals for ["C", "D"]
    events_non_forbidden: The non-forbidden events

    Return
    ------------
    all_events_satisfy: All the events that satisfy the condition [event1, event2, ... event n]
    """
    all_events_satisfy = []
    for i, element in enumerate(marginals_element):
        if(np.array_equal(element, value_of_element)):
            all_events_satisfy.append(events_non_forbidden[i])

    return np.array(all_events_satisfy)

def generate_combinations(second_element, unique_support=list([0,1])):
    """
    TODO: !!! Remember to pass in unique_spport when combine with the main script
    Description: get all the combinations of nodes that's in the second element of the d-separation relation

    Parameters:
    ------------
    second_element: The list contain all the nodes in a d-separation relations
    unique_support: A list contain the unique elements of the orginal supports

    Return
    ------------
    length: The number of total combinations that we can get
    combination_marginals: Dictionary. The marginals for the nodes in second elements
    """
    combinations = create_support(second_element, unique_support)
    marginals = break_marginal(combinations)
    combination_marginals = dict(zip(second_element, marginals))
    length = len(combinations)
    return combination_marginals, length



if __name__ == "__main__":
    # d_separation_relation = list([['B1'], ['B2'], ['A2']])

    # For my reference, to use this one, I need
    #                                   1. Non-forbidden-events generated from is_contradiction
    #                                   2. Nodes of the inflation graph
    #                                   3. Get the marginals for nodes
    #                                   4. All the d-separation relations
    event_non_forbidden = np.array([[0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 1],
                                    [0, 0, 0, 0, 1, 0],
                                    [0, 0, 0, 0, 1, 1],
                                    [0, 0, 0, 1, 0, 0],
                                    [0, 0, 0, 1, 1, 0],
                                    [0, 0, 1, 0, 0, 0],
                                    [0, 0, 1, 0, 0, 1],
                                    [0, 0, 1, 1, 0, 0],
                                    [0, 1, 0, 0, 0, 0],
                                    [0, 1, 0, 0, 0, 1],
                                    [0, 1, 1, 0, 0, 0],
                                    [0, 1, 1, 0, 0, 1],
                                    [1, 0, 0, 0, 0, 0],
                                    [1, 0, 0, 0, 1, 0],
                                    [1, 0, 0, 1, 0, 0],
                                    [1, 0, 0, 1, 1, 0],
                                    [1, 1, 0, 0, 0, 0]])
    nodes = list(['A1','A2','B1','B2','C1','C2'])
    marginals_dic= get_marginals_non_forbidden_events(event_non_forbidden, nodes)
    # print(marginals_dic)
    # all = generate_formula_given_d_separation(d_separation_relation)
    # # print(all)
    # second = generate_formula_given_d_separation(d_separation_relation)[1]
    # # print(second[0])
    # combination_marginals,length = generate_combinations(second)
    # # print(length)
    # get_all_possiblility(length, all, marginals_dic, event_non_forbidden,combination_marginals)


    ring_six_inflation = nx.DiGraph()
    ring_six_inflation.add_edges_from([("X1", "A1"), ("X1", "B1"), ("Y1", "B1"), ("Y1", "C1"), 
                                       ("Z1", "C1"), ("Z1", "A2"), ("X2", "A2"), ("X2", "B2"),
                                       ("Y2", "B2"), ("Y2", "C2"), ("Z2", "C2"), ("Z2", "A1")])
    ring_six_inflation_hidden = list(["X1", "X2", "Y1", "Y2", "Z1", "Z2"])

    d = check_d_networks.d_separation_list(ring_six_inflation, ring_six_inflation_hidden)

    containers = all_d_separate_relations(d, marginals_dic)
    print(len(containers))
