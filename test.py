import sympy as sp
from Taylor import Taylor
from NumericalDiff import NumericalDiff

nEval = 5
f = lambda x: sp.sin(x)*sp.cos(x)*2
t = Taylor(function=f, n=5, a=5)
t.generate()
p7 = float(t.evaluate(200))
f7 = float(f(nEval))
print(f"Taylor Polynomial at x=7: {p7}")
print(f"Function at x=7: {f7}")
print(f"Error: {t.getError(nEval)}")
t.graph()