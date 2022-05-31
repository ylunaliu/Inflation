import numpy as np
import itertools

def create_support(nodes, unique_element):
    """ 
    Description: Create all possible events given the unique_element in the original support

    Parameters:
    ------------
    nodes: A list of sorted nodes
    unique_element: A list of the unique elements in the original support
   
    Return
    ------------
    All possible combination of events of the nodes
    """
    return np.array(list(itertools.product(unique_element,repeat=len(nodes))))


def create_forbidden_event_given_injectable_sets(injectable_set, marginal, unique_element):
    """ 
    Description: Find the forbidden marginal of event for an injectable set

    Parameters:
    ------------
    injectable_set: An injectable_set
    marginals: The marginal for that injectable set list of lists for that single injectable set
    unique_element: A list of the unique elements in the original support
   
    Return
    ------------
    not_possible: A list of lists for the forbidden events
    """
    mariginal_all_support = create_support(injectable_set, unique_element)
    not_possible = np.array(list(set(map(tuple,mariginal_all_support)).difference(set(map(tuple,marginal)))))
    return not_possible


def create_dictionary_for_all_injectable_set_not_possible(injectable_sets, dictionary_injectable, unique_element):
    """ 
    Description: Find the forbidden marginal of event for an injectable set

    Parameters:
    ------------
    injectable_sets: The maximum injectable_set
    dictionary_injectable: A dictionary contain the marginals for all injectable sets
                                    - key: str(injectable_set)
                                    - value: marginals for that injectable set
    unique_element: A list of the unique elements in the original support
   
    Return
    ------------
    dictionary_not_possible:  A dictionary with key as the injectable set and value as the forbidden marginals
    """
    dictionary_not_possible = {}
    for injectable_set in injectable_sets:
        # For each injectable_set, find the forbidden marginal
        marginals = dictionary_injectable[str(injectable_set)]
        not_possible = create_forbidden_event_given_injectable_sets(injectable_set, marginals, unique_element)
        dictionary_not_possible[str(injectable_set)] = not_possible
        
    return dictionary_not_possible


def cut_marginal_from_orginal_support(all_support, cutting_index):
    """ 
    Description: Cut out the marginals for each node

    Parameters:
    ------------
    all_support: A list of lists, all the events that is possible
    cutting_index: A list containing the cutting index
   
    Return
    ------------
    A 2D numpy array contains the marginals for a injectable set(cutting index)
    """
    combined_marginals = []
    all_support_copy = list(all_support).copy()
    all_support_copy = np.array(all_support_copy)
    for i in range(len(cutting_index)):
        combined_marginals.append(all_support_copy[:,cutting_index[i]])

    return np.array(combined_marginals).T

def get_index_forbidden_event(forbidden_events, all_support, cutting_index):
    """ 
    Description: Get the index of all the forbidden events

    Parameters:
    ------------
    all_supports: A list of lists, all the events that is possible
    forbidden_events: A list of lists containing the forbidden events
    cutting_index: A list containing the cutting index for that injectable set
   
    Return
    ------------
    index_to_be_remove: A list of indexes for all the forbidden events
    """

    marginals = cut_marginal_from_orginal_support(all_support, cutting_index)
    index_to_be_remove = []

    for forbidden_event in forbidden_events:
        for index, element in enumerate(marginals):
           if(np.array_equal(element, forbidden_event)):
                index_to_be_remove.append(index)
 
    index_to_be_remove = set(index_to_be_remove)
    index_to_be_remove = np.array(list(index_to_be_remove))

    return index_to_be_remove


def get_nonforbidden_events(all_support, index_to_keep):
    """ 
    Description: Get the nonforbidden events

    Parameters:
    ------------
    all_supports: A list of lists, all the events that is possible
    index_to_keep: The list of index for the nonforbidden events
   
    Return
    ------------
    events_to_keep: A list of lists contains all the events to keep
    """
    events_to_keep = []
    for index in index_to_keep:
        events_to_keep.append(list(all_support)[index])
    
    return np.array(events_to_keep)

def rule_out_forbidden_events_due_to_injectable_sets(dictionary_not_possible, injectable_sets, all_support, node_support):
    """ 
    Description: Get the nonforbidden events

    Parameters:
    ------------
    all_supports: A list of lists, all the events that is possible
    dictionary_not_possible:  A dictionary with key as the injectable set and value as the forbidden marginals
    injectable_sets: A list of lists the maximum injectable sets
    node_support: A list of sorted nodes for the inflation graph
   
    Return
    ------------
    events_to_keep: A list of lists contains all the events to keep
    """
    index_to_be_remove = []
    for injectable_set in injectable_sets:
        cutting_index = []
        not_possible_support = dictionary_not_possible[str(injectable_set)]
        # look for the index based on injectable_set
        for i in range(len(injectable_set)):
            cutting_index.append(list(node_support).index(injectable_set[i]))
        index_to_be_remove.extend(get_index_forbidden_event(not_possible_support,all_support,cutting_index))

    index_to_be_remove = list(set(index_to_be_remove))
    index_to_be_remove = np.array(index_to_be_remove)
    index_to_keep = np.arange(0,len(all_support),1)
    index2 = np.array(list(set(index_to_keep)^set(index_to_be_remove)))


    events_nonforbidden = get_nonforbidden_events(all_support, index2)
    return events_nonforbidden