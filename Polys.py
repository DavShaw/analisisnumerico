import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import sympy as sp
from Matrix import Matrix
import random
matplotlib.use('Agg')

class Polys():
  
  def __init__(self, data):
    self.points = data
    self.poly = None
    
  def minSqrtLinearRegression(self):
    x = [point[0] for point in self.points]
    y = [point[1] for point in self.points]
    Sy = sum(y)
    Sx = sum(x)
    x2 = [n**2 for n in x]
    Sx2 = sum(x2)
    xy = [x[i]*y[i] for i in range(len(x))]
    Sxy = sum(xy)
    n = min(len(x), len(y))
    denominator = (n*Sx2)-((Sx)**2)
    b = ((Sy*Sx2)-(Sx*Sxy))/denominator
    m = ((n*Sxy)-(Sx*Sy))/denominator
    self.poly = lambda x: m*x + b
    
  def lagangeInterpolation(self):
    x = [point[0] for point in self.points]
    y = [point[1] for point in self.points]
    xVar = sp.symbols('x')
    n = len(x)
    poly = 0
    for i in range(n):
      product = 1
      for j in range(n):
        if (i != j):
          product *= (xVar-x[j])/(x[i]-x[j])
      poly += product*y[i]
    self.poly = sp.lambdify(xVar, poly)
    
  def graphData(self):
    x = [point[0] for point in self.points]
    y = [point[1] for point in self.points]    
    plt.plot(x, y)
    
  def generatePoly(self):
    x = [point[0] for point in self.points]
    self.poly = lambda x: sum([point[1]*x**i for i, point in enumerate(self.points)])
    
  def evaluatePoly(self, n):
    if self.poly is None:
      raise ValueError('No polynomial generated')
    return self.poly(n)
  
  def graphPoly(self):
    if self.poly is None:
      raise ValueError('No polynomial generated')
    x = [point[0] for point in self.points]
    y = [self.poly(point[0]) for point in self.points]
    plt.plot(x, y)
  
  def generateMatrix(self) -> Matrix:
    x = [point[0] for point in self.points]
    a = []
    for i in range(len(x)):
      n = x[i]
      row = [n**i for i in range(len(x))]
      a.append(row)
    a = np.array(a)
    m = Matrix(a)
    return m
  
  def showGraph(self):
    plt.savefig('graph.png')
  
if __name__ == "__main__":
  x = [1940, 1945, 1950, 1955, 1960, 1965, 1970, 1975, 1980, 1985, 1990]
  y1 = [15000, 150000, 250000, 275000, 270000, 280000, 290000, 650000, 1200000, 1500000, 2750000]
  y2 = [100000, 850000, 1330000, 2500000, 3000000, 3700000, 4400000, 46600000, 4800000, 4420000, 5000000]
  pez = [(i,j) for i, j in zip(x, y1)]
  cangrejo = [(i,j) for i, j in zip(x, y2)]
  p = Polys(pez)
  c = Polys(cangrejo)
  p.lagangeInterpolation()
  lagrange = p.poly
  p.minSqrtLinearRegression()
  linear = p.poly
  
  # GRAPH FOR LAGRANGE INTERPOLATION
  
  x_smooth = np.linspace(min(x), max(x), 1000)
  y_smooth = [lagrange(i) for i in x_smooth]
  
  plt.plot(x_smooth, y_smooth, label='Lagrange Interpolation')
  plt.plot(x, y1, 'ro')
  plt.savefig('lagrange.png')
  
  # CLEAR PLOT
  plt.clf()
  
  # GRAPH FOR MINIMUM SQUARES LINEAR REGRESSION
  plt.plot(x, [linear(i) for i in x], label='Linear Regression')
  plt.plot(x, y1, 'ro')
  plt.savefig('linear.png')