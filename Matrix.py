import numpy as np

class Matrix:
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
