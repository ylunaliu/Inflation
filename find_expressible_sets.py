from find_injectable_sets import find_injectable_sets
from os import dup
from platform import node
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools

def find_expressible_sets(injectable_sets, dictionary):

    # Create a sub graph for the expressible sets
    expressible_graph = nx.Graph()

    # Adding the componment of the injectable sets as node. Assign a number as node name and injectable set as attribute
    for i in range(len(injectable_sets)):
        expressible_graph.add_node(str(i), sets=injectable_sets[i])

    # Get all the nodes
    nodes = list(expressible_graph.nodes)

    # Get all the combinations of two nodes
    combinations = list(itertools.combinations(nodes,2))

    experssible_pair = [] # Array storing the expressible pair 
    for pair_injectable in combinations:
        node1 = pair_injectable[0] # number, node name
        node2 = pair_injectable[1]

        injectable_sets_node1 = expressible_graph.nodes[str(node1)]["sets"] # node attribute, an injectable set
        injectable_sets_node1_ancestor = {}
        for i in range(len(injectable_sets_node1)):
            injectable_sets_node1_ancestor.update(dictionary[str(injectable_sets_node1[i])]) # Get the common ancestor

        injectable_sets_node2 = expressible_graph.nodes[str(node2)]["sets"]
        injectable_sets_node2_ancestor = {}
        for i in range(len(injectable_sets_node2)):
            injectable_sets_node2_ancestor.update(dictionary[str(injectable_sets_node2[i])])

        boolean_set = []
        if(not set([*injectable_sets_node1_ancestor]).isdisjoint([*injectable_sets_node2_ancestor])):
            # Find the duplicate 
            duplicate_node = list(set([*injectable_sets_node1_ancestor]).intersection([*injectable_sets_node2_ancestor]))

            for node in duplicate_node:
                boolean_set.append(injectable_sets_node1_ancestor[node]==injectable_sets_node2_ancestor[node])
                
        if(not True in boolean_set):
            experssible_pair.append(pair_injectable)
            
                

    expressible_graph.add_edges_from(experssible_pair)
    expressible_sets = list(nx.find_cliques(expressible_graph))


    expressible_convert = [] # Convert from the number nodes representation to expressible sets
    for injectable_node in expressible_sets:
        if(len(injectable_node)>1):
            all_stuff = []
            for i in range(len(injectable_node)):
                all_stuff.append(expressible_graph.nodes[injectable_node[i]]["sets"])
            expressible_convert.append(all_stuff)
    
    
    return expressible_convert


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

    injectable_sets, maximum_injectable_sets1, dictionary = find_injectable_sets(cut_inflation, cut_inflation_hidden)
    print(f"this is the injectable sets{maximum_injectable_sets1}")
    
    expressible = find_expressible_sets(maximum_injectable_sets1, dictionary)
    print(f"This is the expressible_sets{expressible}")

    # Only need the maximum injectable sets
    # Also maximum exprssible sets