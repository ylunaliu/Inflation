import numpy as np
import itertools

def break_marginal(support):
    """ 
    Description: Break the marginals for a given support with nodes

    Parameters:
    ------------
    support: A 2D numpy array, 
   
    Return
    ------------
    A 2D numpy array contains the marginals for all nodes, [[marginals for node1], [marginals for node2] ...]
    """
    # Given a support, break to marginal for different nodes
    marginal_original_node = []
    for i in range(support.shape[1]):
        marginal_original_node.append(support[:,i])
    return np.array(marginal_original_node)


def find_marginal_support_given_injectable_set(injectable_set, dictionary_marginal):
    """ 
    Description: Find the marginals for an injectable set

    Parameters:
    ------------
    Injectable set: List, an injectable set
    
    Dictionary_marginal: Dictionary 
   
    Return
    ------------
    marginal_injectable_set: List of lists, the marginal of injectable set. [[marginals for node1 in injectable set], [marginals for node2 in injectable set] ...]
    """
    marginal_injectable_set = []

    for element in injectable_set:
        marginal_injectable_set.append(dictionary_marginal[element[0]])
    marginal_injectable_set= np.array(marginal_injectable_set).T
    marginal_injectable_set = np.array(list(((map(np.asarray, set(map(tuple, marginal_injectable_set)))))))
    
    return marginal_injectable_set

def dictionary_marginal_injectable(injectable_sets, dictionary_margin):
    """ 
    Description: Find the marginals for an injectable sets

    Parameters:
    ------------
    Injectable_sets: List of lists, a compelete injectable sets
    
    Dictionary_margin: Dictionary containing the original node and it's ancestor
   
    Return
    ------------
    Injecatble_sets_dictionary_marginal: A dictionary contain the marginals for all injectable sets
                                        - key: str(injectable_set)
                                        - value: marginals for that injectable set
    """
    injectable_sets_dictionary_marginals = {}
    for every_injectable_set in injectable_sets:
        injectable_sets_dictionary_marginals[str(every_injectable_set)] = find_marginal_support_given_injectable_set(every_injectable_set,dictionary_margin)
    return injectable_sets_dictionary_marginals


def dictionary_marginal_expressible(expressible_sets, dictionary_margin):
    """ 
    Description: Find the marginals for an expressible sets 

    Parameters:
    ------------
    expressible_sets: List of lists, the maximum expressible_sets
    Dictionary_margin: Dictionary containing the original node and it's ancestor
   
    Return
    ------------
    expressible_sets_dictionary_marginals: A dictionary contain the marginals for all expressible sets
                                        - key: str(expressible set)
                                        - value: marginals for that expressible set
    """
    expressible_sets_dictionary_marginals = {}
    for every_expressible_set in expressible_sets:
        separate_marginals_expressible = find_marginals_expressible_set(every_expressible_set, dictionary_margin)
        expressible_sets_dictionary_marginals[str(every_expressible_set)] = marginals_expressible_full(separate_marginals_expressible, len(every_expressible_set))
    return expressible_sets_dictionary_marginals

def find_marginals_expressible_set(expressible_set, dictionary_margin):
    """ 
    Description: Given an expressible set, return the marginals for each injectable set inside the expressible set 

    Parameters:
    ------------
    expressible_set: A expressible set. A list of lists. eg. [['A2', "B2"], ['C2']]
    dictionary_margin: Dictionary containing the original node and it's ancestor

    Return:
    ------------
    marginals_injectable_inside_expressible_set: A list containg the arrays that have the marginals for all injectable sets
                                                 inside an expressible set

    """
    marginals_injectable_inside_expressible_set = []
    for injectable in expressible_set:
        marginals_injectable_inside_expressible_set.append(find_marginal_support_given_injectable_set(injectable, dictionary_margin))
    
    return(marginals_injectable_inside_expressible_set)

