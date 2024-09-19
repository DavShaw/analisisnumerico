import Matrix, numpy as np
if __name__ == '__main__':
  a = np.array([[3,-1,0],
       [-1,4,-1],
       [0,-1,5]])
  b = np.array([2,3,5])
  A = np.insert(a,a.shape[0],b,1)
  A = Matrix.Matrix(A)
  x0 = np.zeros(len(b))
  r = A.jacobiSum((10**(-2)),x0, limit=10000000)
  print(r)
  print(np.dot(a,r)-b)