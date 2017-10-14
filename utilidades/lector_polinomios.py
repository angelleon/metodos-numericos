#!/usr/bin/python3
# -*- coding: utf8 -*-
#"""


#Copyright 2017 Angel Leon <luianglenlop@gmail.com>

#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
##
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#MA 02110-1301, USA.


#import re
#from polinomios import *

# excepciones al analizar la entrada del usuario
#class ErrorEntrada(Exception):
#    def __str__(self):
#        return "Error en la entrada de datos"


#class ErrorCoeficiente(ErrorEntrada):
#    def __str__(self):
#        return "Error en los coeficientes del polinomio"


#class FuncionConstante(ErrorEntrada):  # lanzada si al reducir los terminos se obtien sólo constantes
#    def __str__(self):
#        return "función constante"


#class CaracterInvalido(ErrorEntrada):
#    def __str__(self):
#        return "caracter invalido"


#class FuncionMultivariable(ErrorEntrada):  # lanzada cuando hay varias literales, el programa usa cualquier letra
    # como variable
#    def __str__(self):
#        return "función multivariable"
#
#class MaxIteraciones(Exception):
#    def __str__(self):
#        return "Se alcanzo el maximo de iteraciones"


#def derivar_poly(coeficientes, exponentes):  # deriva, planeado reemplazar al usar el paradigma OO
#    deriv_coeficientes = []
#    deriv_exponentes = []
#    for i in range(len(coeficientes)):
#        if exponentes[i] != 0:
#            deriv_coeficientes.append(coeficientes[i] * exponentes[i])
#            deriv_exponentes.append(exponentes[i] - 1)
#    return [deriv_coeficientes, deriv_exponentes]
#

