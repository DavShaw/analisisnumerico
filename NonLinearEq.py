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
    """ 
    Sea y = f(x) una función continua en el intervalo [a,b] y que se cumple el self.__mediumTheorem(a,b)
    Existe un c en [a,b] tal que f(c) = 0 (Es raíz)
    Sean los intervalos
    (a,f(a)) -> (c,f(c)) que es igual a  (a, fa) -> (c, 0) [Intervalo 1]
    (c,f(c)) -> (b,f(b)) que es igual a  (c, 0) -> (b, fb) [Intervalo 2]
    Hallaremos dos pendientes
    Para m1, m2 usaremos intervalor 1, 2 respectivamente
    m1 = fa/(a-c)
    m2 = fb/(b-c)
    Buscamos que las dos pendientes sean iguales: m1 = m2 -> fa/(a-c) = fb/(b-c).
    Despejemos en función de C -> c = (a*fb - b*fa)/(fb - fa)
    Tenemos la raiz!
    """
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
        
if __name__ == "__main__":
  f = lambda x: x**2 - 2
  solver = NonLinearEquation(f)
  error = 1e-5
