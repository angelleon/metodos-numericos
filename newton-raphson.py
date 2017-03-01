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

# ToDo implementar paradigma OO


def graficar_newton(coeficiente, exponentes, x0, raiz, puntos):
	if raiz < x0:
		x0 = raiz - abs(x0 - raiz)
		xf = raiz + abs(x0 - raiz)
	elif raiz > x0:
		xf = raiz + abs(x0 - raiz)
	else:
		raise ErrorEntrada
	x_vals = np.linspace(x0, xf, 51)
	y_vals = [evaluar_poly(x, coeficiente, exponentes) for x in x_vals]
	plt.axhline(0, color='black')
	plt.axvline(0, color='black')
	plt.grid(True)
	plt.plot(x_vals, y_vals)
	plt.scatter([raiz], [0.0])
	print(puntos)
	for i in range(len(puntos[0])):
		plt.scatter(puntos[0][i][0], puntos[1][i][0])
		plt.plot(puntos[0][i], puntos[1][i], linewidth=0.5)
	plt.show()


def newton_raphson(coeficientes, exponentes, x0, n_signif):
	print("funcion newton_raphson")
	tolerancia = 0.05 * 10 ** (2 - n_signif)
	error = tolerancia * 2
	cont = 0
	puntos = [[], []]
	while abs(error) > tolerancia:
		fx0 = evaluar_poly(x0, coeficientes, exponentes)
		(coef_deriv, exp_deriv) = derivar_poly(coeficientes, exponentes)
		dfx0 = evaluar_poly(x0, coef_deriv, exp_deriv)
		xi = x0 - (fx0/dfx0)
		puntos[0].append([x0, xi])
		puntos[1].append([fx0, 0])
		error = (xi - x0) * 100.0/xi
		x0 = xi
		cont += 1
	return [xi, cont, error, puntos]


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
	(coefi, expon, polin, variable, x0, n_signif) = parametros
	if n_signif < 1:
		print("CIFRAS_SIGNIFICATIVAS debe ser mayor o igual a 1")
		return
	print("Aplicando Newton-Raphson a", polin, "a partir de x=", x0)
	inicio_segundos = time.time()
	inicio_procesador = time.clock()
	(raiz, iteraciones, error, puntos) = newton_raphson(coefi, expon, x0, n_signif)
	tiempo_ejecucion = time.clock() - inicio_procesador
	tiempo_segundos = time.time() - inicio_segundos
	print("Resultados:")
	print("Raiz encontrada en", variable, "=", raiz)
	print("Iteraciones: ", iteraciones)
	print("Error: ", error)
	print("Tiempo transcurrido :", tiempo_segundos, "segundos")
	print("Tiempo de procesador:", tiempo_ejecucion, "segundos")
	input("presione enter para graficar la función")
	graficar_newton(coefi, expon, x0, raiz, puntos)


if __name__ == '__main__':
	try:
		main(sys.argv)
	except KeyboardInterrupt:
		print("Operación cancelada")
