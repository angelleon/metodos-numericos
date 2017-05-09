#!/usr/bin/python3
# -*- coding: utf8 -*-
"""


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
from lector_polinomios import *


def main(argv):
	(poly, str_poly, variable) = leer_poly()
	(a, b) = leer_intervalo()
	tolerancia = leer_tolerancia()
	#print("integral")
	valor_real = poly.integrar(a, b)
	error = tolerancia * 2
	aprox = 0
	n = 0
	cont = 0
	max_inter = False
	#print("ciclo")
	while abs(error) > tolerancia:
		n += 10
		#print("aprox")
		aprox = poly.sum_riemman(a, b, n)
		#print(aprox)
		error = (valor_real - aprox) * 100 / valor_real
		cont += 1
		if cont > 1000:
			max_inter = True
			break
	if max_inter:
		print("\nSe alcanzo el número máximo de iteraciones sin llegar a la pecisión deseada\n")
	print("""Valor real: %s
	Valor calculado: %s
	Iteraciones: %s
	n: %s
	Tolerancia: %s
	Error: %s""" % (str(valor_real), str(aprox), str(cont), str(n),str(tolerancia), str(error)))


if __name__ == '__main__':
	main(sys.argv)

