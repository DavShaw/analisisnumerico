import sympy as sp
import math as mt
import numpy as np
from matplotlib import pyplot as plt

class Taylor():
    def __init__(self, function = None, n = 5, a = 1):
        if function:
            self.func = function
            self.original = function
        else:
            self.original = "x**2"
            self.func = "x**2"
        self.n = n
        self.a = a
        self.x = sp.symbols("x")
        self.func = sp.sympify(self.func)
        self.poly = None
        
        self.__derivatesvalues = []
        self.__derivatesfunc = []
        self.__xList = []
        self.__factList = []
        
    def getDerivates(self):
        return self.__derivatesfunc
    
    def getPoly(self):
        return self.poly
        
    def evaluate(self, n = None):
        if not self.poly is None:
            if self.n:
                return self.poly.subs(self.x,n)
            else:
                return self.poly.subs(self.x, self.a)
        else:
            raise("Cannot evaluate poly if it's none (Execute 'generate' first)")
    
    def generate(self):
        self.__xList = [n for n in range(self.n + 1)]
        self.__derivatesfunc = [sp.diff(self.func,self.x,n) for n in self.__xList]
        self.__derivatesvalues = [f.evalf(subs={self.x:self.a}) for f in self.__derivatesfunc]
        self.__factList = [mt.factorial(n) for n in self.__xList]
        poly = 0
        for i in self.__xList:
            expression = (self.__derivatesvalues[i]/self.__factList[i]) * ((self.x - self.a)**i)
            poly += expression
            
        self.poly = sp.simplify(poly)
        
    def graph(self, xlim = 20, ylim = 20):
        function = self.func
        poly = self.poly
        x = []
        yf = []
        yp = []
        for i in range(self.n+1):
            x.append(i)
            yf.append(function.evalf(subs={self.x:i}))
            yp.append(poly.evalf(subs={self.x:i}))   
        plt.plot(x,yf)
        plt.plot(x,yp)
        plt.xlim(-xlim,xlim)
        plt.ylim(-ylim,ylim)
        plt.show()
        
    def __getMaxAbsValue(self,a,b):
        diff = sp.diff(self.__derivatesfunc[-1], self.x,1)
        maxPoint = sp.Abs(sp.maximum(domain=sp.Interval(a,b), f=diff, symbol=self.x))
        minPoint = sp.Abs(sp.minimum(domain=sp.Interval(a,b), f=diff, symbol=self.x))
        if maxPoint > minPoint:
            return maxPoint
        return minPoint

    def getError(self,x):
        return abs(self.original.evalf(subs={self.x:x}) - self.poly.evalf(subs={self.x:x}))
    def getCota(self,a,b):
        maxvalue = self.__getMaxAbsValue(a,b)
        r = maxvalue*(b-a)**(self.n+1)/mt.factorial(self.n+1)
        return float(r)