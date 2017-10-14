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
from .fracciones import *
from .matriz import Matriz, Renglon


class ErrorLexico(Exception):
    pass


class ErrorSintactico(Exception):
    pass


class Correccion(Exception):
    def __init__(self, renglon):
        self.renglon = renglon


class EntradaVacia(Exception):
    pass


class FinMatriz(Exception):
    pass


class Reingreso:
    pass


class Token:
    def __init__(self, contenido="", clasificacion=0):
        self.contenido = contenido
        self.clasificacion = clasificacion

        self.desconocido = 0
        self.entero = 1
        self.signo = 2
        self.cociente = 3
        self.decimal = 4
        self.correccion = 5
        self.fin_matriz = 6

    def __int__(self):
        if self.clasificacion == self.entero:
            return int(self.contenido)
        elif self.clasificacion == self.decimal:
            return 0
        else:
            raise ValueError

    def __float__(self):
        if self.clasificacion == self.entero:
            return float(self.contenido)
        elif self.clasificacion == self.decimal:
            return float("0." + self.contenido)
        else:
            return ValueError

    def __str__(self):
        cadena = 'Token <"{0}", {1}, {2}>'.format(self.contenido, self.clasificacion, self.__str_clasif())
        return cadena

    def __repr__(self):
        return self.__str__()

    def __str_clasif(self):
        if self.clasificacion == 0:
            return "desconocido"
        elif self.clasificacion == 1:
            return "entero"
        elif self.clasificacion == 2:
            return "signo"
        elif self.clasificacion == 3:
            return "cociente"
        elif self.clasificacion == 4:
            return "decimal"
        elif self.clasificacion == 5:
            return "correccion"


class AnalizadorLexico(Token):
    vacio = False

    def __init__(self, raw_reng=""):
        super().__init__()
        if len(raw_reng) == 0:
            raise EntradaVacia
        self.raw_rang = raw_reng

    def next_token(self):
        if not self.vacio:
            f = -1
            #f2 = -2
            estado = 0
            buffer = ""
            clasificacion = self.desconocido
            raw_reng = self.raw_rang
            # print(raw_reng)
            while estado != f:
                # print(raw_reng)
                if len(raw_reng) > 0:
                    c = raw_reng[0].upper()
                else:
                    c = ""
                if estado == 0:
                    if c.isspace():
                        pass
                    elif c.isdigit():
                        clasificacion = self.entero
                        estado = 1
                    elif c in ('+', '-'):
                        clasificacion = self.signo
                        estado = 2
                    elif c == '/':
                        clasificacion = self.cociente
                        estado = 3
                    elif c == '.':
                        clasificacion = self.decimal
                        estado = 4
                    elif c == ';':
                        clasificacion = self.fin_matriz
                        estado = 6
                    else:
                        raise ErrorLexico
                elif estado == 1:
                    if c.isdigit():
                        pass
                    else:
                        estado = f
                elif estado == 4:
                    if c.isdigit():
                        estado = 5
                    else:
                        raise ErrorLexico
                elif estado == 5:
                    if c.isdigit():
                        estado = 5
                    else:
                        estado = f
                elif estado in (2, 3, 6):
                    estado = f
                else:
                    raise ErrorLexico
                if estado > 0:
                    buffer += c
                if estado != f:
                    raw_reng = raw_reng[1:]
                    self.raw_rang = raw_reng
                if len(self.raw_rang) == 0:
                    self.vacio = True
            return Token(buffer, clasificacion)
        else:
            return Token()


