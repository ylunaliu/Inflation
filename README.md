# Inflation
Finding the injectable and expressible sets of an inflation graph

1. Version 1: <br />
**find_injectable_sets.py**: Find all injectable sets in a given graph<br />
**find_expressible_sets.py**: Find all expressible sets in a given graph<br />
**find_maximum_expressible_sets.py**: Find the maximum expressible sets in a given graph<br />
**Is_contradtion.py**: Find all the non-forbidden events using injectable set, and see if it reach a contradition with the marginals of expressible sets. 
**utiles.py**: supplementary function to Is_contradition<br />
**utiles_reject_forbidden_events.py**: supplementary function to Is_contradition, specifically for finding the non-forbidden events<br />
2. Version 2: <br />
Based on finding the non-forbidden-events and d-separation relation, find all the logical expression for d-separation <br />
**check_d_networks.py**: Find all the d-separation relations for a given graph using networkx's find d-separation <br />
**utiles_find_conditions.py**: utile for version2 haven't combined with Version 1. Cancel changes <br />


3. making inflation graph as a class <br />
**class_inflation_graph.py** <br />

4. make taking multiple inflation graph compatible <br />
**Inflation_graph.py** <br />
