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
  
  def __intoTheInterval(self, a, b, c):
    if a < c < b or b < c < a:
      return True
    return False
  
  def bisect(self, a, b, error = 0):
    if error == 0:
      error = 1e-2
    if not self.__mediumTheorem(a, b):
      errorMsg = f'Cannot apply bisection method. [{a},{b}] does not contain C.'
      raise ValueError(errorMsg)
    
    while True:
      c = (a + b) / 2
      
      if abs(a-b) < error:
        return c
      if self.__mediumTheorem(a,c):
        b = c
      else:
        a = c
        
if __name__ == "__main__":
  f = lambda x: x**2 - 6
  solver = NonLinearEquation(f)
  result = solver.bisect(a = 1, b = 3)
  print(result)