# ToDo: terminar para poder ingresar coeficientes como fracciones
#def convertir_fraccion(fraccion):
#    motor = re.compile("[-+]?[0-9]+|[-+]?[0-9]\.[0-9]+")
#    numerador = motor.search(fraccion)
#    fraccion = fraccion[:numerador.start()] + fraccion[numerador.end():]
#    numerador = float(numerador.group())
#    denominador = motor.search(fraccion)
#    denominador = float(denominador.group())
#    return numerador/denominador
#
#
## ToDo: implementar en OO
#def evaluar_poly(x, coeficientes, exponentes):  # obtener la imagen de f en el punto x, por reemplazar en paradigma OO
#    imagen = 0
#    for i in range(0, len(coeficientes)):
#        imagen += coeficientes[i] * x ** exponentes[i]
#    return imagen
#
#
#def leer_poly():  # para modo interactivo
#    while True:
#        raw_poly = input(#Introduzca el polinomio en la forma:
##anx^n + ... + a2x^2 + a1x + a0\npolinomio: )
#try:
#            #return analizar_poly(raw_poly)
#        except ErrorEntrada:
#            #print("\nIntente de nuevo")
#
#
#def leer_tolerancia():
#    while True:
##        try:
#            n = int(input("Introduzca la cantidad de cifras de confianza\nn: "))
#        except ValueError:
#            print("Introduzaca un valor numerico")
#            continue
##        if n < 1:
#            print("El valor de n debe ser un entero positivo")
#            continue
#        break
#    return 0.05 * 10 ** (2 - n)
#
##
#def leer_intervalo():
##    while True:
#        while True:
#            try:
##                x0 = float(input("Introduzca el extremo izquierdo del intervalo"))
#            except ValueError:
#                print("Introduzca un valor numerico")
#                continue
#            break
#        while True:
#            try:
#                xf = float(input("Introduzca el extremo derecho del intervalo"))
#            except ValueError:
##                print("Introduzca un valor numerico")
##                continue
#            break
#        intervalo = analizar_intervalo(x0, xf)
#        if intervalo:
#            break
#    return intervalo
### ToDo: llamar a analizar fracciones
#
#
#def analizar_intervalo(x0, xf):
#    if x0 == xf:
#        return False
#    if x0 > xf:
##        return [xf, x0]
#    return [x0, xf]
#
#
##def buscr_carac_invalidos(raw_poly):  # busca errores de tipeo
#    motor = re.compile("[^a-z0-9-+^./]")
##    if motor.search(raw_poly) is not None:
#        mostrar_error(motor.search(raw_poly).group(), raw_poly)
##        raise CaracterInvalido  # lanzar la excepcion en caso de que algo en el string no se pueda interprtetar
#    # correctamente
#
#
#def obtener_terminos_x(raw_poly):
#    terminos = []
#    termino = ''
#    motor = re.compile("([+-]?([0-9]*|[0-9]*\.[0-9]+)[a-z](\^[0-9])?)")
#    while termino is not None:
#        termino = motor.search(raw_poly)
#        if termino is not None:
#            terminos.append(termino.group())  # guarda el termino encontrado en la lista
#        else:
##            break
#        raw_poly = raw_poly[0:termino.start()] + raw_poly[termino.end():]  # elimina la coincidencia encontrada de la
##    #  cadena para la siguiente iteracion
#    return [terminos, raw_poly]
##
##
#def reducir_terminos_lineales(terminos):
#    termino_lineal = 0
##    for i in terminos:
#        i = float(i)
#        termino_lineal += i
#    return str(termino_lineal)
##
#
#def obtener_terminos_lineales(raw_poly):
#    motor = re.compile("([-+]?[0-9]+)|([-+]([0-9]*\.[0-9]+))")
#    terminos = []
##    termino = motor.search(raw_poly)
##    while termino is not None and len(raw_poly) != 0:
#        termino = motor.search(raw_poly)
#        if termino is not None:
#            terminos.append(termino.group())
#            break
#        raw_poly = raw_poly[0:termino.start()] + raw_poly[termino.end():]  # elimina la coincidencia de la cadena de
##    # entrada para la siguiente iteraccion
#    termino = reducir_terminos_lineales(terminos)
##    return termino
##
#
#def obtener_terminos(raw_poly):
#    buscr_carac_invalidos(raw_poly)
#    respuesta = obtener_terminos_x(raw_poly)
#    terminos = respuesta[0]
#    raw_poly = respuesta[1]
#    terminos.append(obtener_terminos_lineales(raw_poly))
#    return terminos
#
##
#def mostrar_error(error, raw_poly):  # muestra la parte de la cadena de entrada que no se reconoce
#    motor = re.compile(error)
##    coincidencia = motor.search(raw_poly)
#    indicador = "^~~~~~"
#    if coincidencia.start() != 0:
##        for i in range(0, coincidencia.start()):
#            indicador = ' ' + indicador
#    print("\n\t" + raw_poly + '\n\t' + indicador)
#
##
#def obtener_variable(terminos):  # busca la variable, comunmente x, que se usa en el polinomio, en caso de encontrar
#    # más de un caracter en el rango a-z se considera una funcion multivariable, posiblemente por erro de tipeo
#    motor = re.compile("[a-z]")
##    variables = set()
#    variable = None
#    for i in terminos:
#        coincidencia = motor.search(i)
#        if coincidencia is not None:
#            variables.add(coincidencia.group())
#            variable = coincidencia.group()
#    if len(variables) > 1:
#        print("Ingrese funciones de una variable")
#        raise FuncionMultivariable
##    elif len(variables) == 0:  # comprueba que haya al menos un termino con una variable
#        print("El método no se puede aplicar a funciones constantes")
#        raise FuncionConstante
#    return variable
#
##
#def obtener_coeficientes(terminos):
#    motor = re.compile("^([-+]?[0-9]*\.[0-9]+)|^([-+]?[0-9]+)|^([-+])")
##    coeficientes = []
##    for termino in terminos:
#        coincidencia = motor.search(termino)
##        if coincidencia is None:
#            coeficientes.append(1.0)
#            continue
#        coeficiente = coincidencia.group()
##        if coeficiente == '+' or coeficiente == '-':
#            coeficiente += '1'
#        coeficientes.append(float(coeficiente))
##    return coeficientes
#
##
#def obtener_exponentes(terminos):
##    exponentes = []
#    for termino in terminos:
#        coincidencia = re.search("\^[0-9]+", termino)
#        if coincidencia is not None:
##            exponentes.append(int(coincidencia.group()[1:]))
#            continue
#        coincidencia = re.search("[a-z]", termino)
#        if coincidencia is not None:
##            exponentes.append(1)
#        else:
#            exponentes.append(0)
#    return exponentes
#
##
#def buscar_duplicados(lista):  # busca elementos duplicados en una lista, se usa para reducir los terminos con el
#    # mismo exponente en x
##    repetidos = set()
#    indices = []
#    for i in range(len(lista)):
#        if i < len(lista) - 1:
#            for j in range(i+1, len(lista)):
##                if lista[j] == lista[i]:
#                    repetidos.add(lista[j])
#                    break
#    if len(repetidos) == 0:
#        return None
#    cont = 0
#    for i in repetidos:
##        indices.append([])
#        for j in range(0, len(lista)):
#            if i == lista[j]:
#                indices[cont].append(j)
#        cont += 1
#    return indices
#
#
##def reducir_terminos(coeficientes, exponentes):  # reduce terminos con el mismo exponente
#    reducibles = buscar_duplicados(exponentes)
#    if reducibles is None:
##        return None
#    indice_reducidos = []
##    indice_descartados = []
#    for i in reducibles:
#        indice_reducidos.append(i[0])
#        for j in i[1:]:
#            indice_descartados.append(j)
##    for i in reducibles:
#        for j in i:
##            if j != i[0]:
#                coeficientes[i[0]] += coeficientes[j]
#    coef_reducidos = []
#    exp_reducidos = []
#    for i in range(0, len(coeficientes)):
##        if i not in indice_descartados:
#            coef_reducidos.append(coeficientes[i])
#            exp_reducidos.append(exponentes[i])
#    return [coef_reducidos, exp_reducidos]
##
#
#def ordenar(coeficientes, exponentes, terminos):  # ordena linstas paralelas, los elementos de una lista se ordenan y
#    #  los correspondientes (segun su indice) de la otra lista se ordenan con el elemento correspondiente de la
#    # primera lista
##    if exponentes == sorted(exponentes, reverse=True):
#        return None
#    indices = {}
#    cont = 0
#    for i in exponentes:
##        indices[str(i)] = cont
#        cont += 1
#    exponentes.sort(reverse=True)
#    coef_ordenados = []
##    term_ordenados = []
#    for clave in sorted(indices.keys()):
#        coef_ordenados.append(int(coeficientes[indices[clave]]))
##        term_ordenados.append(terminos[indices[clave]])
#    return [coef_ordenados, exponentes, term_ordenados]
##
#
### ToDo: lanzar excepciones en vez de retornar None
#def analizar_poly(raw_poly):
#    if len(raw_poly) == 0:
##        print("No hay entrada")
#        raise ErrorEntrada
#    raw_poly = raw_poly.lower()
#    terminos = obtener_terminos(raw_poly)
##    if isinstance(terminos, str):
#        mostrar_error(terminos, raw_poly)
#        return None
#    elif terminos is None:
##        return None
#    variable = obtener_variable(terminos)
##    if variable is None:
#        return None
##    coeficientes = obtener_coeficientes(terminos)
##    exponentes = obtener_exponentes(terminos)
#    reduccion = reducir_terminos(coeficientes, exponentes)
##    if reduccion is not None:
#        coeficientes = reduccion[0]
##        exponentes = reduccion[1]
#    term_ord = ordenar(coeficientes, exponentes, terminos)
#    if term_ord is not None:
##        coeficientes = term_ord[0]
#        exponentes = term_ord[1]
#        terminos = term_ord[2]
##    str_poly = ''
#    for i in terminos:
#        str_poly += str(i)
##    return [Polinomio(coeficientes, exponentes), str_poly, variable]
#
#def obtener_tokens():
#    pass
#
##
#def probar_intervalo(coeficientes, exponentes, x0, xf):  # busca si en el intervalo hay raices para evitar usar el
#    # metodo en caso de que no
#    if evaluar_poly(x0, coeficientes, exponentes) * evaluar_poly(xf, coeficientes, exponentes) < 0:
#        return [x0, xf]
##    dx = abs(x0 - xf) / float(100)
#    xi = x0
#    for i in range(100):
##        if evaluar_poly(xi, coeficientes, exponentes) * evaluar_poly(xf, coeficientes, exponentes) < 0:
#            if i <= 50:  # devuelve el intervalo más corto
##                return [x0, xi]
#            else:
##                return [xi, xf]
#        xi += dx
#    return False """

