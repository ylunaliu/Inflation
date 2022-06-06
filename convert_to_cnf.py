from sympy import *
from sympy.logic.boolalg import to_cnf
from sympy.abc import A, B, C,D,E, F,G, H,J,K

statement = to_cnf((((A|B)&(C|F|G))&((D|H|J)&(E|K)))|(~((A|B)&(C|F|G))&~((D|H|J)&(E|K))),force=True)
print(statement)