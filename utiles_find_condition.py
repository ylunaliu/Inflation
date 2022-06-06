from enum import unique
from re import I
from xml.dom.minidom import Element
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

def all_d_separate_relations(d_separation_relations: list, marginals_dic, event_non_forbidden, marginals_unique_dic, dic_event_to_variable):
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
    unique_support = list([0,1])
    # global number_to_index_from
    # number_to_index_from =len(event_non_forbidden)

    number_to_index_from = {}
    f = open("myfile.txt", "w")
    number_to_index_from['index'] = len(event_non_forbidden)+1
    dictionary_variable_margins_P = {}
    container = []
    d_assignment_constraint1 = [] 
    constraint_each_margin_P1 = []
    for each_d_separation_relation in d_separation_relations:
        f.write(f"Here is the d-separation: {each_d_separation_relation}\n")
        print(number_to_index_from)
        print(f"here is each d separation {each_d_separation_relation}") #1
        all = generate_formula_given_d_separation(each_d_separation_relation)
        second = all[1]
        combination_marginals, length = generate_combinations(second, unique_support, marginals_unique_dic) # I should move this out of here
        print(f"length of combinations{length}")
        container1, d_assignment_constraint, constraint_each_margin_P = get_all_possiblility(length, all, marginals_dic, event_non_forbidden, combination_marginals, dic_event_to_variable,number_to_index_from, dictionary_variable_margins_P,f)
        container.append(container1)
        d_assignment_constraint1.extend(d_assignment_constraint)
        constraint_each_margin_P1.extend(constraint_each_margin_P)

    f.write(f"with d_assignment_constrant {d_assignment_constraint1}\n")
    f.write(f"with constraint each margin {constraint_each_margin_P1}\n")
    print(f"This is the size of constraint each margin {len(constraint_each_margin_P1)}")
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
    # print(d_separation_relation)
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
    unique = []
    for marginal in marginals_non_forbidden:
        unique.append(np.unique(np.array(marginal)))
    
    marginals_unique = dict(zip(nodes, unique))
    marginals_non_forbidden_dictionary = dict(zip(nodes, marginals_non_forbidden))
    return marginals_non_forbidden_dictionary, marginals_unique

def get_all_possiblility(length, list_of_elements, marginals_dic_elements, events_non_forbidden, combination_marginals, dic_event_to_variable, number_to_index_from, dictionary_variable_margins_P, f):
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
    d_assignment_constraint1 = []
    constraint_each_margin_P1 = []
    for i in range(length):

        f.write(f"This is for assignment{i}\n")
        events_for_formula, d_assignment_constraint, constraint_each_margin_P= get_events_given_formula(list_of_elements, marginals_dic_elements, i, events_non_forbidden, combination_marginals, dic_event_to_variable, number_to_index_from, dictionary_variable_margins_P,f)
        d_assignment_constraint1.extend(d_assignment_constraint)
        constraint_each_margin_P1.extend(constraint_each_margin_P)
        containers.append(events_for_formula)
        f.write(f"Here is the main constraint so far {d_assignment_constraint1}\n")
        f.write(f"Here is the subsequent P constraint so far {constraint_each_margin_P1}\n")
    return containers, d_assignment_constraint1, constraint_each_margin_P1

def get_events_given_formula(list_of_elements, marginals_dic_elements, j, events_non_forbidden, combination_maginals, dic_event_to_variable,number_to_index_from,dictionary_variable_margins_P, my_file):
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
    key_varaible_for_margins = []
    constraint_P_list = []
    constraint_each_margin_P = []
    # Loop through the elements

    for i, element in enumerate(list_of_elements):
        value_of_element = []
        # print(f"This is the elemnt {element}")
        # Get the specific value that this element can take from combination_marginals
        for item in element:
            value_item = combination_maginals[item][j]
            # print(f"This is the node{item} the index{i}")
            value_of_element.append(value_item)
        
        # print(f"value_of_element{value_of_element}")
        # print(f"This is the value of element{value_of_element}")

        # Get the marginals for that element in the non-forbidden events
        marginals_element = utiles.find_marginal_support_given_set_with_repitation(element, marginals_dic_elements)
        # print(f"This is the marginals_elements {element}")
        key_varaible_for_margins = [list(element), value_of_element]
        if(not (str(key_varaible_for_margins) in dictionary_variable_margins_P)):
            value_number_to_index_from = number_to_index_from["index"]
            number_to_index_from["index"] = value_number_to_index_from+ 1
            dictionary_variable_margins_P[str(key_varaible_for_margins)] = number_to_index_from["index"]
            # print(f"here is the label for p: {value_number_to_index_from+ 1}\n")
        
        # Get the constraints for Ps

        constraint_P_list.append(dictionary_variable_margins_P[str(key_varaible_for_margins)])
        # print(f"dictionary_variavle_marginals{dictionary_variable_margins_P}")
        some_events, SAT_conversion = find_events_satisfy_condition(value_of_element, marginals_element, events_non_forbidden, dic_event_to_variable)
        # print(f"here is the all events statisfy the conditions{SAT_conversion} for {element} equal to {value_of_element}")
        
        constraint_P = get_constraint_P(SAT_conversion, dictionary_variable_margins_P[str(key_varaible_for_margins)])
        constraint_each_margin_P.append(constraint_P)
        my_file.write(f"Here is the constraint_P: {constraint_P} with p equal to {dictionary_variable_margins_P[str(key_varaible_for_margins)]}\n")
        results.append(some_events)
    
    # print(f"This is the constrain given by one assignment on P {constraint_each_margin_P}")
    d_assignment_constraint = get_constraint_d_assignment(constraint_P_list)
    my_file.write(f"here is the constraint given by P constraint_list: {d_assignment_constraint}\n")
    my_file.write(f"here is the P constraint list{constraint_P_list}\n")
    # print(f"here is the result for the elements {list_of_elements}, the result{results}")

    return results, d_assignment_constraint, constraint_each_margin_P


