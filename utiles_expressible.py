from venv import create
from find_injectable_sets import find_injectable_sets
from os import dup
from platform import node
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools
from find_expressible_sets import find_expressible_sets
from sympy.physics.quantum import TensorProduct
from maximum_expressible_set import maximum_expressible
from create_all_support import create_support
import create_all_support


def marginals_expressible_full(marginals, length):
    """
    expressible sets will be at least size 2 
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

   



    # print(supports)

if __name__ == "__main__":
    pass