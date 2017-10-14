#!/usr/bin/python3
# -*- coding: utf8 -*-

# Se recomienda no usar el modo interactivo de los programas porque no
# ha sido probado completamente, en lugar de eso se recomienda usar el modo
# no interactivo desde consola
# probado en Python 3.6 (3.6.0 [GCC 6.3.1 20170109]) sobre Linux 4.4

"""
newton_raphson.py

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
from utilidades.util import calc_toler
from utilidades.lectores import leer_csignif, leer_poly
from utilidades.polinomios import evaluar_poly, derivar_poly
from utilidades.Errores import MaxIteraciones


def newton_raphson(coef, exp, x0, toler, c_signif):
    if evaluar_poly(coef, exp, x0) == 0:
        print("x0 es raiz")
        return x0
    print(coef, exp)
    error = toler * 2
    cont = 0
    puntos = [[], []]
    xi = None
    while abs(error) > toler:
        fx0 = evaluar_poly(coef, exp, x0)
        (coef_deriv, exp_deriv) = derivar_poly(coef, exp)
        dfx0 = evaluar_poly(coef_deriv, exp_deriv, x0)
        xi = x0 - (fx0/dfx0)
        if xi == 0:
            xi += 0.1 * 10 ** (-c_signif)
        puntos[0].append([x0, xi])
        puntos[1].append([fx0, 0])
        error = (xi - x0) * 100.0/xi
        x0 = xi
        cont += 1
        if cont == 1001:
            raise MaxIteraciones
        """if evaluar_poly(coef, exp, xi) == 0:
            print("xi es raiz")
            break"""
    return xi


def main(argv):
    coef, exp = leer_poly()
    coef_deriv, exp_deriv = derivar_poly(coef, exp)
    c_signif = leer_csignif()
    toler = calc_toler(c_signif)
    raices = set()
    for i in range(-50, 50, 4):
        try:
            r = newton_raphson(coef_deriv, exp_deriv, i, toler, c_signif)
            raices.add(r)
        except MaxIteraciones:
            continue
    if len(raices) > 0:
        print("\nSe encontraron extremos locales en: ")
        for i in raices:
            print("x = ", i)
    else:
        print("No se encontraron raices")

if __name__ == '__main__':
    try:
        while True:
            main(sys.argv)
    except KeyboardInterrupt:
        print("Saliendo.....\n")
