#!/usr/bin/python3

"""
fracciones.py

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


def factores_primos(a):  # funcion no usada :( , poco eficiente
	primos = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
	factores = []
	cont = 0
	while a > 1:
		print(cont, len(primos))
		if cont == len(primos):
			factores.append(a)
			break
		if a % primos[cont] == 0:
			factores.append(primos[cont])
			a /= primos[cont]
			continue
		cont += 1
	return factores


def mcm(a, b):
	"""print("funcion mcm")
	print("a", type(a), a)
	print("b", type(b), b)"""
	return a * b // mcd(a, b)  # mas economico que descomponer en factores primos


def mcd(a, b):  # algoritmo de Euclides para encontrar el mcd
	"""print("funcion mcd")
	print("a", type(a), a)
	print("b", type(b), b)"""
	if a < 0 and b < 0:
		a = abs(a)
		b = abs(b)
	if a < 0:
		a *= -1
	if b < 0:
		b *= -1
	if a == 0 and b != 0:
		return b
	elif b == 0 and a != 0:
		return a
	elif a == 0 and b == 0:
		return 1
	while a != b:
		if a > b:
			a -= b
		elif a < b:
			b -= a
	return a


class Fraccion:
	def __init__(self, numerador, denominador=1):
		if denominador < 0:
			numerador *= -1
			denominador = abs(denominador)
		divisor = mcd(numerador, denominador)  # reducir fraccion antes de asignar los atributos
		numerador //= divisor
		denominador //= divisor
		if denominador == 0:
			numerador = 0
			denominador = 1
		self.numerador = numerador
		self.denominador = denominador

	def __str__(self):
		if self.denominador == 1:
			return str(self.numerador)
		return str(self.numerador) + "/" + str(self.denominador)

	def __repr__(self):
		return str(self)

	def __add__(self, other):

		if isinstance(other, int):
			other = Fraccion(other)
		if other.denominador == self.denominador:
			return Fraccion(self.numerador + other.numerador, self.denominador)
		else:
			d = mcm(self.denominador, other.denominador)
			return Fraccion((d // self.denominador * self.numerador) + (d // other.denominador * other.numerador), d)

	def __sub__(self, other):
		if isinstance(other, int):
			other = Fraccion(other)
		if other.denominador == self.denominador:
			return Fraccion(self.numerador - other.numerador, self.denominador)
		else:
			d = mcm(self.denominador, other.denominador)
			return Fraccion((d // self.denominador * self.numerador) - (d // other.denominador * other.numerador), d)

	def __mul__(self, other):
		if isinstance(other, int):
			other = Fraccion(other)
		elif isinstance(other, float):
			other = Fraccion(other)
		return Fraccion(self.numerador * other.numerador, self.denominador * other.denominador)

	def __lt__(self, other):
		if isinstance(other, int):
			other = Fraccion(other)
		divisor = mcd(self.denominador, other.denominador)
		if self.numerador//divisor < other.numerador//divisor:
			return True
		else:
			return False

	def __iadd__(self, other):
		return self.__add__(other)

	def __gt__(self, other):
		if isinstance(other, int):
			other = Fraccion(other)
		divisor = mcd(self.denominador, other.denominador)
		if self.numerador//divisor > other.numerador//divisor:
			return True
		else:
			return False

	def __eq__(self, other):
		if isinstance(other, int):
			other = Fraccion(other)
		divisor = mcd(self.denominador, other.denominador)
		if self.numerador // divisor == other.numerador // divisor:
			return True
		else:
			return False

	def reciproco(self):
		if self.numerador == 0:
			return Fraccion(0)
		return Fraccion(self.denominador, self.numerador)

if __name__ == '__main__':
	print("Modulo que define la clase fracciones. Este archivo por si mismo no hace nada")