class AnalizadorSintactico(Token):
    def __init__(self, tokens=()):
        super().__init__()
        # print(tokens)
        if len(tokens) == 0:
            raise EntradaVacia
        self.tokens = []
        for i in tokens:
            self.tokens.append(i)

    def next_elemento(self, fracciones=True):
        numerador = ""
        denominador = ""
        f1 = -1
        f2 = -2
        estado = 0
        while estado not in (f1, f2):
            if len(self.tokens) > 0:
                t = self.tokens[0]
                # print(t)
            if estado == 0:
                if t.clasificacion == self.entero:
                    estado = 2
                elif t.clasificacion == self.decimal:
                    estado = 3
                elif t.clasificacion == self.signo:
                    estado = 1
                elif t.clasificacion == self.fin_matriz:
                    raise FinMatriz
                else:
                    raise ErrorSintactico
                numerador += t.contenido
            elif estado == 1:
                # print(t)
                if t.clasificacion == t.entero:
                    estado = 2
                elif t.clasificacion == t.decimal:
                    estado = 3
                else:
                    raise ErrorSintactico
                numerador += t.contenido
            elif estado == 2:
                if t.clasificacion == self.decimal:
                    estado = 3
                    numerador += t.contenido
                elif t.clasificacion == self.cociente:
                    estado = 4
                else:
                    estado = f1
            elif estado == 3:
                if t.clasificacion == self.cociente:
                    estado = 4
                else:
                    estado = f1
            elif estado == 4:
                if t.clasificacion == self.entero:
                    estado = 5
                elif t.clasificacion == self.decimal:
                    estado = 6
                else:

                    raise ErrorSintactico
                denominador += t.contenido
            elif estado == 5:
                if t.clasificacion == self.decimal:
                    estado = 6
                    denominador += t.contenido
                else:
                    estado = f2
            elif estado == 6:
                estado = f2
            if estado not in (f1, f2):
                self.tokens = self.tokens[1:]
        if estado == f1:
            denominador = 1
        if fracciones:
            elemento = Fraccion(float(numerador), float(denominador))
        else:
            elemento = float(numerador) / float(denominador)
        return elemento


class LectorMatrices:
    def __init__(self, cuadrada=False, fracciones=True):
        self.cuadrada = cuadrada
        self.fracciones = fracciones

    def convertir(self, raw_reng):  # raw_matrix):
        an_lex = AnalizadorLexico(raw_reng)
        elementos = []
        while True:
            if an_lex.vacio:
                break
            elementos.append(an_lex.next_token())
        i = 0
        an_sint = AnalizadorSintactico(elementos)
        elementos = []
        while True:
            elementos.append(an_sint.next_elemento())
            if len(an_sint.tokens) == 0:
                break
        return Renglon(elementos)

    def leer_renglon(self, n_renglon=1):
        raw_reng = None
        while True:
            raw_reng = input("Ingrese renglon {0}\n(R{0}): ".format(n_renglon))
            try:
                r = self.convertir(raw_reng)
            except ErrorLexico as e_lex:
                print(e_lex)
                continue
            except ErrorSintactico as e_sint:
                print(e_sint)
                continue
            break
        return r

    def corregir(self, matriz):
        while True:
            print(matriz)
            answ = input("""¿Desea corregir algo?
    <Enter>\tTodo correcto
    2\tCorregir renglón
    3\tIngresar matriz de nuevo
    (opción): """)
            if answ == "1":
                r = None
                while True:
                    answ = input("¿Qué renglón desea corregir?\n(n): ")
                    try:
                        r = int(answ)
                    except ValueError:
                        continue
                    except KeyboardInterrupt:
                        break
                    matriz[r] = self.leer_renglon(r)
                    break
            elif answ == "2":
                raise Reingreso
            break
        return matriz, False

    def leer_matriz(self):
        i = 0
        j = -1
        matriz = Matriz()
        while True:
            while True and i != j:
                if i > 0:
                    print(matriz)
                try:
                    matriz.append(self.leer_renglon(i+1))
                except FinMatriz:
                    break
                if i == 0 and self.cuadrada:
                    j = len(matriz[0])
                i += 1
            try:
                bandera = True
                while bandera:
                    matriz, bandera = self.corregir(matriz)
            except FinMatriz:
                break
            except Reingreso:
                continue
            if not bandera:
                break
        return matriz


if __name__ == '__main__':
    print("""Modulo que define funciones para leer matrices interactivamente
y convertir el texto ingresado en objetos Fraccion. Este archivo por si mismo no hace nada""")
