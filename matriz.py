#!/usr/bin/python3
# -*- coding: utf8 -*-


from fracciones import *


class MatrizNoRectangular(Exception):
	def __str__(self):
		return str(self.args[0]) + " elementos en renglón " + str(self.args[1])


class OperacionNoDefinida(Exception):
	pass


class SumaNoDefinida(OperacionNoDefinida):
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
		if self.ceros == self.n:
			self.pivote = Fraccion(0)
			return
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
	def __init__(self, renglones, aumentada=False):
		print("Matriz()")
		print(renglones)
		self.m = len(renglones)
		maxi = len(renglones[0])
		for i in range(self.m):
			if maxi != len(renglones[i]):
				raise MatrizNoRectangular(len(renglones[i]), i+1)
		self.n = maxi
		if aumentada:
			self.n //= 2
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
		self.det = None
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

	def submatriz(self, ren_inic, col_inic, ren_final=None, col_final=None):
		if ren_final is None and col_final is None:
			ren_final = ren_inic
			col_final = col_inic
			ren_inic = 1
			col_inic = 1
		renglones = []
		ren_inic -= 1
		col_inic -= 1
		print(ren_inic, ren_final, col_inic, col_final)
		for i in range(ren_inic, ren_final):
			renglones.append([])
			for j in range(col_inic, col_final):
				renglones[i-ren_inic].append(self[i][j])
				print(self[i][j])
		print(renglones)
		return Matriz(renglones)

	def ordenar(self, imprimir=False, oper=0):
		i = 1
		while i <= self.m:
			for j in range(self.m - i):
				if self.renglones[j].ceros > self.renglones[j + 1].ceros:
					oper += 1
					if imprimir:
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
		if imprimir:
			self.print()

	def reduccion_gaussiana(self, imprimir=False, oper=0):
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
				if self.renglones[i].ceros == self.n:
					continue
				for j in range(self.m):
					if i == j:
						continue
					if self.renglones[i].ceros == self.renglones[j].ceros:
						oper += 1
						alfa = (self.renglones[i].recip_pivote() * self.renglones[j].pivote) * -1
						if imprimir:
							print("\nOperacion ", oper)
							self.print_suma(j, i, alfa)
						self.renglones[j] += self.renglones[i] * alfa
						cont += 1
		self.ordenar(imprimir, oper)
		self.escalonada = True
		if imprimir:
			self.print()

	def gauss_jordan(self, unos=False, imprimir=False, oper=0):
		print("Metodo gauss_jordan")
		if self.escal_reducida:
			return
		if not self.escal_reducida:
			self.reduccion_gaussiana(imprimir)
		for i in range(1, self.m):
			for j in reversed(range(i)):
				if self.renglones[j][self.renglones[i].ceros] != 0:
					oper += 1
					print("\nOperacion", oper)
					alfa = (self.renglones[i].recip_pivote() * self.renglones[j][self.renglones[i].ceros]) * -1
					self.renglones[j] += self.renglones[i] * alfa
					self.print_suma(j, i, alfa)
		if unos:
			for i in range(self.m):
				alfa = self[i].pivote.reciproco()
				self.renglones[i] = self[i] * alfa
				if imprimir:
					self.print_suma(i, i, alfa)
		self.escal_reducida = True
		if imprimir:
			self.print()

	def determinante(self):
		if not self.cuadrada:
			raise OperacionNoDefinida
		self.reduccion_gaussiana(False)
		acum = 1
		for i in range(self.n):
			for j in range(self.n):
				if i == j:
					acum = self[i][j] * acum
		self.det = acum
		return acum

	def inversa(self, imprimir=False):
		if not self.cuadrada:
			raise OperacionNoDefinida
		renglones = []
		for i in range(self.n):
			renglones.append([])
			for j in range(self.n):
				renglones[i].append(self[i][j])
			for j in range(self.n):
				if j == i:
					renglones[i].append(Fraccion(1))
				else:
					renglones[i].append(Fraccion(0))
		aumentada = Matriz(renglones, True)
		aumentada.gauss_jordan(True, imprimir)
		print(1, self.n + 1, self.m, self.n * 2)
		return aumentada.submatriz(1, self.n+1, self.m, self.n * 2)

	def fact_lu(self):
		elementales = []
		for

	def print_cambio_reng(self, a, b):
		print("")
		operacion_1 = 'R%i <--> R%i' % (a+1, b+1)
		operacion_2 = 'R%i <--> R%i' % (b+1, a+1)
		for i in range(len(self.renglones)):
			if i == a:
				print(self[i], operacion_1)
			elif i == b:
				print(self[i], operacion_2)
			else:
				print(self[i])

	def print_suma(self, a, b, alfa):
		print("")
		alfa = str(alfa)
		if alfa[0] != '-':
			alfa = '+' + alfa
		operacion = "R%d = R%d %sR%d" % (a+1, a+1, alfa, b+1)
		for i in range(len(self.renglones)):
			if i == a:
				print(self[i], operacion)
			else:
				print(self[i])

	def print(self):
		print("")
		for i in self.renglones:
			print(i)

if __name__ == '__main__':
	print("Modulo que define las clases Matriz y Renglon. Este archivo por si mismo no hace nada")



""""""