import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from Matrix import Matrix
matplotlib.use('Agg')

class Polys():
  
  def __init__(self, data):
    self.points = data
    self.poly = None
    
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
  data = [(1,56.5),(5,113.0)]
  p = Polys(data)
  p.generatePoly()
  p.graphData()
  p.graphPoly()
  p.showGraph()