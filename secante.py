#!/usr/bin/python3
# -*- coding: utf8 -*-

# Se recomienda no usar el modo interactivo de los programas porque no
# ha sido probado completamente, en lugar de eso se recomienda usar el modo
# no interactivo desde consola
# probado en Python 3.6 (3.6.0 [GCC 6.3.1 20170109]) sobre Linux 4.4

"""
secante.py

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

from polinomios import *
import sys
import time

try:
	import numpy as np
	import matplotlib.pyplot as plt


	def graficar_secante(coefi, expon, x0, xf, raiz, puntos):
		xmin = 0
		xmax = 0
		for i in range(len(puntos[0])):  # obtener los valores maximo y minimo de x que se usaron en el metodo
			# para que ninguna linea o punto quede fuera de la grafica
			xmaxi = max(puntos[0][i])
			xmini = min(puntos[0][i])
			if xmaxi > xmax:
				xmax = xmaxi
			if xmini < xmin:
				xmin = xmini
			plt.plot(puntos[0][i], puntos[1][i], linewidth=0.7)
		x_vals = np.linspace(float(xmin), float(xmax), 51)
		y_vals = [evaluar_poly(x, coefi, expon) for x in x_vals]
		plt.axhline(0, color='black')
		plt.axvline(0, color='black')
		plt.plot(x_vals, y_vals)
		plt.scatter(raiz, 0.0, marker=".")
		plt.gca().set_aspect('equal', 'datalim')
		plt.show()

except ImportError:
	plt = None
	np = None

	def graficar_secante(coefi, expon, x0, xf, raiz, puntos):
		print("Los modulos necesarios para graficar no se han encontrado.\nInstale NumPy y Matplotlib e intentelo de "
		      "nuevo")


def secante(coefi, expon, x0, x1, n_signif):
	tolerancia = 0.05 * 10 ** (2 - n_signif)
	error = tolerancia * 2
	cont = 0
	puntos = [[], []]
	x2 = x1
	x1 = x0
	while abs(error) > tolerancia:
		x0 = x1
		x1 = x2
		fx0 = evaluar_poly(x0, coefi, expon)
		fx1 = evaluar_poly(x1, coefi, expon)
		x2 = x0 - fx0 / ((fx1 - fx0) / (x1 - x0))
		puntos[0].append([x0, x1, x2])
		puntos[1].append([fx0, fx1, 0.0])
		error = (x2 - x1) * 100/x2
		cont += 1
		if cont == 1001:
			raise MaxIteraciones
	return [x2, cont, error, puntos]


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
	print(texto_ayuda)


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
	print("Aplicando Newton-Raphson a", polin, "a partir de x=", x0)
	try:
		inicio_segundos = time.time()
		inicio_procesador = time.clock()
		(raiz, iteraciones, error, puntos) = secante(coefi, expon, x0, x1, n_signif)
		tiempo_ejecucion = time.clock() - inicio_procesador
		tiempo_segundos = time.time() - inicio_segundos
	except MaxIteraciones as ex:
		print(ex)
		return
	print("Resultados:")
	print("Raiz encontrada en", variable, "=", raiz)
	print("Iteraciones: ", iteraciones)
	print("Error: ", error)
	print("Tiempo transcurrido :", tiempo_segundos, "segundos")
	print("Tiempo de procesador:", tiempo_ejecucion, "segundos")
	input("presione enter para graficar la función")
	graficar_secante(coefi, expon, x0, x1, raiz, puntos)

if __name__ == '__main__':
	try:
		main(sys.argv)
	except KeyboardInterrupt:
		print("Cancelando operación")
