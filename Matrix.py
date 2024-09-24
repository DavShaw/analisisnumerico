import numpy as np

class Matrix:
  
  def __init__(self, a):
    self.a = a
    
  def getRow(self,n):
    if n > (len(self.a)-1):
      raise IndexError("Out of the range")
    m = self.a[n]
    return m[:-1]
  
  def getColumn(self, n):
    if len(self.a) == 0 or n > (len(self.a[0]) - 1):
      raise IndexError("Out of the range")
    column = []
    for i in range(len(self.a)):
      row = self.getRow(i)
      column.append(row[n])
    return column
      
  def swapRows(self, i, j):
    self.a[i], self.a[j] = self.a[j].copy(), self.a[i].copy()
    
  def printMatrix(self):
    for i in range(len(self.a)):
      print(f"{self.a[i]}")
      
  def gaussJordan(self):
    n = len(self.a)
    for k in range(n-1):
      if self.a[k,k] == 0:
        i=1
        while self.a[k+i,k] == 0 and k+i < n:
          i+=1
        self.swapRows(k, k+i)
      for i in range(k+1, n):
        lam = self.a[i,k]/self.a[k,k]
        self.a[i, 0:(n+1)] = self.a[i, 0:(n+1)] -lam*self.a[k, 0:(n+1)]
        
  def __getSolutions(self):
    n = len(self.a)
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
      x[i] = (self.a[i, n] - np.dot(self.a[i, i+1:n], x[i+1:n]))/self.a[i,i]
    return x
  
  def jacobiSum(self, tolerance, x0, limit = 100):
    a = []
    b = []
    for i in range(len(self.a)):
      a.append(self.a[i][:-1])
      b.append(self.a[i][-1])
    size = np.shape(a)
    n = size[0]
    m = size[1]
    difference = np.ones(n, dtype=float)
    error = np.max(difference)
    X = np.copy(x0)
    newX = np.copy(x0)

    iteration = 0
    while not(error <= tolerance or iteration > limit):

      for i in range(0, n, 1):
        newValue = b[i]
        for j in range(0, m, 1):
          if (i != j): # except diagonal of a
            newValue = newValue - a[i, j] * X[j]
        newValue = newValue / a[i, i]
        newX[i] = newValue
        difference = np.abs(newX - X)
        error = np.max(difference)
        X = np.copy(newX)
        iteration = iteration + 1
    X = np.transpose([X])
    # Does not converge
    if (iteration > limit):
      X = iteration
      print('Limit hit. Method did not converge')
    return(X)
          
  def jacobiMatrix(self, error, x0):
    a = []
    b = []
    for i in range(len(self.a)):
      a.append(self.a[i][:-1])
      b.append(self.a[i][-1])
    
    # Diagonal matrix
    d = np.diag(np.diag(a))
    
    # Upper and lower triangular matrix
    u = d - np.triu(a)
    l = d - np.tril(a)
    
    # Iteration matrix
    tj = np.dot(np.linalg.inv(d),l+u)
    cj = np.dot(np.linalg.inv(d), b)
    
    propValues, _ = np.linalg.eig(tj)
    
    radio = max(abs(propValues))
    if radio > 1:
      raise ValueError("The iteration matrix does not converge")
    elif radio == 1:
      raise ValueError("Cannot determine convergence")
    else:
      x1 = np.dot(tj,x0) + cj
      while (max(abs(x1-x0)) > error):
        x0 = x1
        x1 = np.dot(tj,x0) + cj
      return x1
    
  def printSolution(self):
    x = self.__getSolutions()
    print(x)
    

  