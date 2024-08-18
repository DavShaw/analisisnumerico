from NumericalDiff import NumericalDiff
import sympy as sp
# Solucionar -> dy/dt = -ky(t)
# Se sabe y(0) = 1
def e1():
    n = NumericalDiff()
    k = 0.1
    h = 0.1
    xi = 1
    f = lambda x: -k*xi
    r = n.solveODE(h, xi, f, start=0, end=20, type="+")
    print(r)
    
#dy/dt = ry(1-y/k)
# r = 0.5, k = 100, y(0) = 10
def e2():
    n = NumericalDiff()
    y = sp.Symbol('y')
    k = 100
    xi = 10
    r = 0.5
    f = lambda y: r*y*(1-(y/k))
    r = n.solveODE(h=1, xi=xi, func=f, start=0, end=15, type="+")
    print(r)
e2()
