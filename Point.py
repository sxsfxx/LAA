import math
from fractions import Fraction

class Point:
    def __init__(self, x, y, z):
        self.x = Fraction(x)
        self.y = Fraction(y)
        self.z = Fraction(z)
    
    def __str__(self):
        return "({0},{1},{2})".format(self.x, self.y, self.z)
    
    def __repr__(self):
        return self.__str__()
    
    def zero(self):
        return self.x==0 and self.y==0 and self.z==0
    
    def mod(self):
        x = self.x*self.x + self.y*self.y + self.z*self.z
        y = Fraction(math.sqrt(x))
        if y*y == x:
            return (True, y)
        else:
            return (False, x)
    
    def normalize(self):
        if self.zero():
            raise ZeroDivisionError()
        m = self.mod()
        if m[0]:
            self.x /= m[1]
            self.y /= m[1]
            self.z /= m[1]
            return self
        else:
            raise ValueError()
    
    def __mul__(a, b):
        return a.x*b.x + a.y*b.y + a.z*b.z
    
    def __matmul__(a, b):
        i = a.y*b.z - a.z*b.y
        j = -1*(a.x*b.z - a.z*b.x)
        k = a.x*b.y - a.y*b.x
        return Point(i,j,k)