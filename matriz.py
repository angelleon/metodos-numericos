#!/usr/bin/python3
# -*- coding: utf8 -*-


from fracciones import *


class MatrizNoRectangular(Exception):
	def __str__(self):
		return str(self.args[0]) + " elementos en renglón " + str(self.args[1])


class SumaNoDefinida(Exception):
	pass


class Renglon:
	def __init__(self, elementos=None, nombre="1"):
		self.elmnts = []
		if elementos is not None:
			for i in elementos:
				self.elmnts.append(i)
		self.ceros = 0
		self.pivote = self.elmnts[0]
		self.contar_ceros_izq()
		self.n = len(self.elmnts)
		self.buscar_pivote()
		self.nombre = "R" + str(nombre)

	def __str__(self):
		cadena = ""
		for i in self.elmnts:
			cadena += "\t" + str(i) + "\t"
		return cadena

	def __repr__(self):
		return str(self)

	def __getitem__(self, item):
		return self.elmnts[item]

	def __add__(self, other):
		print("Metodo sum reng")
		if other.n != self.n:
			raise SumaNoDefinida
		elmnts = []
		for i in range(self.n):
			elmnts.append(self.elmnts[i] + other.elmnts[i])
		self.buscar_pivote()
		return Renglon(elmnts)

	def __sub__(self, other):
		print("metodo rest reng")
		if other.n != self.n:
			raise SumaNoDefinida
		elmnts = []
		for i in range(self.n):
			elmnts.append(self.elmnts[i] - other.elmnts[i])
		self.buscar_pivote()
		return Renglon(elmnts)

	def __mul__(self, other):
		print("Metodo mult reng")
		if type(other) == int or type(other) == Fraccion:
			elmnts = []
			for i in self.elmnts:
				elmnts.append(i * other)
			self.buscar_pivote()
			return Renglon(elmnts)
		if type(other) == Renglon:
			print("multiplicacion de objetos renglon")
			raise Exception

	def buscar_pivote(self):
		self.contar_ceros_izq()
		self.pivote = self.elmnts[self.ceros]

	def contar_ceros_izq(self):
		cont = 0
		for i in self.elmnts:
			if i == 0:
				cont += 1
			else:
				break
		self.ceros = cont

	def recip_pivote(self):
		return self.pivote.reciproco()


class Matriz:
	def __init__(self, renglones):
		print("Matriz()")
		print(renglones)
		self.m = len(renglones)
		maxi = len(renglones[0])
		for i in range(self.m):
			if maxi != len(renglones[i]):
				raise MatrizNoRectangular(len(renglones[i]), i+1)
		self.n = maxi
		if self.m == self.n:
			self.cuadrada = True
		else:
			self.cuadrada = False
		self.renglones = []
		cont = 1
		print(self.m)
		for i in range(self.m):
			self.renglones.append(Renglon(renglones[i], str(cont)))
			cont += 1
		self.escalonada = False
		self.escal_reducida = False
		self.diag_dom = False
		self.__diag_dom()
		"""Hallar el polinomio de grado n dados sus n-1 extremos locales"""

	def __str__(self):
		cadena = ''
		for i in range(self.m):
			cadena += str(self.renglones[i])
			cadena += '\n'
		return cadena

	def __repr__(self):
		return str(self)

	def __getitem__(self, item):
		return self.renglones[item]

	def __diag_dom(self):
		if not self.cuadrada:
			self.diag_dom = False
			return
		for i in range(self.m):
			for j in range(self.n):
				"""diag dom
				si |a_ii| > sum from j=1 to n j!=i |a_ij
				"""
	def __contar_ceros(self):
		ceros = dict()
		for i in self.renglones:
			i.contar_ceros_izq()
			ceros[str(i.nombre)] = i.ceros
		return ceros

	def ordenar(self, oper=0):
		i = 1
		while i <= self.m:
			for j in range(self.m - i):
				if self.renglones[j].ceros > self.renglones[j + 1].ceros:
					oper += 1
					print("Operacion", oper)
					self.print_cambio_reng(j, j+1)
					aux_reng = self.renglones[j]
					self.renglones[j] = self.renglones[j + 1]
					self.renglones[j + 1] = aux_reng
			i += 1
		cont = 1
		for i in self.renglones:
			i.nombre = str(cont)
			cont += 1

	def reduccion_gaussiana(self, oper=0):
		if self.escalonada:
			return
		print("metodo reduccion gaussiana")
		if self.m == 1:
			self.print()
			return
		cont = -1
		while cont != 0:
			cont = 0
			for i in range(self.m):
				for j in range(self.m):
					if i == j:
						continue
					if self.renglones[i].ceros == self.renglones[j].ceros:
						oper += 1
						print("\nOperacion ", oper)
						alfa = (self.renglones[i].recip_pivote() * self.renglones[j].pivote) * -1
						self.print_suma(j, i, alfa)
						self.renglones[j] += self.renglones[i] * alfa
						cont += 1
		self.ordenar(oper)
		self.escalonada = True

	def gauss_jordan(self, oper=0):
		print("Metodo gauss_jordan")
		if self.escal_reducida:
			return
		if not self.escal_reducida:
			self.reduccion_gaussiana()
		for i in range(1, self.m):
			for j in reversed(range(i)):
				if self.renglones[j][self.renglones[i].ceros] != 0:
					oper += 1
					print("\nOperacion", oper)
					alfa = (self.renglones[i].recip_pivote() * self.renglones[j][self.renglones[i].ceros]) * -1
					self.renglones[j] += self.renglones[i] * alfa
					self.print_suma(j, i, alfa)
		self.escal_reducida = True

	def print_cambio_reng(self, a, b):
		operacion_1 = 'R%i <--> R%i' % (a+1, b+1)
		operacion_2 = 'R%i <--> R%i' % (b+1, a+1)
		for i in range(len(self.renglones)):
			if i == a:
				print(self.renglones[i], operacion_1)
			elif i == b:
				print(self.renglones[i], operacion_2)
			else:
				print(self.renglones[i])

	def print_suma(self, a, b, alfa):
		alfa = str(alfa)
		if alfa[0] != '-':
			alfa = '+' + alfa
		operacion = "R%d = R%d %sR%d" % (a+1, a+1, alfa, b+1)
		for i in range(len(self.renglones)):
			if i == a:
				print(self.renglones[i], operacion)
			else:
				print(self.renglones[i])

	def print(self):
		for i in self.renglones:
			print(i)

if __name__ == '__main__':
	print("Modulo que define las clases Matriz y Renglon. Este archivo por si mismo no hace nada")



