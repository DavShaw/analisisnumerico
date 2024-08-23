import sympy as sp
from Taylor import Taylor
from NumericalDiff import NumericalDiff
import numpy as np
import matplotlib.pyplot as plt
import json


"""
1. Determinar el 6to polinomio de Taylor de la función f(x) = 2x*sin(x)-(x-3)²
en x = pi/4.

- Aproximar f(pi/2) con P6(pi/2)
- Determinar la cota |f(pi/2) - p6(pi/2)|
- Aproxime f'(pi/2) usando p6'(pi/2) calcular Ea y Er
- Grafique el polinomio de grado 1 (fx) vs el polinomio de grado 8 (p8x) ???
"""

"""
2. Proyectil de masa m=0.15kg es lanzado verticalmente para arriba
con una velocidad inicial de 10m/s (si t = 0 -> v(0) = 10) y disminuye
la velocidad por efecto de la gravedad = -(9.8)*m y la resistencia del aire
fr = -kv|v| donde k=0.002kg/m
h = 0.001 
intervalo = 0 a 5s
EDO -> dv/dt = -g - (kv|v|/m)

- Velocidad a los 5s despues de lanzado
"""

def e2():
    # constantes o variables
    m = 0.15  
    k = 0.002 
    g = 9.8  
    v0 = 10
    h = 0.001
    a = 0
    b = 5
    tiempo5 = b/h
    
    f = lambda v: -g - (k*v*abs(v)/m)
    solver = NumericalDiff()
    # El type de mi funcion es el tipo de diferenciaicon que hace
    # + es porque es adelante, pues el tiempo se mueve pa delante
    # - seria diferenciacion atrás (no nos sirve)
    result = solver.solveODE(h=h, xi=v0, func=f, start=0, end=int(tiempo5), type="+")
    
    velocidad5 = result[int(tiempo5)]
    print(f"Velocidad a los 5s: {velocidad5}")
    
    # En que segundo comienza a caer
    # con result.json vi manualmente que en la iteraion
    # 978 cambio de + a -
    tiempoCaida = 978 * h
    print(f"Cae en el segundo: {tiempoCaida}")
    

def e1():
    pi = sp.pi
    f = lambda x: 2*x*sp.sin(x) - (x-3)**2
    t = Taylor(f, 6, pi/4)
    t.generate()
    x = sp.symbols("x")
    
    va = float(t.evaluate(pi/2)) # Valor aproximado
    vr = float(f(pi/2)) # Valor real
    
    cota = t.getCota(vr,va)
    
    print(f" Valor aproximado: {va} vs Valor real: {vr}")
    print(f" Cota: {cota}")
    
    df = sp.diff(f(x), x)
    dp = sp.diff(t.getPoly(), x)
    dfevaled = float(df.evalf(subs={x: pi/2}))
    dpevaled = float(dp.evalf(subs={x: pi/2}))
    
    print(f"f'(pi/2): {dpevaled} vs p6'(pi/2): {dfevaled}")
    ea = abs(dfevaled - dpevaled)
    er = ea / dfevaled
    
    print(f"Error absoluto: {ea} vs Error relativo: {er}")
    
    p1 = Taylor(f, 1, pi/4)
    p1.generate()
    p8 = Taylor(f, 8, pi/4)
    p8.generate()
    
    xIntervals = np.linspace(-2*pi, 2*pi, 100)
    
    p1eval = [p1.evaluate(x) for x in xIntervals]
    p8eval = [p8.evaluate(x) for x in xIntervals]
    feval = [float(f(x)) for x in xIntervals]
    
    
    plt.plot(xIntervals, p1eval, label="P1(x)")
    plt.plot(xIntervals, p8eval, label="P8(x)")
    plt.plot(xIntervals, feval, label="f(x) - No se porque no salen las otras funciones :/")
    plt.legend()
    plt.show()
    
e1()
e2()