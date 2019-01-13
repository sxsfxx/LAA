from pprint import pprint
from fractions import Fraction
import copy
import random
import unittest

def list22(m, n, x=0):
    return [ [x for j in range(n)] for i in range(m)]

def calcDet(data, base=0):
    #pprint(data)
    n = len(data)
    if n == 1:
        return data[0][0]
    elif n == 2:
        return data[0][0]*data[1][1] - data[0][1]*data[1][0]
    # >= 3, calculate by the definition recursively
    res = 0
    for i in range(n):
        x = data[base][i]
        det = copy.deepcopy(data)
        del det[base]
        for r in det:
            del r[i]
        #pprint(det)
        d = calcDet(det, 0)
        res += x * (-1)**(base+1+i+1) * d
    return res

def calcAlgCofactor(data):
    result = list22(len(data), len(data))
    for i in range(len(data)):
        for j in range(len(data)):
            # dig the specific row and column
            det = copy.deepcopy(data)
            del det[i]
            for r in det:
                del r[j]
            d = calcDet(det)
            A = (-1)**(i+1+j+1)*d
            result[i][j] = A
    return result

def equalMatrix(left, right):
    return left==right

def transposeMatrix(data):
    m = len(data)
    n = len(data[0])
    result = list22(n, m)
    for i in range(m):
        for j in range(n):
            result[j][i] = data[i][j]
    return result

def inverseMatrix(data):
    d = calcDet(data)
    if d == 0:
        return None
    else:
        A = calcAlgCofactor(data)
        for c in A:
            for i in range(len(c)):
                c[i] /= d
        return transposeMatrix(A)

def simplifyLadder(data):
    rows = copy.deepcopy(data)
    r = len(rows)
    c = len(rows[0])
    for i in range(c):
        # to find the first non-zero row
        zero = True
        for j in range(i, r):
            if rows[j][i] != 0:
                zero = False
                break
        if not zero:
            # move the non-zero row to the current row
            if j != i:
                rows[i],rows[j] = rows[j],rows[i]
            # transfer the header to 1
            if rows[i][i] != 1:
                factor = rows[i][i]
                for k in range(i, c):
                    rows[i][k] /= factor
            #pprint(rows[i])
            # eliminate the first element to 0 for all following rows
            for k in range(i+1, r):
                if rows[k][i] != 0:
                    factor = rows[k][i]
                    for s in range(i, c):
                        rows[k][s] -= rows[i][s]*factor
                #pprint(rows[k])
    #pprint(rows)
    # till now, it's already like the upper triangle matrix
    # continue to simplify and eliminate more non-zero
    for i in range(1, r):
        # locate the beginning 1
        k = -1
        for j in range(c):
            if rows[i][j] != 0:
                k = j
                break
        if k == -1: # all in the current row are 0
            break
        else:
            # try to eliminate non-zero in upper rows
            for j in range(i):
                if rows[j][k] != 0:
                    factor = rows[j][k]
                    for s in range(k, c):
                        rows[j][s] -= rows[i][s]*factor
    #pprint(rows)
    # if a row contains all 0 in middle, move to bottom
    n = r-1
    i = 0
    while i<n:
        print("\ni={}, n={}".format(i, n))
        row = copy.deepcopy(rows[i])
        if all(map(lambda x:x==0, row)):
            del rows[i]
            rows.append(row)
            n -= 1
        else:
            i += 1
        #pprint(rows)
    return rows

def multiplyMatrix(left, right):
    # ms * sn
    m = len(left)
    s = len(left[0])
    if len(right) != s:
        return None
    n = len(right[0])
    res = list22(m, n)
    for i in range(m):
        for j in range(n):
            t = 0
            for k in range(s):
                t += left[i][k] * right[k][j]
            res[i][j] = t
    return res
    
class MyTest(unittest.TestCase):
    @staticmethod
    def newMatrix(m, n):
        data = list22(m, n)
        for i in range(m):
            for j in range(n):
                data[i][j] = Fraction(random.randint(-10, 10))
        return data
    
    def test_calcDet(self):
        for n in (2, 3, 4, 7):
            data = MyTest.newMatrix(n, n)
            pprint(data)
            d0 = calcDet(data, 0)
            d1 = calcDet(data, 1)
            print(d0, d1)
            self.assertEqual(d0, d1)
    
    def test_calcAlgCofactor(self):
        for n in (2, 3, 4, 7):
            data = MyTest.newMatrix(n, n)
            pprint(data)
            res = calcAlgCofactor(data)
            pprint(res)
    
    def test_transposeMatrix(self):
        data = MyTest.newMatrix(5, 3)
        pprint(data)
        t = transposeMatrix(data)
        pprint(data)
    
    def test_inverseMatrix(self):
        for n in (2, 3, 4, 7):
            data = MyTest.newMatrix(n, n)
            pprint(data)
            inv = inverseMatrix(data)
            if inv:
                inv2 = inverseMatrix(inv)
                self.assertEqual(inv2, data)
    
    def test_multiplyMatrix(self):
        left = MyTest.newMatrix(5, 3)
        pprint(left)
        right = MyTest.newMatrix(3, 4)
        pprint(right)
        res = multiplyMatrix(left, right)
        pprint(res)


if __name__ == "__main__":
    unittest.main()
