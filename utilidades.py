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


import re  # modulo de expresiones regulares
import numpy as np
import matplotlib.pyplot as plt

"""
funciones comunes para los programas de metodos numericos
"""

# ToDo: hacer algo para centralizar el manejo de las cosas por hacer (ToDo's)
# ToDo: implementar el paradigma OO
# ToDo: lanzar excepciones, por algo están declaradas
# ToDo: reimplementar el modo interactivo en todos los programas
# ToDo: hacer funcion main más modular en todos los programas
# ToDo: mover analizador lexico a otro archivo


class Polinomio:  # no usada esta clase hasta ahora, la mayoria del programa esta hecho con el paradigma imperativo
	def __init__(self, coef=None, exp=None):
		if coef is not None:
			self.coef = coef
			self.exp = exp
		else:
			self.coef = [1, 0]
			self.exp = [1, 0]

	def evaluar(self, x):
		imagen = 0
		for i in range(len(self.coef)):
			imagen += self.coef[i] * x ** self.exp[i]
		return imagen

	def derivar(self):
		coef_deriv = []
		exp_deriv = []
		for i in range(len(self.coef)):
			if self.exp[i] > 0:
				exp_deriv.append(self.exp[i] - 1)
				coef_deriv.append(self.coef[i] * self.exp[i])
		return Polinomio(coef_deriv, exp_deriv)  # Devuelve la derivada del polinomio como objeto


def graficar_poly(coeficientes, exponentes, x0, xf, raiz, intervalo_original=None):
	if intervalo_original is not None:  # cuando se ha usado un subintervalo porque hay varias raices se grafica
		# el intervalo original para mostrar las multiples intersecciones con el eje x
		x0 = intervalo_original[0]
		xf = intervalo_original[1]
	if abs(x0 - raiz) < abs(raiz - xf): # graficar en un intervalo simetrico
		xf = raiz + abs(x0 - raiz)
	else:
		x0 = raiz - abs(raiz - xf)
	x_vals = np.linspace(x0, xf, 51)  # valores de x a graficar, 51 puntos equidistantes en el intervalo
	y_vals = [evaluar_poly(x, coeficientes, exponentes) for x in x_vals] # imagenes de los valores de x de la linea previa
	plt.axhline(0, color='black')  # ejes, por defecto no parecen
	plt.axvline(0, color='black')
	plt.grid(True)
	plt.plot(x_vals, y_vals, linewidth=1.0)
	plt.scatter([raiz], [0.0])  # graficar la raiz
	# ToDo: establecer el ratio de la rejilla
	plt.grid(True) # rejilla
	plt.plot(x_vals, y_vals) # graficar polinomio
	plt.show()


def derivar_poly(coeficientes, exponentes):  # deriva, planeado reemplazar al usar el paradigma OO
	deriv_coeficientes = []
	deriv_exponentes = []
	for i in range(len(coeficientes)):
		if exponentes[i] != 0:
			deriv_coeficientes.append(coeficientes[i] * exponentes[i])
			deriv_exponentes.append(exponentes[i] - 1)
	return [deriv_coeficientes, deriv_exponentes]


# excepciones al analizar la entrada del usuario
class ErrorEntrada(Exception):
	def __str__(self):
		return "Error en la entrada de datos"


class ErrorCoeficiente(ErrorEntrada):
	def __str__(self):
		return "Error en los coeficientes del polinomio"


class FuncionConstante(ErrorEntrada):  # lanzada si al reducir los terminos se obtien sólo constantes
	def __str__(self):
		return "función constante"


class CaracterInvalido(ErrorEntrada):
	def __str__(self):
		return "caracter invalido"


class FuncionMultivariable(ErrorEntrada):  # lanzada cuando hay varias literales, el programa usa cualquier letra
	# como variable
	def __str__(self):
		return "función multivariable"


# ToDo: terminar para poder ingresar coeficientes como fracciones
def convertir_fraccion(fraccion):
	motor = re.compile("[-+]?[0-9]+|[-+]?[0-9]\.[0-9]+")
	numerador = motor.search(fraccion)
	fraccion = fraccion[:numerador.start()] + fraccion[numerador.end():]
	numerador = float(numerador.group())
	denominador = motor.search(fraccion)
	denominador = float(denominador.group())
	return numerador/denominador


# ToDo: implementar en OO
def evaluar_poly(x, coeficientes, exponentes):  # obtener la imagen de f en el punto x, por reemplazar en paradigma OO
	imagen = 0
	for i in range(0, len(coeficientes)):
		imagen += coeficientes[i] * x ** exponentes[i]
	return imagen


def introducir_poly():  # para modo interactivo
	while True:
		raw_poly = input("""Introduzca el polinomio en la forma:
		anx^n + ... + a2x^2 + a1x + a0\npolinomio: """)
		try:
			return analizar_poly(raw_poly)
		except ErrorEntrada:
			print("\nIntente de nuevo")



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


# ToDo: programas diferente requieren parametros diferentes
# hacer uno por programa o <inserte solución aquí> :/
def introducir_parametros():  # para el modo interactivo
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
# ToDo: llamar a analizar fracciones


def analizar_intervalo(x0, xf):
	if x0 == xf:
		return False
	if x0 > xf:
		return [xf, x0]
	return [x0, xf]


def introducir_poly_dummy():
	pass


def buscr_carac_invalidos(raw_poly):  # busca errores de tipeo
	motor = re.compile("[^a-z0-9-+^./]")
	if motor.search(raw_poly) is not None:
		mostrar_error(motor.search(raw_poly).group(), raw_poly)
		raise CaracterInvalido  # lanzar la excepcion en caso de que algo en el string no se pueda interprtetar
	# correctamente


