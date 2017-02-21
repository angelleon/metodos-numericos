#!/bin/env python3
# -*- coding: utf8 -*-
import sys
import re
import time


def evaluar_poly(x, exponentes=[0], coeficientes=[1]):
	print("funcion evaluar_poly")
	#print(x, exponentes, coeficientes)
	imagen = 0
	for i in range(0, len(coeficientes)):
		imagen += coeficientes[i] * x ** exponentes[0]
	return imagen


def modo_interactivo():
	print("funcion modo_interactivo")
	print("Opciones")
	return [None, None, None, None]


def obtener_terminos(raw_poly):
	print("funcion obtener_terminos")
	motor = re.compile("[^a-z0-9-\+^\.]")
	error = motor.search(raw_poly)
	if error is not None:
		print("error en el polinomio\nno se comprende:", error.group())
		return error.group()
	motor = re.compile("([+-]?([0-9]*|[0-9]*\.[0-9]+)[a-z](\^[0-9])?)")
	terminos = []
	while True:
		print("longitud: ", len(raw_poly), "\npolinomio: " + str(raw_poly))
		print(terminos)
		termino = motor.search(raw_poly)
		if len(raw_poly) == 0:
			break
		elif termino is not None:
			terminos.append(termino.group())
		elif termino is None and len(raw_poly) > 0:
			print("Fin de los terminos con x")
			motor = re.compile("[+-]?([0-9]*|[0-9]*\.[0-9]+)+")
			continue
		raw_poly = raw_poly[0:termino.start()] + raw_poly[termino.end():]
	print("terminos: ", terminos)
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
	motor = re.compile("[a-z]")
	variables = set()
	for i in terminos:
		coincidencia = motor.search(i)
		if coincidencia is not None:
			variables.add(coincidencia.group())
			variable = coincidencia.group()
	if len(variables) > 1:
		print("Ingrese funciones de una variable")
		return None
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


def buscar_duplicados(lista):
	print("funcion buscar_duplicados")
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


def reducir_terminos(coeficientes, exponentes):
	print("funcion reducir_terminos")
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


def analizar_poly(raw_poly=''):
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
	time.sleep(10)
	return [coeficientes, exponentes, polinomio, variable]


def probar_intervalo(coeficientes, exponentes, x0, xf):
	print("funcion probar_intervalo")
	if evaluar_poly(x0, exponentes, coeficientes) * evaluar_poly(xf, exponentes, coeficientes) < 0:
		return [x0, xf]
	dx = abs(x0 - xf) / float(100)
	xi = x0
	for i in range(0, 100):
		print(xi, dx, x0, xf)
		if evaluar_poly(xi, exponentes, coeficientes) * evaluar_poly(xf, exponentes, coeficientes) < 0:
			if i <= 50:
				return [x0, xi]
			else:
				return [xi, xf]
		xi += dx

	return False


def bisectar(coeficientes, exponentes, x0, xf, n_signif):
	print("funcion bisectar")
	tolerancia = 0.05 * 10 ** (2 - n_signif)
	error = tolerancia * 2
	cont = 0
	xm = (x0 + xf) / float(2)
	xm_anterior = xm * 2
	while abs(error) > tolerancia:
		if evaluar_poly(x0, exponentes, coeficientes) * evaluar_poly(xm, exponentes, coeficientes) < 0:
			xf = xm
		elif evaluar_poly(xm, exponentes, coeficientes) * evaluar_poly(xf, exponentes, coeficientes) < 0:
			x0 = xm
		error = (xm - xm_anterior) * 100.0 / xm
		xm_anterior = xm
		xm = (x0 + xf) / 2.0
		cont += 1
	return [xm, cont, error]


def imprimir_ayuda():
	print("funcion imprimir_ayuda")
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
	print("funcion main")
	if len(argv) == 1:
		parametros = modo_interactivo()
	elif len(argv) == 2 and (argv[1] == "-h" or argv[1] == "--help"):
		imprimir_ayuda()
	elif len(argv) != 5:
		print("El programa recible 4 argumentos, %d dados" % (len(argv) - 1))
		imprimir_ayuda()
		return
	elif len(argv) == 5:
		parametros = analizar_poly(argv[1])
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
	coeficientes = parametros[0]
	exponentes = parametros[1]
	polinomio = parametros[2]
	variable = parametros[3]
	x0 = parametros[4]
	xf = parametros[5]
	n_signif = parametros[6]
	if n_signif < 1:
		print("CIFRAS_SIGNIFICATIVAS debe ser mayor o igual a 1")
		return
	intervalo = probar_intervalo(coeficientes, exponentes, x0, xf)
	if not intervalo:
		print("No se enconró una raíz en el intervalo. Intente con un intervalo diferente")
		return
	elif intervalo[0] != x0 or intervalo[1] != xf:
		print("Hay dos raices en el intervalo.\nUsando subintervalo [" + intervalo[0] + ',' + intervalo[1] + ']')
		if intervalo[0] != x0:
			x0 = intervalo[0]
		elif intervalo[1] != xf:
			xf = intervalo[1]
	print("Bisectando ", polinomio, " en el intervalo [", x0, ',', xf, ']')
	inicio = time.clock()
	resultados = bisectar(coeficientes, exponentes, x0, xf, n_signif)
	tiempo_ejecucion = time.clock() - inicio
	raiz = resultados[0]
	iteraciones = resultados[2]
	error = resultados[3]
	print("Resultados:")
	print("Raiz encontrada en " + variable + "= " + raiz)
	print("Iteraciones: " + iteraciones)
	print("Error: " + error)
	print("Tiempo de ejecución: ", tiempo_ejecucion)

if __name__ == '__main__':
	main(sys.argv)
