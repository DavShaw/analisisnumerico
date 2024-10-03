<<<<<<< HEAD
from Matrix import Matrix
import numpy as np
m = np.matrix([[3, 2, -1],
               [-2, 9, -6],
               [-1, 1, -1]])
e = np.matrix([1, 3, 5]).T
matrix = Matrix(m)
matrix.addExtendedMatrix(e)
matrix.gaussJordanElimination()
matrix.printMatrix()
=======
import Matrix, numpy as np
if __name__ == '__main__':
  a = np.array([[1,1],
       [1,5]])
  b = np.array([56.5, 113.0])
  A = Matrix.Matrix(a)
  A.append(b)
  x0 = np.zeros(len(b))
  r = A.jacobiMatrix((10**(-100000)),x0)
  print(r)
  print(np.dot(a,r)-b)
>>>>>>> b3eabf23988f79d010b30360ba6baab64a543011
