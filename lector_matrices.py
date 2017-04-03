#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
lector_matrices.py

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
from fracciones import *


class ErrorEntrada(Exception):
	def __str__(self):
		return str(self.args[0]) + ' en ' + str(self.args[1])


class ElementoInesperado(ErrorEntrada):
	pass


def obtener_tokens(raw_elementos):
	#print("funcion convertir")
	#print(raw_elementos)
	error = -1
	completo = -2
	elementos = []
	elemento = []
	numerador = ''
	denominador = ''
	estado = 0
	for i in raw_elementos:
		# print(i)
		for j in i:
			if j == '':
				continue
			if estado == 0:
				numerador += j
				denominador += j
				if j == '.': estado = 2
				elif '0' <= j <= '9': estado = 1
				elif j == '-': estado = 4
				else: estado = error
			elif estado == 1:
				numerador += j
				if '0' <= j <= '9': pass
				elif j == '.': estado = 2
				elif j == '/':
					estado = 5
					numerador = numerador[:-1]
					elemento.append(numerador)
					denominador = ''
					numerador = ''
				elif j == ';':
					numerador = numerador[:-1]
					elemento.append(numerador)
					numerador = ''
					elemento.append("1")
					denominador = ""
				else: estado = error
			elif estado == 2:
				numerador += j
				if '0' <= j <= '9': pass
				elif j == '/': estado = 6
				elif j == ';':
					numerador = numerador[:-1]
					elemento.append(numerador)
					elemento.append("1")
					numerador = ''
					denominador = ''
				else: estado = error
			elif estado == 3:
				numerador += j
				if '0' <= j <= '9': estado = 1
				elif j == '.': estado = 5
				else: estado = error
			elif estado == 4:
				numerador += j
				if '0' <= j <= '9': pass
				elif j == '/':
					estado = 5
					numerador = numerador[:-1]
					elemento.append(numerador)
					numerador = ""
					denominador = ""
				elif j == ';':
					estado = 9
					numerador = numerador[:-1]
					elemento.append(numerador)
					numerador = ""
					elemento.append("1")
					denominador = ""
				elif j == '.': estado = 4
				else: estado = error
			elif estado == 5:
				denominador += j
				if j == '.': estado = 6
				elif j == '-': estado = 7
				elif '0' <= j <= '9': estado = 8
			elif estado == 6:
				denominador += j
				if '0' <= j <= '9': pass
				elif j == ';': estado = completo
				else: estado = error
			elif estado == 7:
				denominador += j
				if j == '.': estado = 6
				elif '0' <= j <= '9': pass
				elif j == ';': estado = completo
				else: estado = error
			elif estado == 8:
				denominador += j
				if '0' <= j <= '9': pass
				elif j == '.': estado = 6
				elif j == ';':
					estado = completo
					denominador = denominador[:-1]
					elemento.append(denominador)
					denominador = ''
				else: estado = error
			elif estado == 9:
				elemento.append(numerador)
				denominador = 1
				elemento.append(denominador)
				numerador = ''
				denominador = ''
			elif estado == error:
				raise ElementoInesperado(j, i)
			elif estado == completo and j != '':
				raise ElementoInesperado(j, i)
		elementos.append(elemento)
		elemento = []
		estado = 0
	"""for i in elementos:
		for j in i:
			j = float(j)"""
	return elementos


def dividir(raw_row):
	#print("funcion dividir")
	#print(raw_row)
	raw_row = raw_row.lower()
	raw_row += ' '
	elementos = []
	elemento = ''
	cont = -1
	for i in raw_row:
		#print(i)
		cont += 1
		if i == ' ':
			if len(elemento) > 0:
				elemento += ';'  # fin de elemento para la conversion posterior
				elementos.append(elemento)
				elemento = ''
			continue
		if '0' <= i <= '9' or i == '/' or i == '.' or i == '-':
			elemento += i
		else:
			raise ErrorEntrada(i, raw_row[cont:])
	if elemento != '':
		elementos.append(elemento)
	#print(elementos)
	return elementos


def analizar_renglon(raw_row):
	try:
		elementos = dividir(raw_row)
	except ErrorEntrada as err:
		print("No se comprende:", err)
		return
	try:
		elementos = obtener_tokens(elementos)
	except ElementoInesperado as err:
		print("No se esperaba:", err)
		return False
	return elementos





def ingresar():
	print(
"""Máximo 20 renglones/columnas
	a11 a12 ... a1n  <enter>
	a21 a22 ... a2n  <enter>
	 .   .  .    .      .
	 .   .   .   .      .
	 .   .    .  .      .
	am1 am2 ... amn
	;                <enter>

	Ingrese 'c' para corregir el renglon anterior
	Ingrese 'cN' para corregir el renglon N""")
	print("Ingrese matriz")
	raw_matrix = []  # :v
	matriz = []
	cont = 0
	cont_bak = 0
	corregir = False
	while cont < 21:
		if cont == 20:
			print("Limite alcanzado\n¿Corregir algún renglón?")
			try:
				cont = int(input("renglón: ")) - 1
				if cont < 1 or cont > cont_bak + 1:
					raise ValueError
			except ValueError:
				print("Ingrese un entero entre 1 y %d" % (cont+1))
			corregir = True
			continue
		if not corregir:
			raw_matrix.append(input("Renglon %i\t" % (cont + 1)))
		else:
			raw_matrix[cont] = input("Renglon %i\t" % (cont + 1))
			corregir = False
			cont = cont_bak
			if cont == 20:
				continue
		if len(raw_matrix[cont]) == 0:
			corregir = True
			continue
		if raw_matrix[cont][-1] == 'c':
			corregir = True
			continue
		if len(raw_matrix[cont]) > 1 and raw_matrix[cont][-2] == 'c':
			cont_bak = cont
			try:
				cont = int(raw_matrix[cont][-1]) - 1
			except ValueError:
				print("Para corregir debe ingresar un entero positivo")
				continue
			corregir = True
			continue
		if raw_matrix[cont][-1] == ';':
			raw_matrix[cont] = raw_matrix[cont][:-1]
			break
		raw_matrix[cont] = analizar_renglon(raw_matrix[cont])
		print(raw_matrix[cont])
		if not raw_matrix[cont]:
			corregir = True
			continue
		cont += 1
		cont_bak = cont
	return raw_matrix


def convertir(raw_matrix):
	print("funcion convertir")
	print(raw_matrix)
	matriz = []
	cont = 0
	contar = False
	decimales = 0
	for renglon in raw_matrix:
		if len(renglon) == 0:
			continue
		print(matriz)
		matriz.append([])
		print(matriz)
		print("renglon", renglon)
		for elemento in renglon:
			print("elemento", elemento)
			for componente in elemento:
				decimales = 0
				print("componente", componente)
				for caracter in componente:
					print("caracter", caracter)
					if contar:
						decimales += 1
					if caracter == '.':
						contar = True
			print(cont, len(matriz))
			matriz[cont].append(Fraccion(int(float(elemento[0]) * 10 ** decimales), int(float(elemento[1]) * 10 ** decimales)))
		cont += 1
	return matriz

if __name__ == '__main__':
	print("""Modulo que define funciones para leer matrices interactivamente
y convertir el texto ingresado en objetos Fraccion. Este archivo por si mismo no hace nada""")