#!/usr/bin/python3
# -*- coding: utf8 -*-

# Se recomienda no usar el modo interactivo de los programas porque no
# ha sido probado completamente, en lugar de eso se recomienda usar el modo
# no interactivo desde consola
# probado en Python 3.6 (3.6.0 [GCC 6.3.1 20170109]) sobre Linux 4.4

"""
falsa-posicion.py

Copyright 2017 Angel Leon <luianglenlop@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.
"""

import sys
"""from polinomios import *
import time
from utilidades.funciones import PolMaclaurin"""

from utilidades.lectores import leer_csignif, leer_poly, leer_intervalo
from utilidades.polinomios import evaluar_poly, derivar_poly
from math import sin, cos, pi
from utilidades.util import factorial, calc_toler
from utilidades.Errores import MaxIteraciones


def imprimir_ayuda():
    mensaje = """Uso:
    Modo no interactivo:
        falsa-posicion.py POLINOMIO X0 XF CIFRAS_SIGNIFICATIVAS
"""
    print(mensaje)


def modo_interactivo():
    print("Metodo falsa posición")


def falsa_posicion(coef, exp, x0, xf, n_signif):
    tolerancia = 0.05 * 10 ** (2 - n_signif)
    error = tolerancia * 2
    xm_anterior = None
    cont = 0
    xm = None
    while abs(error) > tolerancia:
        fx0 = evaluar_poly(coef, exp, x0)
        fxf = evaluar_poly(coef, exp, xf)
        xm = (xf * fx0 - x0 * fxf) / (fx0 - fxf)
        fxm = evaluar_poly(coef, exp, xm)
        if cont == 0:
            xm_anterior = xm * 2
        if xm == 0:
            xm += abs(x0 - xf) / 100.0
        if fxm == 0:
            break
        elif fx0 * fxm < 0:
            xf = xm
        elif fxm * fxf < 0:
            x0 = xm
        error = (xm - xm_anterior) * 100.0 / xm
        xm_anterior = xm
        # xm = (x0 + xf) / 2.0
        cont += 1
        if cont == 1001:
            raise MaxIteraciones
    return xm


def main(argv):
    # coef, exp = leer_poly()
    # coef_deriv, exp_deriv = derivar_poly(coef, exp)
    c_signif = leer_csignif()
    x0 = 0.1
    xf = 4
    coef = []
    exp = []
    k = 0
    i = 1
    toler = calc_toler(c_signif)
    error = toler * 2
    raiz = None
    while error > toler:
        if k % 2 == 0:
            """terminos del polinomio de Maclaurin con k par tienen coeficiente cero por
            deriv_k_esima(sen) = +sen ó -sen"""


            k += 1
            continue
        coef.append(((-1) ** i) / factorial(k))
        exp.append(k)
        try:
            raiz = falsa_posicion(coef, exp, x0, xf, c_signif)
        except Exception as ex:
            print(ex)
            raise
        if raiz is not None:
            error = ((pi - raiz) / pi) * 100
        if k > 10000:
            raise MaxIteraciones
        k += 1
        i += 1
    print("Se encontró\n pi = ", raiz)
    print("Con el polinomio de Maclaurin de {} terminos".format(k))
    print("De los cuales {} son No nulos".format(i-1))
    print("")
    coef.reverse()
    exp.reverse()
    for i in range(len(coef)):
        print("{}x^{}".format(coef[i], exp[i]), end="  ")
    print("")


if __name__ == '__main__':
    try:
        while True:
            main(sys.argv)
    except KeyboardInterrupt:
        print("Saliendo")
