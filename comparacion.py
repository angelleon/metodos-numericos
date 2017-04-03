#!/usr/bin/python3
# -*- coding: utf8 -*-

# Se recomienda no usar el modo interactivo de los programas porque no
# ha sido probado completamente, en lugar de eso se recomienda usar el modo
# no interactivo desde consola
# probado en Python 3.6 (3.6.0 [GCC 6.3.1 20170109]) sobre Linux 4.4

"""
comparacion.py

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
import time
from polinomios import *
from newton_raphson import newton_raphson, graficar_newton
from secante import secante, graficar_secante


def modo_interactivo():
	return introducir_parametros()


def imprimir_ayuda():
	texto_ayuda =\
	"""Uso:
	no interactivo:
		secante.py POLINOMIO X0 Xf CIFRAS-CONFIANZA
	imprimri esta ayuda
		secante.py [-h | --help]
	"""


def main(argv):
	if len(argv) == 1:
		parametros = modo_interactivo()
	elif len(argv) == 2 and (argv[1] == "-h" or argv[1] == "--help"):
		imprimir_ayuda()
		return
	elif len(argv) != 5:
		print("El programa recible 4 argumentos, %d dados" % (len(argv) - 1))
		imprimir_ayuda()
		return
	elif len(argv) == 5:
		try:
			parametros = analizar_poly(argv[1])
		except (FuncionMultivariable, CaracterInvalido) as ex:
			print("Se detecto el error: ", ex)
			return
		if parametros is not None:
			try:
				parametros.append(float(argv[2]))
			except ValueError:
				print("X0 debe ser un número")
				return
			try:
				parametros.append(float(argv[3]))
			except ValueError:
				print("X1 debe ser un número")
			try:
				parametros.append(int(argv[4]))
			except ValueError:
				print("CIFRAS_SIGNIFICATIVAS debe ser un número")
				return
		else:
			print("Error en el polinomio")
			return
	(coefi, expon, polin, variable, x0, x1, n_signif) = parametros
	if n_signif < 1:
		print("CIFRAS_SIGNIFICATIVAS debe ser mayor o igual a 1")
		return
	print("Aplicando metodos a", polin, "a partir de x=", x0)
	inicio_segundos = time.time()
	inicio_procesador = time.clock()
	(raiz, iteraciones, error, puntos) = secante(coefi, expon, x0, x1, n_signif)
	tiempo_ejecucion = time.clock() - inicio_procesador
	tiempo_segundos = time.time() - inicio_segundos
	print("Resultados:")
	print("Secante")
	print("Raiz encontrada en", variable, "=", raiz)
	print("Iteraciones: ", iteraciones)
	print("Error: ", error)
	print("Tiempo transcurrido :", tiempo_segundos, "segundos")
	print("Tiempo de procesador:", tiempo_ejecucion, "segundos")
	inicio_segundos = time.time()
	inicio_procesador = time.clock()
	(raiz, iteraciones, error, puntos) = newton_raphson(coefi, expon, x0, n_signif)
	tiempo_ejecucion = time.clock() - inicio_procesador
	tiempo_segundos = time.time() - inicio_segundos
	print("================================================")
	print("Resultados:")
	print("Newton-Raphson")
	print("Raiz encontrada en", variable, "=", raiz)
	print("Iteraciones: ", iteraciones)
	print("Error: ", error)
	print("Tiempo transcurrido :", tiempo_segundos, "segundos")
	print("Tiempo de procesador:", tiempo_ejecucion, "segundos")
	input("presione enter para graficar los metodos")
	graficar_secante(coefi, expon, x0, x1, raiz, puntos)
	graficar_newton(coefi, expon, x0, raiz, puntos)

if __name__ == '__main__':
	try:
		main(sys.argv)
	except KeyboardInterrupt:
		print("Cancelando operación")