def find_events_satisfy_condition(value_of_element: np.ndarray, marginals_element, events_non_forbidden, dic_event_to_variable):
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
    SAT_conversion: A list contain all the variable used to represent events in SAT compatible format
    """
    all_events_satisfy = []
    SAT_conversion = []
    for i, element in enumerate(marginals_element):
        if(np.array_equal(element, value_of_element)):
            all_events_satisfy.append(events_non_forbidden[i])
            SAT_conversion.append(dic_event_to_variable[str(events_non_forbidden[i])])
           
    # print(f"This the the SAT_conversion: {SAT_conversion}")
    return np.array(all_events_satisfy), SAT_conversion

def generate_combinations(second_element, unique_support, marginals_unique_dic):
    """
    TODO: !!! Remember to pass in unique_spport when combine with the main script
    Description: get all the combinations of nodes that's in the second element of the d-separation relation
    TODO: looks suspecious might need to look more into it, for example can all nodes takes all values?

    Parameters:
    ------------
    second_element: The list contain all the nodes in a d-separation relations
    unique_support: A list contain the unique elements of the orginal supports

    Return
    ------------
    length: The number of total combinations that we can get
    combination_marginals: Dictionary. The marginals for the nodes in second elements
    """
    filter_not_complete = []
    filter_not_complete_value = []
    for i, node in enumerate(second_element):
        if(not np.array_equal(marginals_unique_dic[node], np.array(unique_support))):
            print(np.array_equal(marginals_unique_dic[node], np.array(unique_support)))
            filter_not_complete.append(i)
            filter_not_complete_value.append(np.setdiff1d(np.array(unique_support), marginals_unique_dic[node]))
    
    
    combinations = create_support(second_element, unique_support)
    
    if(len(filter_not_complete)!=0):
        combinations = np.array(filter_not_complete_events(combinations, filter_not_complete, filter_not_complete_value))


    marginals = break_marginal(combinations)
    combination_marginals = dict(zip(second_element, marginals))
    length = len(combinations)
    return combination_marginals, length

def filter_not_complete_events(combinations, filter_not_complete, filter_not_complete_value):
    index_to_abandon = []
    new_combinations = []
    for each_node_index in filter_not_complete:
        for forbidden_value in filter_not_complete_value[each_node_index]:
            marginal = combinations[:,each_node_index]
            index_to_abandon.extend(np.where(marginal==forbidden_value)[0])
    
    index_to_abandon = list(set(index_to_abandon))
    index = np.arange(0,len(combinations),1)
    index_to_keep = np.array(list(set(index)^set(index_to_abandon)))

    for index in index_to_keep:
        new_combinations.append(combinations[index])

    return(new_combinations)

def non_forbidden_events_variable_dic(event_non_forbidden):
    """"
    Assigning variable to each non forbidden events
    Key(str(event_non_forbidden[0]))
    """
    dic_event_to_variable = {}
    for i, each_event in enumerate(event_non_forbidden):
        dic_event_to_variable[str(each_event)] = i+1
    
    return dic_event_to_variable

def get_constraint_P(events_num, P_num):
    """
    events: list of events's numebr [1,4,5]...
    P: A single numer

    This is the additional variable that helps with simfiply the case. P = (e1 v e2 v e3) can be written as (~P1 v e1 v e2 v e3)^(P1 v ~(e1 ^ e2 ^e3))
    then (~P1 v e1 v e2 v e3)^(P1 v ~e1)^(P1 v ~e2)^(P1 v ~e3) 
    """
    constraint = []
    first_element = list([-P_num])
    first_element.extend(events_num)
    constraint.append(first_element)

    for event in events_num:
        constraint.append([P_num, -1*(event)])

    return constraint
    
def get_constraint_d_assignment(P_num_list):
    """
    Produce the constraint for d-separation in cnf form
    P_num_list = [var_firstele...var_lastele]
    """
    print()
    return ([[-P_num_list[0], -P_num_list[1], P_num_list[2]],[-P_num_list[0], -P_num_list[1], P_num_list[3]],[-P_num_list[3], -P_num_list[2], P_num_list[1]],[-P_num_list[3], -P_num_list[2], P_num_list[0]]])

if __name__ == "__main__":
    d1 = list([[['B1'], ['B2'], ['A2']],[['C2'], ['B2'], ['C1']]])

    # get_constraint_P([1,5,6], 9)
    # get_constraint_d_assignment([1,2,3,4])
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

    dic_event_to_variable = non_forbidden_events_variable_dic(event_non_forbidden)
    nodes = list(['A1','A2','B1','B2','C1','C2'])
    marginals_dic, marginals_unique_dic= get_marginals_non_forbidden_events(event_non_forbidden, nodes)
   
   
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

    containers = all_d_separate_relations(d, marginals_dic, event_non_forbidden, marginals_unique_dic, dic_event_to_variable)
    print(np.size(containers))
