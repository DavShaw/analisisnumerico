import sympy as sp
import json

class NumericalDiff:
  def forward(self, h, xi, func):
    return xi + h * func(xi)
  
  def backward(self, h, xi, func):
    return xi - h * func(xi)

  def solveODE(self, h, xi, func, start = 0, end = 1, type="+", exact=True):
    iterations = {}    
    for i in range(start, end+1):
      if i == 0:
        iterations[i] = xi
        continue
      if type == "+":
        xi = self.forward(h, xi, func)
      else: 
        xi = self.backward(h, xi, func)
      iterations[i] = float(xi) if exact else round(float(xi), 3)
    return json.dumps(iterations, indent=2)

  def solveODELimited(self, h, xi, func, start, end, type, limitAt):
    iterations = self.solveODE(h, xi, func, start, end, type)
    index = 0
    while True:
      if iterations[index] >= limitAt:
        return(index, iterations[index])
      index += 1