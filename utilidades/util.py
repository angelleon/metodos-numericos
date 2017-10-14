from math import sqrt

def es_cuadrado(n=0):
    n = sqrt(n)
    if n != round(n):
        return False
    return True

def calc_toler(c):
    return 0.5 * 10 ** (2 - c)

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