from enum import Enum

class ErrorLexico(Exception):
    def __init__(self, pos=-1, poly=None):
        self.pos = None
        self.poly = None
        if pos > -1 and poly is not None:
            self.pos = pos
            self.poly = poly

    def __str__(self):
        cadena =\
"""
===================================================================================
Error Lexico"""
        if self.poly != "":
            cadena += "\nNo se comprende:\n" + self.poly
            if self.pos > -1:
                cadena += " " * (self.pos - 1) + "^-----"
        cadena +=\
"""

==================================================================================="""
        return cadena


class ErrorSintactico:
    pass

class TipoTkn(Enum):
    desconocido = -2
    error = -1
    entero = 0
    variable = 1
    division = 2
    signo = 3
    potencia = 4
    decimal = 5

class Token:
    contenido = ""
    clasif = None

    def __init__(self, clasificacion=TipoTkn.desconocido, contenido=""):
        self.clasif = clasificacion
        self.contenido = contenido


class AnalizadorLexico:
    vacio = True
    long_inicial = 0

    def __init__(self, cadena=""):
        self.cadena = cadena.lower()
        self.raw_poly = self.cadena
        if len(cadena) != 0:
            self.vacio = False
        self.long_inicial = len(self.cadena)

    def next_token(self):
        buffer = ""
        error = -1
        aceptado = 0
        estado = None
        clasif = TipoTkn.desconocido
        while len(self.cadena) != 0:
            c = self.cadena[0]
            if estado is None:
                if c in ('+', '-'):
                    estado = 1
                elif c.isdigit():
                    estado = 2
                elif c == '.':
                    estado = 3
                elif c.isalpha():
                    estado = 4
                else:
                    raise ErrorLexico
            elif estado == 1:
                if c == '.':
                    estado = 3
                elif c.isalpha():
                    estado = 4
                elif c.isdigit():
                    estado = 2
                else:
                    raise ErrorLexico
            elif estado == 2:
                if c in ('+', '-'):
                    estado = aceptado
                elif c.isdigit():
                    pass
                elif c == '.':
                    estado = 3
                else:
                    raise ErrorLexico
            elif estado == 3:
                if c.isdigit():
                    estado = 6
                else:
                    raise ErrorLexico
            elif estado == 4:
                if c == '^':
                    estado = 8
                elif c == '/':
                    estado = 7
                elif c in ('+', '-'):
                    estado = aceptado
                else:
                    raise ErrorLexico
            elif estado == 5:
                if c == '.':
                    estado = 11
                elif c.isdigit():
                    estado = 12
                else:
                    raise ErrorLexico
            elif estado == 6:
                if c.isdigit():
                    pass
                elif c in ('+', '-'):
                    estado = aceptado
                else:
                    raise ErrorLexico
            elif estado == 7:
                if c.isdigit():
                    estado = 10
                else:
                    raise ErrorLexico
            elif estado == 8:
                if c.isdigit():
                    estado = 9
                else:
                    raise ErrorLexico
            elif estado == 9:
                if c.isdigit():
                    pass
                else:
                    estado = aceptado
            elif estado == 10:
                if c.isdigit():
                    pass
                else:
                    estado = aceptado
            elif estado == 11:
                if c.isdigit():
                    estado = 13
                else:
                    raise ErrorLexico
            elif estado == 12:
                if c.isdigit():
                    pass
                elif c == '.':
                    estado = 13
                elif c.isalpha():
                    estado = 4
                else:
                    estado = aceptado
            elif estado == 13:
                if c.isdigit():
                    pass
                elif c in ('+', '-'):
                    estado = aceptado
                else:
                    raise ErrorLexico
        return Token(clasif, buffer)


