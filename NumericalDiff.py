import sympy as sp
import json

# This class has been made by David, some A.I. has made the documentation, to don't waste time on it.
class NumericalDiff:
  
  def diffWithTable(self, xi: float, table: dict, selectedH = 0):
    """
    Calculates the numerical difference using a table of values.
    Args:
      xi (float): The x-value at which to calculate the difference.
      table (dict): A dictionary representing the table of values, where the keys are the x-values and the values are the corresponding y-values.
      selectedH (float, optional): The selected step size for difference calculation. Defaults to 0.
    Returns:
      float: The numerical difference at the given x-value.
    Raises:
      Exception: If xi is not present in the table.
      Exception: If the table has less than 2 values.
    """
    x = list(table.keys())
    y = list(table.values())
    
    if not (xi in x):
      raise Exception("xi is not in the table")
    if len(x) < 2:
      raise Exception("Table must have atleast 2 values")
    
    xiIndex = list(x).index(xi)
    if xiIndex == 0:
      h = selectedH if selectedH != 0 else x[xiIndex+1] - x[xiIndex]
      return self.forwardDiff(fxiplus1 = y[xiIndex+1], 
                              fxi = y[xiIndex],
                              h = h)
      
    elif xiIndex == len(x) - 1:
      h = selectedH if selectedH != 0 else x[xiIndex] - x[xiIndex-1]
      return self.backwardDiff(fximinus1 = y[xiIndex-1],
                               fxi = y[xiIndex],
                               h = h)
      
    else:
      h = selectedH if selectedH != 0 else x[xiIndex+1] - x[xiIndex-1]
      return self.centralDiff(fxiplus1 = y[xiIndex+1],
                             fximinus1 = y[xiIndex-1],
                             h = h)
      
  def forwardDiff(self, fxiplus1, fxi, h):
    """
    Calculates the forward difference approximation of the derivative of a function.

    Args:
      fxiplus1 (float): The value of the function at x_i+1.
      fxi (float): The value of the function at x_i.
      h (float): The step size.

    Returns:
      float: The approximate derivative of the function using the forward difference method.
    """
    return (fxiplus1 - fxi) / h
  
  def backwardDiff(self, fximinus1, fxi, h):
    """
    Calculates the backward difference approximation of the derivative.

    Args:
      fximinus1 (float): The function value at x_i-1.
      fxi (float): The function value at x_i.
      h (float): The step size.

    Returns:
      float: The approximate derivative value.
    """
    return (fxi - fximinus1) / h
  
  def centralDiff(self, fxiplus1, fximinus1, h):
    """
    Calculates the central difference approximation of the derivative of a function.

    Args:
      fxiplus1 (float): The value of the function at x + h.
      fximinus1 (float): The value of the function at x - h.
      h (float): The step size.

    Returns:
      float: The approximation of the derivative using the central difference method.
    """
    return (fxiplus1 - fximinus1) / (2 * h)
  
  def __eulerForward(self, h, xi, func):
    """
    Performs the Euler Forward method for numerical differentiation.
    Args:
      h (float): Step size.
      xi (float): Initial value.
      func (function): Function to be differentiated.
    Returns:
      float: Approximation of the derivative at xi.
    """
    return xi + h * func(xi)
  
  def __eulerBackward(self, h, xi, func):
    """
    Performs the Euler Backward method for numerical differentiation.
    Args:
      h (float): Step size.
      xi (float): Initial value.
      func (function): The function to be differentiated.
    Returns:
      float: The approximate value of the derivative at xi.
    """
    return xi - h * func(xi)

  def solveODE(self, h, xi, func, start=0, end=1, type="+", exact=True):
    """
    Solves an ordinary differential equation (ODE) using numerical methods.
    Args:
      h (float): Step size for the numerical method.
      xi (float): Initial value for the ODE.
      func (function): The function representing the ODE.
      start (int): The starting index for the iterations (default: 0).
      end (int): The ending index for the iterations (default: 1).
      type (str): The type of numerical method to use. Can be "+" for Euler Forward or "-" for Euler Backward (default: "+").
      exact (bool): Flag indicating whether to return the exact value of xi or round it to 3 decimal places (default: True).
    Returns:
      str: A JSON string representing the iterations of the ODE solution.
    Raises:
      Exception: If an invalid type is provided.
    """
    iterations = {}
    for i in range(start, end+1):
      if i == 0:
        iterations[i] = xi
        continue
      elif type == "+":
        xi = self.__eulerForward(h, xi, func)
      elif type == "-":
        xi = self.__eulerBackward(h, xi, func)
      else :
        raise Exception("Invalid type")
      iterations[i] = float(xi) if exact else round(float(xi), 3)
    return json.dumps(iterations, indent=2)
  
