import numpy as np

class Matrix:
<<<<<<< HEAD
    def __init__(self, matrix: np.matrix, extendedMatrix: np.matrix = None):
        self.matrix: np.matrix = matrix
        self.extendedMatrix: np.matrix = extendedMatrix

    def addExtendedMatrix(self, extendedMatrix: np.matrix):
        if extendedMatrix.shape[0] != self.matrix.shape[0]:
            raise ValueError("Extended matrix must have the same number of rows as the base matrix.")
        self.extendedMatrix = extendedMatrix.reshape(-1, 1)

    def swapRows(self, row1: int, row2: int):
        if not self.__isMatrixExtended():
            raise Exception("Matrix is not extended")
        self.matrix[[row1, row2], :] = self.matrix[[row2, row1], :]
        self.extendedMatrix[[row1, row2], :] = self.extendedMatrix[[row2, row1], :]

    def __isMatrixExtended(self):
        return self.extendedMatrix is not None and self.matrix is not None

    def printMatrix(self):
        if not self.__isMatrixExtended():
            raise Exception("Matrix is not extended")
        for i in range(len(self.matrix)):
            print(f"{self.matrix[i]} | {self.extendedMatrix[i][0]}") 

    def __swapToPreventErros(self):
        if self.matrix[0,0] == 0:
            self.swapRows(0,1)

        if self.matrix[1,1] == 0:
            self.swapRows(1,2)

        if self.matrix[2,2] == 0:
            raise ValueError("Matrix has no unique solution")

    def gaussJordanElimination(self):
        # Copied from Leidy
        a = self.matrix
        b = self.extendedMatrix
        n = len(a)

        self.__swapToPreventErros()

        for j in range(n-1):
            for i in range(j+1,n):
                factor = a[i,j]/a[j,j]
                a[i,j:n] = a[i,j:n] - factor*a[j,j:n]
                b[i] = b[i] - factor*b[j]
=======
  
  def __init__(self, a):
    self.a = a
    
  def append(self, b):
    a = self.a
    A = np.insert(a,a.shape[0],b,1)
    self.a = A
    
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
    
    
    
"""

import numpy as np
import time

A = np.array([[1,1], [1,5]])
b = np.array([56.5,113.0])
tol = 1e-6
x0 = np.zeros(len(b))

def Jacobi_Mx_sum(A, b, x0, tol):
    n = len(b)
    x1 = np.zeros(n)
    count = 0
    diff = tol + 1
    start_time = time.time()

    while diff > tol:
        count += 1
        x_nuevo = np.zeros(n)
        for i in range(n):
            suma = np.dot(A[i, :], x0) - A[i, i] * x0[i]
            x_nuevo[i] = (b[i] - suma) / A[i, i]
        diff = np.max(abs(x_nuevo - x0))
        x0 = x_nuevo
    end_time = time.time()

    print("iteraciones:", count)
    print("timepo:", end_time - start_time)
    return x0

Jacobi_Mx_sum(A, b, x0, tol)


    
"""

  
>>>>>>> b3eabf23988f79d010b30360ba6baab64a543011