class AnalizadorSintactico:
    secuencia_tkn = []
    long_inicial = 0

    def __init__(self, secuencia_tkn=()):
        for i in secuencia_tkn:
            self.secuencia_tkn.append(i)
        self.long_inicial = len(secuencia_tkn)

    def obtener_poly(self):
        error = False
        anterior = None
        for tkn in self.secuencia_tkn:
            tkn = Token()
            if anterior is None:
                if tkn.clasif not in (TipoTkn.signo, TipoTkn.sep_decimal, TipoTkn.entero):
                    raise ErrorSintactico
                else:
                    anterior = tkn.clasif
                    continue
            elif anterior == TipoTkn.signo:
                if tkn.clasif not in (TipoTkn.entero, TipoTkn.sep_decimal):
                    raise ErrorSintactico
                else:
                    anterior = tkn.clasif
                    continue
            elif anterior == TipoTkn.entero:
                if tkn.clasif not in (TipoTkn.sep_decimal):
                    pass



def analizar_poly(raw_poly=""):
    raw_poly = raw_poly.lower()
    a_lex = AnalizadorLexico(raw_poly)
    tokens = []
    while not a_lex.vacio:
        tokens.append(a_lex.next_token())
    a_sint = AnalizadorSintactico(tokens)
    return a_sint.obtener_poly()
