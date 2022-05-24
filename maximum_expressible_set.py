from ssl import ALERT_DESCRIPTION_BAD_RECORD_MAC
from find_injectable_sets import find_injectable_sets
from os import dup
from platform import node
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools
from find_expressible_sets import find_expressible_sets

def append_list(expressible_set):
    joined_list = []
    for i in range(len(expressible_set)):
        joined_list.extend(expressible_set[i])
    return joined_list



def maximum_expressible(expressible):   
    acc = []
    acc_joined = []
    for each_expressible_set in expressible:
        # print(f"here is the expressible set{each_expressible_set}")
        joined_num = len(each_expressible_set)
        # print(f"length of the expressible set{joined_num}")
        joined = append_list(each_expressible_set)
        joined_num_node = len(joined)
        # print(f"here is after they joined{joined}")
        if(acc == []):
            acc.append(each_expressible_set)
            acc_joined.append(joined)
        # print(f"here is acc_joined{acc_joined}")
        boolean_ifsubset = False
        for i, element in enumerate(acc_joined):
            # print(f"here is the element in acc_joined{element}")
            # print(f"compare with {joined}")
            if(set(joined).issubset(set(element))):
                # print(f"length of the one to compare{len(acc[i])}")
                if(len(joined)==len(acc_joined[i]) and (joined_num_node - joined_num)<(len(acc_joined[i])-len(acc[i]))):
                    acc.remove(acc[i])
                    acc.append(each_expressible_set)
                    acc_joined.append(joined)
                    acc_joined.remove(element)
                boolean_ifsubset = False
                break
            else:
                if(set(element).issubset(set(joined))):
                    acc.remove(acc[i])
                    acc_joined.remove(element)
                boolean_ifsubset = True
        if(boolean_ifsubset):    
            acc.append(each_expressible_set)
            # print(f"here is the acc{acc}")
            acc_joined.append(joined)
            # print(f"here is the joined accumulator{acc_joined}")
    return acc, acc_joined
if __name__ == "__main__":
    sprial_inflation = nx.DiGraph()
    sprial_inflation.add_edges_from([("X2", "C2"), ("Z2", "B2"), ("Y2", "A2"),
                            ("X1", "A2"), ("X1", "A1"), ("X1", "C1"), 
                            ("Y1", "A1"), ("Y1", "B1"), ("Y1", "B2"), 
                            ("Z1", "C1"), ("Z1", "B1"), ("Z1", "C2")])

    sprial_inflation_hidden = list(["X2", "Y2", "Z2", "X1", "Y1", "Z1"])

    injectable,maximum_injectable_sets1, dictionary = find_injectable_sets(sprial_inflation, sprial_inflation_hidden)
    expressible = find_expressible_sets(maximum_injectable_sets1, dictionary)
    print(f"here is the expressible set{expressible}")

    # expressible_test = [[["A"], ["B", "C"]], [["A"], ["B"], ["C"]], [["C"], "D"]]
    # expressible_test2 = [[["A"], ["B"], ["C"]],[["A"], ["B", "C"]], [["C"], "D"]]
    # expressible_test3 = [[['A1'], ['C2']], [['B1', 'C2'], ['A2']], [['B2', 'A1'], ['C2']]]
    expressible_test4 = [[['B1', 'C2'], ['A2']], [['B1'], ['A2']]]
    acc,acc_joined= maximum_expressible(expressible)
    print(f"here is the maximum expressible set{acc},")
