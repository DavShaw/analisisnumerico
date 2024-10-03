import sympy as sp

class NonLinearEquation:
  def __init__(self, f):
    self.x = sp.symbols('x')
    self.f = f(self.x)
        
  def __mediumTheorem(self, a, b):
    fa = self.f.subs(self.x, a)
    fb = self.f.subs(self.x, b)
    check = (fa * fb) < 0
    return True if check else False
  
  def bisect(self, a, b, error = 0, getIterations = False):
    iterations = 0

    if error == 0:
      error = 1e-2
    if not self.__mediumTheorem(a, b):
      errorMsg = f'Cannot apply bisection method. [{a},{b}] does not contain C.'
      raise ValueError(errorMsg)
    
    while True:
      c = (a + b) / 2
      
      if abs(a-b) <= error:
        if not getIterations:
          return c
        return (c, iterations)
      if self.__mediumTheorem(a,c):
        b = c
      else:
        a = c

      iterations += 1

  def fakePosition(self, a, b, error = 0, getIterations = False):
    iterations = 0

    if error == 0:
      error = 1e-2

    if not self.__mediumTheorem(a, b):
      errorMsg = f'Cannot apply false position method. [{a},{b}] does not contain C.'
      raise ValueError(errorMsg)
        
    fa = self.f.subs(self.x, a)
    fb = self.f.subs(self.x, b)
        
    while True:
      c = (a*fb - b*fa) / (fb-fa)
      fc = self.f.subs(self.x, c)
      if abs(fc) <= error:
        if not getIterations:
          return float(c)
        return (float(c), iterations)
      if self.__mediumTheorem(a, c):
        b = c
        fb = fc
      else:
        a = c
        fa = fc

      iterations += 1