from find_injectable_sets import find_injectable_sets
from os import dup
from platform import node
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools


sprial_inflation = nx.DiGraph()
sprial_inflation.add_edges_from([("X2", "C2"), ("Z2", "B2"), ("Y2", "A2"),
                                ("X1", "A2"), ("X1", "A1"), ("X1", "C1"), 
                                ("Y1", "A1"), ("Y1", "B1"), ("Y1", "B2"), 
                                ("Z1", "C1"), ("Z1", "B1"), ("Z1", "C2")])

sprial_inflation_hidden = list(["X2", "Y2", "Z2", "X1", "Y1", "Z1"])

injectable_sets, dictionary = find_injectable_sets(sprial_inflation, sprial_inflation_hidden)



expressible_graph = nx.Graph()
for i in range(len(injectable_sets)):
    expressible_graph.add_node(str(i), sets=injectable_sets[i])

nodes = list(expressible_graph.nodes)
combinations = list(itertools.combinations(nodes,2))
dictionary2 = nx.get_node_attributes(expressible_graph, "sets")

print(dictionary2)

for pair_injectable in combinations:
    node1 = pair_injectable[0] #number
    node2 = pair_injectable[1]
    injectable_sets_node1 = dictionary2[str(node1)] # ['B1', 'C1', 'A1']
    injectable_sets_node1_ancestor = dictionary[str(injectable_sets_node1[0])]
    for i in range(len(injectable_sets_node1)):
        injectable_sets_node1_ancestor.update(dictionary[str(injectable_sets_node1[i])])

    injectable_sets_node2 = dictionary2[str(node2)]
    injectable_sets_node2_ancestor = dictionary[str(injectable_sets_node2[0])]
    for i in range(len(injectable_sets_node2)):
        injectable_sets_node2_ancestor.update(dictionary[str(injectable_sets_node2[i])])
    experssible_pair = []
    if(not set([*injectable_sets_node1_ancestor]).isdisjoint([*injectable_sets_node2_ancestor])):
        # Find the duplicate 
        duplicate_node = list(set([*injectable_sets_node1_ancestor]).intersection([*injectable_sets_node2_ancestor]))
        # print(f'The duplicate_node for {sets} is {duplicate_node}')
        index_node = []
        boolean_set = []
        for node in duplicate_node:
            boolean_set.append(injectable_sets_node1_ancestor[node]==injectable_sets_node2_ancestor[node])
        if(True in boolean_set):
            experssible_pair.append(pair_injectable)
            
print(experssible_pair)

expressible_graph.add_edges_from(experssible_pair)
expressible_sets = list(nx.find_cliques(expressible_graph))

expressible_convert = []
for injectable_node in expressible_sets:
    if(len(injectable_node)>1):
        all = []
        for i in range(len(injectable_node)):
            all.append(dictionary2[injectable_node[i]])
        expressible_convert.append(all)



print(expressible_convert)
# nx.draw(expressible_graph,with_labels=True)
# plt.show()
    
# I need to construct a sub graph for expressible sets
# Try checking attributes
# Need more work