def obtener_terminos_x(raw_poly):
	terminos = []
	termino = ''
	motor = re.compile("([+-]?([0-9]*|[0-9]*\.[0-9]+)[a-z](\^[0-9])?)")
	while termino is not None:
		termino = motor.search(raw_poly)
		if termino is not None:
			terminos.append(termino.group())  # guarda el termino encontrado en la lista
		else:
			break
		raw_poly = raw_poly[0:termino.start()] + raw_poly[termino.end():]  # elimina la coincidencia encontrada de la
	#  cadena para la siguiente iteracion
	return [terminos, raw_poly]


def reducir_terminos_lineales(terminos):
	termino_lineal = 0
	for i in terminos:
		i = float(i)
		termino_lineal += i
	return str(termino_lineal)


def obtener_terminos_lineales(raw_poly):
	motor = re.compile("([-+]?[0-9]+)|([-+]([0-9]*\.[0-9]+))")
	terminos = []
	termino = motor.search(raw_poly)
	while termino is not None and len(raw_poly) != 0:
		termino = motor.search(raw_poly)
		if termino is not None:
			terminos.append(termino.group())
			break
		raw_poly = raw_poly[0:termino.start()] + raw_poly[termino.end():]  # elimina la coincidencia de la cadena de
	# entrada para la siguiente iteraccion
	termino = reducir_terminos_lineales(terminos)
	return termino


def obtener_terminos(raw_poly):
	buscr_carac_invalidos(raw_poly)
	respuesta = obtener_terminos_x(raw_poly)
	terminos = respuesta[0]
	raw_poly = respuesta[1]
	terminos.append(obtener_terminos_lineales(raw_poly))
	return terminos


def mostrar_error(error, raw_poly):  # muestra la parte de la cadena de entrada que no se reconoce
	motor = re.compile(error)
	coincidencia = motor.search(raw_poly)
	indicador = "^~~~~~"
	if coincidencia.start() != 0:
		for i in range(0, coincidencia.start()):
			indicador = ' ' + indicador
	print("\n\t" + raw_poly + '\n\t' + indicador)


def obtener_variable(terminos):  # busca la variable, comunmente x, que se usa en el polinomio, en caso de encontrar 
	# más de un caracter en el rango a-z se considera una funcion multivariable, posiblemente por erro de tipeo
	motor = re.compile("[a-z]")
	variables = set()
	for i in terminos:
		coincidencia = motor.search(i)
		if coincidencia is not None:
			variables.add(coincidencia.group())
			variable = coincidencia.group()
	if len(variables) > 1:
		print("Ingrese funciones de una variable")
		raise FuncionMultivariable
	elif len(variables) == 0:  # comprueba que haya al menos un termino con una variable
		print("El método no se puede aplicar a funciones constantes")
		raise FuncionConstante
	return variable


def obtener_coeficientes(terminos):
	motor = re.compile("^([-+]?[0-9]*\.[0-9]+)|^([-+]?[0-9]+)|^([-+])")
	coeficientes = []
	for termino in terminos:
		coincidencia = motor.search(termino)
		if coincidencia is None:
			coeficientes.append(1.0)
			continue
		coeficiente = coincidencia.group()
		if coeficiente == '+' or coeficiente == '-':
			coeficiente += '1'
		coeficientes.append(float(coeficiente))
	return coeficientes


def obtener_exponentes(terminos):
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
	return exponentes


def buscar_duplicados(lista):  # busca elementos duplicados en una lista, se usa para reducir los terminos con el
	# mismo exponente en x
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
	return indices


def reducir_terminos(coeficientes, exponentes):  # reduce terminos con el mismo exponente
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
	return [coef_reducidos, exp_reducidos]


def ordenar(coeficientes, exponentes, terminos):  # ordena linstas paralelas, los elementos de una lista se ordenan y
	#  los correspondientes (segun su indice) de la otra lista se ordenan con el elemento correspondiente de la
	# primera lista
	if exponentes == sorted(exponentes, reverse=True):
		return None
	indices = {}
	cont = 0
	for i in exponentes:
		indices[str(i)] = cont
		cont += 1
	exponentes.sort(reverse=True)
	coef_ordenados = []
	term_ordenados = []
	for clave in sorted(indices.keys()):
		coef_ordenados.append(int(coeficientes[indices[clave]]))
		term_ordenados.append(terminos[indices[clave]])
	return [coef_ordenados, exponentes, term_ordenados]


# ToDo: lanzar excepciones en vez de retornar None
def analizar_poly(raw_poly):
	if len(raw_poly) == 0:
		print("No hay entrada")
		raise ErrorEntrada
	raw_poly = raw_poly.lower()
	terminos = obtener_terminos(raw_poly)
	if isinstance(terminos, str):
		mostrar_error(terminos, raw_poly)
		return None
	elif terminos is None:
		return None
	variable = obtener_variable(terminos)
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


def probar_intervalo(coeficientes, exponentes, x0, xf):  # busca si en el intervalo hay raices para evitar usar el
	# metodo en caso de que no
	if evaluar_poly(x0, coeficientes, exponentes) * evaluar_poly(xf, coeficientes, exponentes) < 0:
		return [x0, xf]
	dx = abs(x0 - xf) / float(100)
	xi = x0
	for i in range(100):
		if evaluar_poly(xi, coeficientes, exponentes) * evaluar_poly(xf, coeficientes, exponentes) < 0:
			if i <= 50:  # devuelve el intervalo más corto
				return [x0, xi]
			else:
				return [xi, xf]
		xi += dx
	return False

if __name__ == '__main__':
	print("Funciones comunes para metodos numericos\nEste archivo no hace nada por si mismo, importe para usar las "
	      "funciones declaradas aqui en otros programas")

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
