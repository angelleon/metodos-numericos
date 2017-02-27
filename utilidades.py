#!/bin/env python3
# -*- coding: utf8 -*-

"""
utilidades.py

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

# import sys
import re
# import time
import numpy as np
import matplotlib.pyplot as plt
# import numpy.polynomial.polynomial


def graficar_poly(coeficientes, exponentes, x0, xf, raiz):
	if abs(x0 - raiz) < abs(raiz - xf):
		xf = raiz + abs(x0 - raiz)
	else:
		x0 = raiz - abs(raiz - xf)
	x_vals = np.linspace(x0, xf, 51)  # abs(xf - x0)/50.0)
	y_vals = [evaluar_poly(x, coeficientes, exponentes) for x in x_vals]
	plt.axhline(0, color='black')
	plt.axvline(0, color='black')
	plt.grid(True)
	plt.plot(x_vals, y_vals)
	print(raiz)
	plt.plot([raiz], [0.0], 'ro')
	plt.show()
	"""fig, ax = plt.subplots()
	# ax.plot(x_vals, evaluar_poly(x_vals, coeficientes, exponentes))
	# ax.plot(x_vals, y_vals)
	# ax.set_aspect('equal')
	ax.grid(True, which='both')
	plt.plot(x_vals, y_vals)
	plt.show()

	ax.axhline(y=0, color='k')
	ax.axvline(x=0, color='k')"""
	"""plt.plot(x_vals, y_vals, 'r')
	plt.plot([raiz], [0], 'o')
	plt.show()"""


# todo declarar funcion analizar fracciones
def convertir_fracciones():
	motor = re.compile("[-+]?[0-9]|[-+]?[0-9]?\.[0-9]+")


def derivar_poly(coeficientes, exponentes):
	deriv_coeficientes = []
	deriv_exponentes = []
	for i in range(len(coeficientes)):
		if exponentes[i] != 0:
			deriv_coeficientes.append(coeficientes[i] * exponentes[i])
			deriv_exponentes.append(exponentes[i] - 1)
	return [deriv_coeficientes, deriv_exponentes]


class Numero(enumerate):
	flotante = 1
	entero = 2


class FuncionTipo(enumerate):
	constante = 0
	polinomial = 1
	trigonometrica = 2
	exponencial = 3
	logaritmica = 4


class Funcion(object):
	def __init__(self, tipo, subtipo=0):
		self.tipo = tipo
		self.subtipo = subtipo
		self.terminos = []

	def __str__(self):
		return str([termino for termino in self.terminos])

	def derivar(self):
		pass


class Polinomio(Funcion):
	def derivar(self):
		pass

class ErrorEntrada(Exception):
	pass


class ErrorCoeficiente(ErrorEntrada):
	pass


class FuncionConstante(ErrorEntrada):
	def __str__(self):
		return "función constante"


class CaracterInvalido(ErrorEntrada):
	def __str__(self):
		return "caracter invalido"


class FuncionMultivariable(ErrorEntrada):
	def __str__(self):
		return "función multivariable"


def convertir_a_numero(raw_numero):
	pass


def convertir_fraccion(fraccion):
	print("funcion convertir fracciones")
	motor = re.compile("[-+]?[0-9]+|[-+]?[0-9]\.[0-9]+")
	numerador = motor.search(fraccion)
	fraccion = fraccion[:numerador.start()] + fraccion[numerador.end():]
	numerador = float(numerador.group())
	denominador = motor.search(fraccion)
	denominador = float(denominador.group())
	return numerador/denominador


def evaluar_poly(x, coeficientes, exponentes):
	# print("funcion evaluar_poly")
	# print(x, coeficientes, exponentes)
	imagen = 0
	for i in range(0, len(coeficientes)):
		imagen += coeficientes[i] * x ** exponentes[i]
	return imagen


def introducir_poly():
	while True:
		raw_poly = input("""Introduzca el polinomio en la forma:
		anx^n + ... + a2x^2 + a1x + a0\npolinomio: """)
		try:
			return analizar_poly(raw_poly)
		except ErrorEntrada:
			continue


def introducir_extremos():
	while True:
		try:
			x0 = float(input("Introduzca el extremo izquierdo del intervalo\nx0: "))
		except ValueError:
			print("introduzca un valor numerico")
			continue
		break
	while True:
		try:
			xf = float(input("Introduzca el extremo derecho del intervalo\nxf: "))
		except ValueError:
			continue
		if xf == x0:
			print("x0 y xf deben ser diferentes")
			continue
		break
	return [x0, xf]


def introducir_n_confianza():
	while True:
		try:
			n = int(input("Introduzca la cantidad de cifras de confianza\nn: "))
		except ValueError:
			print("Introduzaca un valor numerico")
			continue
		if n < 1:
			print("El valor de n debe ser un entero positivo")
			continue
		break
	return n


def introducir_parametros():
	print("funcion introducir_poly")
	polinomio = introducir_poly()
	intervalo = introducir_intervalo()
	n_confianza = introducir_n_confianza()
	return [polinomio[0], polinomio[1], polinomio[2], polinomio[3], intervalo[0], intervalo[1], n_confianza]


def introducir_intervalo():
	while True:
		while True:
			try:
				x0 = float(input("Introduzca el extremo izquierdo del intervalo"))
			except ValueError:
				print("Introduzca un valor numerico")
				continue
			break
		while True:
			try:
				xf = float(input("Introduzca el extremo derecho del intervalo"))
			except ValueError:
				print("Introduzca un valor numerico")
				continue
			break
		intervalo = analizar_intervalo(x0, xf)
		if intervalo:
			break
	return intervalo
# TODO llamar a analizar fracciones


def analizar_intervalo(x0, xf):
	if x0 == xf:
		return False
	if x0 > xf:
		return [xf, x0]
	return [x0, xf]


def introducir_poly_dummy():
	pass


def buscr_carac_invalidos(raw_poly):
	motor = re.compile("[^a-z0-9-+^./]")
	if motor.search(raw_poly) is not None:
		mostrar_error(motor.search(raw_poly).group(), raw_poly)
		raise CaracterInvalido


def obtener_terminos_x(raw_poly):
	terminos = []
	termino = ''
	motor = re.compile("([+-]?([0-9]*|[0-9]*\.[0-9]+)[a-z](\^[0-9])?)")
	while termino is not None:
		termino = motor.search(raw_poly)
		if termino is not None:
			terminos.append(termino.group())
		else:
			break
		raw_poly = raw_poly[0:termino.start()] + raw_poly[termino.end():]
	return [terminos, raw_poly]


def reducir_terminos_lineales(terminos):
	termino_lineal = 0
	for i in terminos:
		i = float(i)
		termino_lineal += i
	return str(termino_lineal)


def obtener_terminos_lineales(raw_poly):
	print("funcion obtener_terminos_lineales")
	print(raw_poly)

	motor = re.compile("([-+]?[0-9]+)|([-+]([0-9]*\.[0-9]+))")
	terminos = []
	termino = motor.search(raw_poly)
	while termino is not None and len(raw_poly) != 0:
		termino = motor.search(raw_poly)
		print(termino.group())
		if termino is not None:
			terminos.append(termino.group())
			break
		raw_poly = raw_poly[0:termino.start()] + raw_poly[termino.end():]
	print(terminos)
	termino = reducir_terminos_lineales(terminos)
	return termino


def obtener_terminos(raw_poly):
	print("funcion obtener_terminos")
	buscr_carac_invalidos(raw_poly)
	respuesta = obtener_terminos_x(raw_poly)
	terminos = respuesta[0]
	raw_poly = respuesta[1]
	print(terminos, raw_poly)
	terminos.append(obtener_terminos_lineales(raw_poly))
	print(terminos)
	return terminos


def mostrar_error(error, raw_poly):
	print("funcion mostrar error")
	motor = re.compile(error)
	coincidencia = motor.search(raw_poly)
	indicador = "^~~~~~"
	if coincidencia.start() != 0:
		for i in range(0, coincidencia.start()):
			indicador = ' ' + indicador
	print("\n\t" + raw_poly + '\n\t' + indicador)


def obtener_variable(terminos):
	print("funcion obtener_variable")
	print(terminos)
	motor = re.compile("[a-z]")
	variables = set()
	for i in terminos:
		print(type(i))
		coincidencia = motor.search(i)
		if coincidencia is not None:
			variables.add(coincidencia.group())
			variable = coincidencia.group()
	if len(variables) > 1:
		print("Ingrese funciones de una variable")
		raise FuncionMultivariable
	elif len(variables) == 0:
		print("El método de bisección no se puede aplicar a funciones constantes")
		return None
	return variable


def obtener_coeficientes(terminos):
	print("funcion funcion obtener_coeficientes")
	motor = re.compile("^([-+]?[0-9]*\.[0-9]+)|^([-+]?[0-9]+)|^([-+])")
	coeficientes = []
	for termino in terminos:
		print(termino)
		coincidencia = motor.search(termino)
		if coincidencia is None:
			coeficientes.append(1.0)
			continue
		coeficiente = coincidencia.group()
		print(coeficiente, coincidencia.groups())
		if coeficiente == '+' or coeficiente == '-':
			coeficiente += '1'
		coeficientes.append(float(coeficiente))
	print(coeficientes)
	return coeficientes


def obtener_exponentes(terminos):
	print("funcion obtener_exponentes")
	print(terminos)
	exponentes = []
	for termino in terminos:
		coincidencia = re.search("\^[0-9]+", termino)
		if coincidencia is not None:
			exponentes.append(int(coincidencia.group()[1:]))
			continue
		coincidencia = re.search("[a-z]", termino)
		if coincidencia is not None:
			exponentes.append(1)
		else:
			exponentes.append(0)
	print(exponentes)
	return exponentes


def buscar_duplicados(lista):
	print("funcion buscar_duplicados")
	print(lista)
	repetidos = set()
	indices = []
	for i in range(0, len(lista)):
		if i < len(lista) - 1:
			for j in range(i+1, len(lista)):
				if lista[j] == lista[i]:
					repetidos.add(lista[j])
					break
	if len(repetidos) == 0:
		return None
	cont = 0
	for i in repetidos:
		indices.append([])
		for j in range(0, len(lista)):
			if i == lista[j]:
				indices[cont].append(j)
		cont += 1
	print(indices)
	return indices


def reducir_terminos(coeficientes, exponentes):
	print("funcion reducir_terminos")
	print(coeficientes, exponentes)
	reducibles = buscar_duplicados(exponentes)
	if reducibles is None:
		return None
	indice_reducidos = []
	indice_descartados = []
	for i in reducibles:
		indice_reducidos.append(i[0])
		for j in i[1:]:
			indice_descartados.append(j)
	for i in reducibles:
		for j in i:
			if j != i[0]:
				for k in indice_reducidos:
					coeficientes[k] += coeficientes[j]
	coef_reducidos = []
	exp_reducidos = []
	for i in range(0, len(coeficientes)):
		if i not in indice_descartados:
			coef_reducidos.append(coeficientes[i])
			exp_reducidos.append(exponentes[i])
	print(coef_reducidos, exp_reducidos)
	return [coef_reducidos, exp_reducidos]


def ordenar(coeficientes, exponentes, terminos):
	print("funcion ordenar")
	print(coeficientes, exponentes, terminos)
	if exponentes == sorted(exponentes, reverse=True):
		return None
	indices = {}
	cont = 0
	for i in exponentes:
		indices[str(i)] = cont
		cont += 1
	print(exponentes)
	exponentes.sort(reverse=True)
	print(exponentes)
	coef_ordenados = []
	term_ordenados = []
	print(exponentes)
	print(indices.keys(), sorted(indices.keys()))
	print(indices)
	for clave in sorted(indices.keys()):
		print(clave, coeficientes[indices[clave]], indices[clave])
		coef_ordenados.append(int(coeficientes[indices[clave]]))
		term_ordenados.append(terminos[indices[clave]])
	print(coef_ordenados, exponentes, term_ordenados)
	return [coef_ordenados, exponentes, term_ordenados]


def analizar_poly(raw_poly):
	print("funcion analizar_poly")
	if len(raw_poly) == 0:
		print("No hay entrada")
		return
	raw_poly = raw_poly.lower()
	terminos = obtener_terminos(raw_poly)
	if isinstance(terminos, str):
		mostrar_error(terminos, raw_poly)
		return None
	elif terminos is None:
		return None
	variable = obtener_variable(terminos)
	print(variable)
	if variable is None:
		return None
	coeficientes = obtener_coeficientes(terminos)
	exponentes = obtener_exponentes(terminos)
	reduccion = reducir_terminos(coeficientes, exponentes)
	if reduccion is not None:
		coeficientes = reduccion[0]
		exponentes = reduccion[1]
	term_ord = ordenar(coeficientes, exponentes, terminos)
	if term_ord is not None:
		coeficientes = term_ord[0]
		exponentes = term_ord[1]
		terminos = term_ord[2]
	polinomio = ''
	for i in terminos:
		polinomio += str(i)
	print("polinomio: ", polinomio)
	return [coeficientes, exponentes, polinomio, variable]


def probar_intervalo(coeficientes, exponentes, x0, xf):
	print("funcion probar_intervalo")
	if evaluar_poly(x0, coeficientes, exponentes) * evaluar_poly(xf, coeficientes, exponentes) < 0:
		return [x0, xf]
	dx = abs(x0 - xf) / float(100)
	xi = x0
	for i in range(0, 100):
		print(xi, dx, x0, xf)
		if evaluar_poly(xi, coeficientes, exponentes) * evaluar_poly(xf, coeficientes, exponentes) < 0:
			if i <= 50:
				return [x0, xi]
			else:
				return [xi, xf]
		xi += dx
	return False

"""
Escribir un programa que lea un polinomio de grado n>1 e implemente el metodo de newton para aproximar una raiz
graficar el polinomio y las rectas

comparar los metodos de newton y el metodo de la secante.
el usuario introducira un polinomio al programa y este buscará la raiz con newton
dado x0 con el metodo de la secante
con el mismo x0 pidiendo x1
el programa imprimirá la cantidad de iteraciones de cada metodo y el tiempo de ejecución del metodo
la aprox de la raiz

"""
