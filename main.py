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