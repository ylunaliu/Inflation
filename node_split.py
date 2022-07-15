import networkx as nx
import numpy as np

def create_node_split_name(node):
    """
    Descrption: used to split the node name

    Parameter:
    ------------


    Return:
    ------------
    A list containing the first and the rest of the characters in the node.
    """
    new_name = node + "#"
    return new_name


def node_split(graph, nodes_hidden):
    observed_node = list(graph.nodes()^nodes_hidden)

    for node in observed_node:
        # print(f"for node {node}")
        predecessor = list(graph.predecessors(node))
        children = list(graph.successors(node))
        if(len(predecessor)!=0):
            # print(graph.in_edges(node))
            out_edge = list(graph.out_edges(node))
            # print(f"here is the out_edge{out_edge}")

            for edge in out_edge:
                graph.remove_edge(edge[0], edge[1])
                new_name = create_node_split_name(node)
                graph.add_edge(new_name,edge[1])



    # print(graph.edges)
    return graph



if __name__ == "__main__":
    #example1: unrelated confounders
    unrelated_confounders = nx.DiGraph()
    unrelated_confounders.add_edges_from([("U1", "A1"), ("U1", "D1"), ("U2", "B1"), ("U2", "D1"), ("D1", "A1"), ("D1", "B1")])
    unrelated_confounders_hidden = list(["U1", "U2"])

    #example2: Instrumental graph
    instrumental = nx.DiGraph()
    instrumental.add_edges_from([("A1", "D1"), ("D1", "B1"), ("U1", "D1"), ("U1", "B1")])
    instrumental_hidden = list(["U1"])
    
    node_split(unrelated_confounders, unrelated_confounders_hidden)

    print(unrelated_confounders.edges)

