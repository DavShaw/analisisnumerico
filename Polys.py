import numpy as np
import matplotlib.pyplot as plt
import matplotlib
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
  data = [(0,0.120),(2,0.153), (3,0.170), (6,0.225), (7,0.260), (1,0.135), (4,0.200), (5,0.215), (8,0.280), (9,0.300), (10,0.320), (11,0.340), (12,0.360), (13,0.380), (14,0.400)]
  p = Polys(data)
  p.minSqrtLinearRegression()
  x = [d[0] for d in data]
  y = [d[1] for d in data]
  py = [p.evaluatePoly(n) for n in x]
  
  plt.plot(x,y,".")
  plt.plot(x,py, color="red")
  plt.savefig("axd.png")