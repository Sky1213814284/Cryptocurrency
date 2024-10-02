import math
import sys
import random

def fieldArith(size, operand1, operation, operand2):
    def check(size,operand1,operand2):
        op1 = int(operand1)
        op2 = int(operand2)
        size = int(size)
        if op1 < 0:
            op1 = size - (abs(op1) % size)
        elif op1 > size:
            op1 = op1 % size
        if op2 < 0:
            op2 = size - (abs(op2) % size)
        elif op2 > size:
            op2 = op2 % size
        return size, op1, op2 

    def addition(size, operand1, operand2):
        return (operand1 + operand2) % size

    def multiplication(size, operand1, operand2):
        return (operand1*operand2) % size
    
    def exponentiation(size, operand1, operand2):
        return (operand1 ** operand2) % size

    def subtraction(size, operand1, operand2):
        temp = operand1 - operand2
        if temp < 0:
            return temp + size
        else:
            return temp
    def multInverse(size, operand2):
        return (operand2 ** (size - 2)) % size
    
    def division(size, operand1, operand2):
        return multiplication(size, operand1, multInverse(size, operand2))
    
    size, op1, op2 = check(size,operand1, operand2)
    if(operation == "+"):
        return addition(size, op1, op2)
    elif(operation == "-"):
        return subtraction(size, op1, op2)
    elif(operation == "times"):
        return multiplication(size, op1, op2)
    elif(operation == "/"):
        return division(size, op1, op2)
    elif(operation == "expo"):
        return exponentiation(size, op1, op2)

def genRand(range):
    range = int(range)
    return random.randint(1, range - 1)

def pointAdd(size, x1, y1, x2, y2):
    if x1 == x2 and y1 == -y2:
        return None, None
    if (x1 == None and y1 == None) and (x2 != None and y2 != None):
        return x2, y2
    elif (x1 != None and y1 != None) and (x2 == None and y2 == None):
        return x1, y1
    elif (x1 == None and y1 == None) and (x2 == None and y2 == None):
        return None, None
    slope = 0
    if x1 == x2 and y1 == y2:
        slope = fieldArith(size, 3*(x1**2), "/", 2*y1)
    else:
        ydiff = fieldArith(size, y2, "-", y1)
        xdiff = fieldArith(size, x2, "-", x1)
        slope = fieldArith(size, ydiff, "/", xdiff)
    msquare = fieldArith(size, slope, "expo", 2)
    x1px2 = fieldArith(size, x1, "+", x2)
    x3 = fieldArith(size, msquare, "-", x1px2)
    x1subx3 = fieldArith(size, x1, "-", x3)
    mmult = fieldArith(size, slope, "times", x1subx3)
    y3 = fieldArith(size, mmult, "-", y1)
    return x3, y3

def userid():
    print("yz5zys")

def pointMul(size, k, x1, y1):
    k = int(k)
    size = int(size)
    x1 = int(x1)
    y1 = int(y1)
    bin = format(k, "b")
    l = list(bin.strip())
    maxPow = len(l)
    pointList = []
    currX = x1
    currY = y1
    for i in range(maxPow):
        pointList.append((currX, currY))
        currX, currY = pointAdd(size, currX, currY, currX, currY)
    n = 0
    resultX = None
    resultY = None
    length = len(l)
    while n < length:
        if(l[length - n - 1]) == "1":
            if resultX == None and resultY == None:
                resultX, resultY = pointList[n][0], pointList[n][1]
            else:
                resultX, resultY = pointAdd(size, resultX, resultY, pointList[n][0], pointList[n][1])
        n += 1
    return resultX, resultY
    
def _genkey(mod, order, Gx, Gy):
    mod = int(mod)
    order = int(order)
    Gx = int(Gx)
    Gy = int(Gy)
    privKey = genRand(order)
    finalX, finalY = pointMul(mod, privKey, Gx, Gy)
    return privKey, finalX, finalY

def genkey(mod, order, Gx, Gy):
    privKey, finalX, finalY = _genkey(mod, order, Gx, Gy)
    while finalX == 0 and finalY == 0:
        privKey, finalX, finalY = _genkey(mod, order, Gx, Gy)
    print(privKey)
    print(finalX)
    print(finalY)

def _sign(mod, order, Gx, Gy, d, h):
    #random OTP k
    k = genRand(order)
    #multiplicative inverse of k
    kinv = fieldArith(order, 1, "/", k)
    r, _ = pointMul(mod, k, Gx, Gy)
    #r*d
    rd = fieldArith(order, r, "times", d)
    #h + r*d
    hrd = fieldArith(order, h, "+", rd)
    #k-1 (h + r*d)
    s = fieldArith(order, kinv, "times", hrd)
    return r, s

def sign(mod, order, Gx, Gy, d, h):
    r, s = _sign(mod, order, Gx, Gy, d, h)
    print(r)
    print(s)
    

def _verify(mod, order, Gx, Gy, Qx, Qy, r, s, h):
    #s inverse
    sinv = fieldArith(order, 1, "/", s)
    #s^-1 * h
    sinvh = fieldArith(order, sinv, "times", h)
    #s^-1 * r
    sinvr = fieldArith(order, sinv, "times", r)
    #(s^-1 * h) * G
    sinvhGx, sinvhGy = pointMul(mod, sinvh, Gx, Gy)
    #(s^-1 * r) * Q
    sinvrQx, sinvrQy = pointMul(mod, sinvr, Qx, Qy)
    #R
    Rx, _ = pointAdd(mod, sinvhGx, sinvhGy, sinvrQx, sinvrQy)
    if Rx == int(r):
        return True
    else:
        return False

def verify(mod, order, Gx, Gy, Qx, Qy, r, s, h):
    print(_verify(mod, order, Gx, Gy, Qx, Qy, r, s, h))

def test(size, x1, y1, x2, y2):
    size = int(size)
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    print(pointAdd(size, x1, y1, x2, y2))

if __name__ == '__main__':
    args = sys.argv
    globals()[args[1]](*args[2:])
