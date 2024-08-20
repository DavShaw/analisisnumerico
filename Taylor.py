import sympy as sp
import math as mt
import matplotlib
import numpy as np
from matplotlib import pyplot as plt


class Taylor:
  """
  A class for generating and evaluating Taylor polynomials.
  Args:
    function (function, optional): The function to generate the Taylor polynomial for. Defaults to x^2.
    n (int, optional): The degree of the Taylor polynomial. Defaults to 5.
    a (int, optional): The point around which to generate the Taylor polynomial. Defaults to 1.
  Attributes:
    func_lambda (function): The lambda function representing the input function.
    n (int): The degree of the Taylor polynomial.
    a (int): The point around which the Taylor polynomial is generated.
    x (Symbol): The symbol 'x' used in the sympy library.
    func_sympy (Expr): The sympy expression representing the input function.
    poly (Expr): The sympy expression representing the generated Taylor polynomial.
    __derivatesvalues (list): The list of derivative values at the point 'a'.
    __derivatesfunc (list): The list of derivative functions.
    __xList (list): The list of values from 0 to 'n'.
    __factList (list): The list of factorials of values from 0 to 'n'.
  Raises:
    ValueError: If the Taylor polynomial is None and evaluate() is called.
  """
  def __init__(self, function=None, n=5, a=1):
    if function:
      self.func_lambda = function
    else:
      self.func_lambda = lambda x: x**2

    self.n = n
    self.a = a
    self.x = sp.symbols("x")
    self.func_sympy = sp.sympify(self.func_lambda(self.x))
    self.poly = None

    self.__derivatesvalues = []
    self.__derivatesfunc = []
    self.__xList = []
    self.__factList = []

  def getDerivates(self):
    """
    Returns the derivative function.

    Returns:
      list: The list of the derivatives of the function.
    """
    return self.__derivatesfunc
  
  def getPoly(self):
    """
    Returns the polynomial of the object.
    """
    return self.poly
      
  def evaluate(self, n=None):
    """
    Evaluates the polynomial at a given value or at the initial value if no value is provided.

    Parameters:
      n (float): The value at which to evaluate the polynomial. If not provided, the initial value is used.

    Returns:
      float: The result of evaluating the polynomial at the given value.

    Raises:
      ValueError: If the polynomial is None (i.e., not generated) and trying to evaluate it.
    """
    if self.poly is not None:
      if n is not None:
        return self.func_lambda(n)
      else:
        return self.func_lambda(self.a)
    else:
      raise ValueError("Cannot evaluate poly if it's None (Execute 'generate' first)")
  
  def generate(self):
    """
    Generates the Taylor polynomial approximation for the given function.
    Returns:
      None
    """
    self.__xList = [n for n in range(self.n + 1)]
    self.__derivatesfunc = [sp.diff(self.func_sympy, self.x, n) for n in self.__xList]
    self.__derivatesvalues = [float(f.evalf(subs={self.x: self.a})) for f in self.__derivatesfunc]
    self.__factList = [mt.factorial(n) for n in self.__xList]
    poly = 0
    for i in self.__xList:
      expression = (self.__derivatesvalues[i] / self.__factList[i]) * ((self.x - self.a) ** i)
      poly += expression

    self.poly = sp.simplify(poly)
      
  def graph(self, xlim=20, ylim=20):
    x_vals = np.linspace(-xlim, xlim, 400)
    y_func = [self.func_lambda(val) for val in x_vals]
    y_poly = [self.poly.evalf(subs={self.x: val}) for val in x_vals]

    plt.plot(x_vals, y_func, label="Original Function")
    plt.plot(x_vals, y_poly, label="Taylor Polynomial")
    plt.xlim(-xlim, xlim)
    plt.ylim(-ylim, ylim)
    plt.legend()
    plt.show()
      
  def __getMaxAbsValue(self, a, b):
    diff = sp.diff(self.__derivatesfunc[-1], self.x, 1)
    max_point = sp.Abs(sp.maximum(domain=sp.Interval(a, b), f=diff, symbol=self.x))
    min_point = sp.Abs(sp.minimum(domain=sp.Interval(a, b), f=diff, symbol=self.x))
    return max(max_point, min_point)

  def getError(self, x):
    return abs(float(self.func_lambda(x) - self.poly.evalf(subs={self.x: x})))
  
  def getCota(self, a, n):
    maxvalue = self.__getMaxAbsValue(a, n)
    r = maxvalue * (n - a) ** (self.n + 1) / mt.factorial(self.n + 1)
    return float(r)
