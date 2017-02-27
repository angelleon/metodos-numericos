#!/bin/env python3
# -*- coding: utf8 -*-

"""
newton-raphson.py

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
from utilidades import *


def newton_raphson(coeficientes, exponentes, x0, n_signif):
	print("funcion newton_raphson")
	tolerancia = 0.05 * 10 ** (2 - n_signif)
	error = tolerancia * 2
	cont = 0
	while abs(error) > tolerancia:
		fx0 = evaluar_poly(x0, coeficientes, exponentes)
		(coef_deriv, exp_deriv) = derivar_poly(coeficientes, exponentes)
		dfx0 = evaluar_poly(x0, coef_deriv, exp_deriv)
		xi = x0 - (fx0/dfx0)
		error = (xi - x0) * 100.0/xi
		x0 = xi
		cont += 1
	return [xi, cont, error]



def modo_interactivo():
	print("Buscando raiz con el metodo de Newton-Raphson")
	return introducir_parametros()


def imprimir_ayuda():
	texto_ayuda = \
		"""Uso:
			Interactivo:
			newton-raphson.py

			No interactivo:
			newton-raphson.py POLINOMIO X0 CIFRAS-SIGNIFICATIVAS

			Mostrar este texto de ayuda:
			newton-raphson.py [ -h | --help ]"""
	print(texto_ayuda)


def main(argv):
	if len(argv) == 1:
		parametros = modo_interactivo()
	elif len(argv) == 2 and (argv[1] == "-h" or argv[1] == "--help"):
		imprimir_ayuda()
	elif len(argv) != 4:
		print("El programa recible 4 argumentos, %d dados" % (len(argv) - 1))
		imprimir_ayuda()
		return
	elif len(argv) == 4:
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
				parametros.append(int(argv[3]))
			except ValueError:
				print("CIFRAS_SIGNIFICATIVAS debe ser un número")
				return
		else:
			print("Error en el polinomio")
			return
	# except ()
	# except (ErrorCoeficiente, ErrorEntrada, CaracterInvalido, FuncionMultivariable):
	# 	raise
	coeficientes = parametros[0]
	exponentes = parametros[1]
	polinomio = parametros[2]
	variable = parametros[3]
	x0 = parametros[4]
	# xf = parametros[5]
	n_signif = parametros[5]
	if n_signif < 1:
		print("CIFRAS_SIGNIFICATIVAS debe ser mayor o igual a 1")
		return
	print("Aplicando Newton-Raphson a", polinomio, "a partir de x=", x0)
	inicio_segundos = time.time()
	inicio_procesador = time.clock()
	(raiz, iteraciones, error) = newton_raphson(coeficientes, exponentes, x0, n_signif)
	# resultados = bisectar(coeficientes, exponentes, x0, xf, n_signif)
	tiempo_ejecucion = time.clock() - inicio_procesador
	tiempo_segundos = time.time() - inicio_segundos
	# raiz = resultados[0]
	# iteraciones = resultados[1]
	# error = resultados[2]
	print("Resultados:")
	print("Raiz encontrada en", variable, "=", raiz)
	print("Iteraciones: ", iteraciones)
	print("Error: ", error)
	print("Tiempo transcurrido :", tiempo_segundos, "segundos")
	print("Tiempo de procesador:", tiempo_ejecucion, "segundos")
	input("presione enter para graficar la función")
	# graficar_poly(coeficientes, exponentes, x0, xf, raiz)


if __name__ == '__main__':
	main(sys.argv)