def marginals_expressible_full(marginals, length):
    """ 
    Description: Given separate marginals of the injectable set in an expressible set, give the full
                 combination of the marginals for that expressible set

    Parameters: 
    ------------
    marginals: A list contain arrays of the marginals for the injectable sets in the expressible sets, I made the assumption 
               here an expressible set need to have at least 2 injectable sets
    length: The length of the expressible sets. Or the number of injectable sets inside the expressible set
    
    Return:
    ------------
    marginal: A list of lists contain all the marginal given an expressible set
    """
    marginal = marginals[0]
    for i in range(length-1):
        all_combinations = list(itertools.product(marginal, marginals[i+1]))
        supports = []
        for combination in all_combinations:
            chain = list(itertools.chain.from_iterable(combination))
            supports.append(chain)
        marginal = supports
 
    return marginal
            

def find_marginal_support_given_joined_expressible_set(expressible_set_joined, dictionary_margin_compatible_all_nodes):
    """ 
    Description: Given an expressible set in the joined format, find its marginals

    Parameters:
    ------------
    expressible_sets_join: A list of lists with all nodes in maximum expressible sets joined together
    dictionary_margin_compatible_all_nodes: A dictionary for marginals for all the non-forbidden events
                                            - key: str(node)
                                            - value: marginal for that node for the non-forbidden events
                                        
    Return
    ------------
    marginal_expressible_set: A list of lists contain the marginals for a expressible set
    """
    marginal_expressible_set = []
    for element in expressible_set_joined:
        marginal_expressible_set.append(dictionary_margin_compatible_all_nodes[element])
    marginal_expressible_set= np.array(marginal_expressible_set).T
    marginal_expressible_set = np.array(list(((map(np.asarray, set(map(tuple, marginal_expressible_set)))))))
    print(f"The is the marginal_expreesible_set {marginal_expressible_set} for expressible_set_joined{expressible_set_joined}")
    return marginal_expressible_set

def make_dictionary_for_nonforbidden_expressible_marginals(expressible_sets, expressible_sets_joined, dictionary_margin_compatible_all_nodes):
    """ 
    Description: Given an expressible sets, return the dictionary contain the marginals for the remaining 
                 non-forbidden events after rule out the forbidden events by injectable sets.

    Parameters:
    ------------
    expressible_sets: A list of lists, the maximum expressible sets
    expressible_sets_join: A list of lists with all nodes in maximum expressible sets joined together
    dictionary_margin_compatible_all_nodes: A dictionary for marginals for all the non-forbidden events
                                            - key: str(node)
                                            - value: marginal for that node for the non-forbidden events
                                        
    Return
    ------------
    dictionay_non_forbidden_events: The dictionary contain the marginls for a expressible set
                         - key: str(expressible_set)
                         - value: marginals for that expressible_sets for the non-forbidden events
    """
    dictionay_non_forbidden_events = {}
    for i, expressible_set in enumerate(expressible_sets):
        marginal_expressible_compatible = find_marginal_support_given_joined_expressible_set(expressible_sets_joined[i], dictionary_margin_compatible_all_nodes)
        dictionay_non_forbidden_events[str(expressible_set)] = marginal_expressible_compatible
    return  dictionay_non_forbidden_events

def check_for_contracdition(dictionary_marginals_nonforbidden_events, dictionary_marginals_expressible, expressible_sets):
    """ 
    Description: Given the expressible sets, marginals for the nonforbidden event for expressible sets, and the marginals for expressible sets
                 Check if there is a contradition exist

    Parameters:
    ------------
    expressible_sets: A list of lists, the maximum expressible sets
    dictionay_non_forbidden_events: The dictionary contain the marginls for a expressible set
                        - key: str(expressible_set)
                        - value: marginals for that expressible_sets for the non-forbidden events
    dictionary_marginals_expressible: A dictionary contain the marginals for all expressible sets
                - key: str(expressible set)
                - value: marginals for that expressible set
                                        
    Return
    ------------
    True if there is a contradition
    False if there is no contradition
    """
    is_expressible_not_compelete = []
    for expressible_set in expressible_sets:
        # Check if the number of marginals in non-forbidden event is less then the number of marginals in the complete expressible sets
        is_expressible_not_compelete.append(len(dictionary_marginals_nonforbidden_events[str(expressible_set)])< len(dictionary_marginals_expressible[str(expressible_set)]))
    
    if(True in is_expressible_not_compelete):
        print("We reach a contradition, the support is not compatible with given inflation")
        return False
    else:
        print("No contradtion found for the support given this inflation")
        return True


if __name__ == "__main__":
    pass