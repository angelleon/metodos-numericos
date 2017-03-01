#!/bin/env python3
# -*- coding: utf8 -*-

"""
biseccion.py

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

from utilidades import *
import sys
import time


def bisectar(coeficientes, exponentes, x0, xf, n_signif):
	tolerancia = 0.05 * 10 ** (2 - n_signif)
	error = tolerancia * 2  # asegurar que la condicion del ciclo se cumple
	cont = 0
	xm = (x0 + xf) / float(2)
	# ToDo: si la raiz se encuentra en la primera iteración se obtine un valor del error incorrecto
	xm_anterior = xm * 2  # se obtiene el primer valor del error = 1
	while abs(error) > tolerancia:
		if xm == 0:
			xm += abs(x0 - xf) / 100.0
		if evaluar_poly(xm, coeficientes, exponentes) == 0:
			break
		elif evaluar_poly(x0, coeficientes, exponentes) * evaluar_poly(xm, coeficientes, exponentes) < 0:
			xf = xm
		elif evaluar_poly(xm, coeficientes, exponentes) * evaluar_poly(xf, coeficientes, exponentes) < 0:
			x0 = xm
		error = (xm - xm_anterior) * 100.0 / xm
		xm_anterior = xm
		xm = (x0 + xf) / 2.0
		cont += 1
	return [xm, cont, error]


def imprimir_ayuda():
	texto_ayuda =\
"""Uso:
	Interactivo:
	bisectar.py

	No interactivo:
	bisectar.py POLINOMIO X0 Xf CIFRAS-SIGNIFICATIVAS

	Mostrar este texto de ayuda:
	bisectar.py [ -h | --help ]"""
	print(texto_ayuda)


def main(argv):
	if len(argv) == 1:
		parametros = introducir_parametros()
	elif len(argv) == 2 and (argv[1] == "-h" or argv[1] == "--help"):
		imprimir_ayuda()
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
				print("Xf debe ser un número")
				return
			try:
				parametros.append(int(argv[4]))
			except ValueError:
				print("CIFRAS_SIGNIFICATIVAS debe ser un número")
				return
		else:
			print("Error en el polinomio")
			return
	(coefi, expon, polin, variable, x0, xf, n_signif) = parametros  # desempaquetando los parametros
	if n_signif < 1:
		print("CIFRAS_SIGNIFICATIVAS debe ser mayor o igual a 1")
		return
	# ToDo: redundante en modo interactivo
	if analizar_intervalo(x0, xf):
		(x0, xf) = analizar_intervalo(x0, xf)
	else:
		print("x0 y xf no pueden ser iguales")
		return
	intervalo = probar_intervalo(coefi, expon, x0, xf)
	if not intervalo:
		print("No se enconró una raíz en el intervalo. Intente con un intervalo diferente")
		return
	elif intervalo[0] != x0 or intervalo[1] != xf:
		print("Hay dos raices en el intervalo.\nUsando subintervalo [" + intervalo[0] + ',' + intervalo[1] + ']')
		if intervalo[0] != x0:
			x0 = intervalo[0]
		elif intervalo[1] != xf:
			xf = intervalo[1]
	print("Bisectando ", polin, " en el intervalo [", x0, ',', xf, ']')
	inicio_segundos = time.time()
	inicio_procesador = time.clock()
	(raiz, iteraciones, error) = bisectar(coefi, expon, x0, xf, n_signif)
	tiempo_ejecucion = time.clock() - inicio_procesador
	tiempo_segundos = time.time() - inicio_segundos
	print("Resultados:")
	print("Raiz encontrada en", variable, "=", raiz)
	print("Iteraciones: ", iteraciones)
	print("Error: ", error)
	print("Tiempo transcurrido :", tiempo_segundos, "segundos")
	print("Tiempo de procesador:", tiempo_ejecucion, "segundos")
	input("presione enter para graficar la función")
	graficar_poly(coefi, expon, x0, xf, raiz)


if __name__ == '__main__':
	try:
		main(sys.argv)
	except KeyboardInterrupt:
		print("Operación cancelada")
