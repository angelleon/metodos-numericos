#!/usr/bin/python3
# -*- coding: utf8 -*-

# modulo aún no implementado en los programas

"""
funciones.py

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
from enum import Enum
from math import e


class TipoFuncion(Enum):
	funcion = -1
	constante = 0
	identidad = 1
	potencia = 2
	triginometrica = 3
	trigonometrica_inversa = 4
	exponencial = 5
	logaritmica = 6
	suma = 7
	producto = 8
	cociente = 9
	composicion = 10
	valor_absoluto = 11


class Funcion(object):
	tipo = TipoFuncion.funcion

	def __init__(self, variable='x'):
		self.variable = variable
		self.valor = None

	def __str__(self):
		return "prototipo de funcion vacia"

	def __add__(self, other):
		pass

	def __sub__(self, other):
		pass

	def __mul__(self, other):
		pass

	def __pow__(self, power, modulo=None):
		pass

	def evaluar(self):
		pass

	def derivar(self):
		pass

	def integrar(self):
		pass


class FuncionConstante(Funcion):
	tipo = TipoFuncion.constante

	def __init__(self, valor):
		super().__init__('')
		try:
			self.valor = float(valor)
		except ValueError:
			print("Recibido objeto:", type(valor))
			raise

	def __str__(self):
		return str(self.valor)

	def __add__(self, other):
		return self.valor + other.valor

	def evaluar(self):
		return self.valor

	def derivar(self):
		return FuncionConstante(0)

	def integrar(self):
		return Potencia(FuncionConstante(1), Identidad('x'))


class Identidad(Funcion):
	tipo = TipoFuncion.identidad

	def __init__(self, variable='x'):
		super().__init__()
		self.variable = variable
		self.valor = variable

	def __str__(self):
		return str(self.variable)

	def __add__(self, other):
		return self.valor + other.valor

	def derivar(self):
		return FuncionConstante(1)


class Potencia(Funcion):
	tipo = TipoFuncion.potencia

	def __init__(self, coeficiente=FuncionConstante(1), variable=Identidad('x'), exponente=FuncionConstante(1)):
		super().__init__()
		self.tipo = TipoFuncion.potencia
		self.coeficiente = coeficiente
		self.exponente = exponente
		self.valor = coeficiente * variable ** exponente

	def __str__(self):
		return str(self.coeficiente) + "x^" + str(self.exponente)


class Polinomio(Funcion):
	def __init__(self, coeficientes=(1, 0), exponentes=(1, 0)):
		super().__init__()
		self.tipo = TipoFuncion.suma
		self.terminos = []
		for i in range(len(exponentes)):
			self.terminos.append(Potencia(coeficientes[i], exponentes[i]))


class Exponencial(Funcion):
	tipo = TipoFuncion.exponencial

	def __init__(self, base=e, exponente=Identidad('x')):
		super().__init__()


class Logaritmica(Funcion):
	tipo = TipoFuncion.logaritmica


class Trigonometrica(Funcion):
	tipo = TipoFuncion.triginometrica


class Seno(Trigonometrica):
	pass


def obtener_tokens(raw_func):
	return False


def clasificar_tokens(tokens):
	return False


def analizador_func(raw_func):
	tokens = obtener_tokens(raw_func)
	tokens = clasificar_tokens(tokens)
