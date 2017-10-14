#!/usr/bin/python3
# -*- coding: utf8 -*-

import sys
from math import sin, pi
from utilidades.lectores import leer_real, leer_csignif
from utilidades.util import calc_toler


def leer_intervalo():
    x0 = leer_real("Ingrese primer punto del intervalo\n(x0): ")
    k0 = x0 // pi
    k1 = (k0 + 1) * pi
    k2 = (k0 + 2) * pi
    while True:
        xf = leer_real("Ingrese un número entre {} y {}".format(k1, k2))
        if not (k1 < xf < k2):
            print("¡ Valor no valido ¡")
        else:
            break
    if k0 % 2 != 0:
        k0 += 1
    x0 -= k0 * pi
    xf -= k0 * pi
    return x0, xf


def biseccion(x0, xf, toler):
    error = toler * 2
    i = 0
    xm = None
    xm_anterior = None
    while error > toler:
        xm_anterior = xm
        xm = (x0 + xf) / 2
        fx0 = sin(x0)
        fxm = sin(xm)
        fxf = sin(xf)
        if fx0 * fxm < 0:
            xf = xm
        elif fxm * fxf < 0:
            x0 = xm
        elif fxm == 0:
            break
        if i != 0:
            error = 100 * abs(xm - xm_anterior) / xm
        i += 1
    return xm, i, error


def print_info(pi_aprox, toler, error, iteraciones):
    print("\n\n===========================================================")
    print("Valor calculado: {}".format(pi_aprox))
    print("Tolerancia: {}".format(toler))
    print("Error: {}".format(error))
    print("Iteraciones: {}".format(iteraciones))
    print("===========================================================\n\n")


def main(argv):
    c = leer_csignif()
    toler = calc_toler(c)
    x0, xf = leer_intervalo()
    print("intervalo real {} {}".format(x0, xf))
    pi_aprox, iteraciones, error = biseccion(x0, xf, toler)
    print_info(pi_aprox, toler, error, iteraciones)


if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print("Operación cancelada")
