# Inflation
Finding the injectable and expressible sets of an inflation graph

1. Version 1:
find_injectable_sets: Find all injectable sets in a given graph
\\
find_expressible_sets: Find all expressible sets in a given graph
find_maximum_expressible_sets: Find the maximum expressible sets in a given graph
\\
Is_contradtion.py: Find all the non-forbidden events using injectable set, and see if it reach a contradition with the marginals of expressible sets
\\
utiles.py: supplementary function to Is_contradition
\\
utiles_reject_forbidden_events.py: supplementary function to Is_contradition, specifically for finding the non-forbidden events

2. Version 2:
Based on finding the non-forbidden-events and d-separation relation, find all the logical expression for d-separation
check_d_networks.py: Find all the d-separation relations for a given graph using networkx's find d-separation
utiles_find_conditions: utile for version2 haven't combined with Version 1 


3. making inflation graph as a class
class_inflation_graph.py

4. make taking multiple inflation graph compatible:
Inflation_graph.py
