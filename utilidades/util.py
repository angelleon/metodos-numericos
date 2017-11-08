

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


def continuar():
    """Función para controlar el ciclo de la función spam()
    requiere la función esté en una estructura
    try: while True: spam(); except KeyboardInterrupt: exit(0)
    o similar"""
    while True:
        answ = input("\n¿Desea continuar?\n\n<Enter> Continuar\n2. Salir\n(opción): ")
        if len(answ) == 0:
            break
        try:
            answ = int(answ)
            if answ == 2:
                raise KeyboardInterrupt
        except ValueError:
            continue
