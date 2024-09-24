import Matrix, numpy as np
if __name__ == '__main__':
  a = np.array([[1,1],
       [1,5]])
  b = np.array([56.5, 113.0])
  A = np.insert(a,a.shape[0],b,1)
  A = Matrix.Matrix(A)
  x0 = np.zeros(len(b))
  r = A.jacobiMatrix((10**(-100000)),x0)
  print(r)
  print(np.dot(a,r)-b)