from find_injectable_sets import find_injectable_sets
from os import dup
from platform import node
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools

def find_expressible_sets(injectable_sets, dictionary):
    expressible_graph = nx.Graph()
    for i in range(len(injectable_sets)):
        expressible_graph.add_node(str(i), sets=injectable_sets[i])

    # Get all the nodes
    nodes = list(expressible_graph.nodes)
    nodes_attribute = nx.get_node_attributes(expressible_graph, "sets")
    print(f'here is the nodes_assignment {nodes_attribute}')

    # Get all the combinations of two nodes
    combinations = list(itertools.combinations(nodes,2))
    experssible_pair = []
    for pair_injectable in combinations:
        print(f"checking pair{pair_injectable}")
        node1 = pair_injectable[0] #number
        node2 = pair_injectable[1]
        injectable_sets_node1 = expressible_graph.nodes[str(node1)]["sets"] # ['B1', 'C1', 'A1']
        print(f"injectable_sets_from_node_1{injectable_sets_node1}")
        injectable_sets_node1_ancestor = {}
        for i in range(len(injectable_sets_node1)):
            injectable_sets_node1_ancestor.update(dictionary[str(injectable_sets_node1[i])])
            print(dictionary[str(injectable_sets_node1[i])])
        print(f"injectable_sets_from_node_ancestor_1{injectable_sets_node1_ancestor}")
        injectable_sets_node2 = expressible_graph.nodes[str(node2)]["sets"]
        print(f"injectable_sets_from_node_2{injectable_sets_node2}")
        injectable_sets_node2_ancestor = {}

        for i in range(len(injectable_sets_node2)):
            injectable_sets_node2_ancestor.update(dictionary[str(injectable_sets_node2[i])])
        print(f"injectable_sets_from_node2_ancestor_2{injectable_sets_node2_ancestor}")

        boolean_set = []
        if(not set([*injectable_sets_node1_ancestor]).isdisjoint([*injectable_sets_node2_ancestor])):
            print(f"checking if any ancestor are overlapping{not set([*injectable_sets_node1_ancestor]).isdisjoint([*injectable_sets_node2_ancestor])}")
            # Find the duplicate 
            duplicate_node = list(set([*injectable_sets_node1_ancestor]).intersection([*injectable_sets_node2_ancestor]))
            print(f"duplicate {duplicate_node}")
            # print(f'The duplicate_node for {sets} is {duplicate_node}')
            index_node = []

            for node in duplicate_node:
                # print(f"checking if it the same node{injectable_sets_node1_ancestor[node]==injectable_sets_node2_ancestor[node]}")
                boolean_set.append(injectable_sets_node1_ancestor[node]==injectable_sets_node2_ancestor[node])
                
            print(f"boolean_set{boolean_set}")
        if(not True in boolean_set):
            experssible_pair.append(pair_injectable)
            print(f"here is the expressible pair{experssible_pair}")
            
                

    expressible_graph.add_edges_from(experssible_pair)
    print(f"here is the expressible pair{experssible_pair}")
    expressible_sets = list(nx.find_cliques(expressible_graph))
    print(expressible_sets)

    expressible_convert = []
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

    injectable_sets1, dictionary = find_injectable_sets(sprial_inflation, sprial_inflation_hidden)
    print(f"this is the injecable sets{injectable_sets1}")
    
    expressible = find_expressible_sets(injectable_sets1, dictionary)
    print(expressible)
# nx.draw(expressible_graph,with_labels=True)
# plt.show()
    
# I need to construct a sub graph for expressible sets
# Try checking attributes
# Need more work