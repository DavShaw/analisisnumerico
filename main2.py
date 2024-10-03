from Polys import Polys
x = [1,2,5,10,20,30,40]
y = [56.5, 78.6, 113, 144.5, 181, 205, 214.5]
data = [(x[i],y[i]) for i in range(len(x))]
p = Polys(data)
m = p.generateMatrix()
m.printMatrix()
