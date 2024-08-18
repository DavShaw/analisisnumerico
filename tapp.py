from Taylor import Taylor
import sympy as sp
#E1. Aproxima la funcion e**X sobre p = 0 con grado 4
#E1. Evaluar sobre 0.1 y calcular Error absoluto

#E2. Aprima la funcion sin(x) sobre pi/6 con grado 3
#E2. Evaluar sobre pi/6 + 0.1 y calcular Error absoluto

def e1():
    x = sp.symbols("x")
    f = sp.exp(x)
    t = Taylor(function = f, n = 4, a = 0)
    t.generate()
    r = t.evaluate(0.1)
    print(f"Resultado: {r}")
    error = t.getError(x=0.1)
    print(f"Abs. Error: {error}")
    cota = t.getCota(a = 0, b = 0.1)
    print(f"Cota: {cota}")
def e2():
    x = sp.symbols("x")
    f = sp.sin(x)
    t = Taylor(function = f, n = 3, a = sp.pi/6)
    t.generate()
    r = t.evaluate(sp.pi/6 + 0.1)
    print(f"Resultado: {r}")
    error = t.getError(x=sp.pi/6 + 0.1)
    print(f"Abs. Error: {error}")
    cota = t.getCota(a = sp.pi/6, b = sp.pi/6 + 0.1)
    print(f"Cota: {cota}")