#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
lector_sel.py

Copyright 2017 Angel Leon <luianglenlop@gmail.com>
t
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

import logging as log
from .fracciones import *
from .matriz import Matriz, Renglon
from .sel import SEL


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
        self.signo = 1
        self.entero = 2
        self.decimal = 3
        self.incognita = 4
        self.cociente = 5
        self.igual = 6
        self.fin_sel = 7

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
            return "signo"
        elif self.clasificacion == 2:
            return "entero"
        elif self.clasificacion == 3:
            return "decimal"
        elif self.clasificacion == 4:
            return "incognita"
        elif self.clasificacion == 5:
            return "cociente"
        elif self.clasificacion == 6:
            return "igual"
        elif self.clasificacion == 7:
            return "fin S.E.L."


class AnalizadorLexico(Token):
    vacio = False

    def __init__(self, raw_reng=""):
        super().__init__()
        if len(raw_reng) == 0:
            raise EntradaVacia
        self.raw_rang = raw_reng

    def next_token(self):
        print("next token")
        if not self.vacio:
            f = -1
            estado = 0
            buffer = ""
            clasificacion = self.desconocido
            raw_reng = self.raw_rang
            # print(raw_reng)
            while estado != f:
                print(raw_reng)
                if len(raw_reng) > 0:
                    c = raw_reng[0].upper()
                else:
                    c = ""
                print(c)
                if c == '':
                    break
                if estado == 0:
                    if c.isspace():
                        pass
                    elif c in ('+', '-'):
                        estado = 1
                        clasificacion = self.signo
                    elif c.isdigit():
                        estado = 2
                        clasificacion = self.entero
                    elif c == '.':
                        estado = 3
                        clasificacion = self.decimal
                    elif c.isalpha():
                        estado = 5
                        clasificacion = self.incognita
                    elif c == '/':
                        estado = 7
                        clasificacion = self.cociente
                    elif c == '=':
                        estado = 9
                        clasificacion = self.igual
                    elif c == ';':
                        estado = 10
                        clasificacion = self.fin_sel
                    else:
                        raise ErrorLexico
                elif estado == 2:
                    if c.isdigit():
                        estado = 2
                    else:
                        estado = f
                elif estado == 3:
                    if c.isdigit():
                        estado = 4
                    else:
                        raise ErrorLexico
                elif estado == 4:
                    if c.isdigit():
                        pass
                    else:
                        estado = f
                elif estado == 5:
                    clasificacion = self.incognita
                    estado = f
                elif estado in (1, 7, 9):
                    estado = f
                elif estado == 10:
                    raise FinMatriz
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
        print("next elem")
        numerador = ""
        denominador = ""
        incognita = "const"
        f1 = -1
        f2 = -2
        f3 = -3
        f4 = -4
        estado = 0
        while estado not in (f1, f2, f3, f4):
            if len(self.tokens) > 0:
                t = self.tokens[0]
                print(self.tokens)
                print(t)
            if estado == 0:
                if t.clasificacion == self.signo:
                    estado = 1
                    numerador += t.contenido
                elif t.clasificacion == self.entero:
                    estado = 2
                    numerador += t.contenido
                elif t.clasificacion == self.decimal:
                    estado = 3
                    numerador += t.contenido
                elif t.clasificacion == self.incognita:
                    estado = 4
                elif t.clasificacion == self.igual:
                    estado = f4
                elif t.clasificacion == self.fin_sel:
                    raise FinMatriz
                else:
                    raise ErrorSintactico
            elif estado == 1:
                if t.clasificacion == self.entero:
                    estado = 2
                elif t.clasificacion == self.decimal:
                    estado = 3
                elif t.clasificacion == self.incognita:
                    estado = 4
                else:
                    raise ErrorSintactico
                numerador += t.contenido
            elif estado == 2:
                if t.clasificacion == self.decimal:
                    estado = 3
                    numerador += t.contenido
                elif t.clasificacion == self.cociente:
                    estado = 6
                else:
                    estado = f1
            elif estado == 3:
                if t.clasificacion == self.cociente:
                    estado = 6
                else:
                    estado = f1
            elif estado == 4:
                if t.clasificacion == self.entero:
                    estado = 9
                else:
                    estado = f3
                if numerador in ('+', '-'):
                    numerador += '1'
                incognita = t.contenido
            elif estado == 6:
                if t.clasificacion == self.decimal:
                    estado = 7
                    denominador += t.contenido
                elif t.clasificacion == self.entero:
                    estado = 8
                    denominador += t.clasificacion
                else:
                    raise ErrorSintactico
            elif estado == 7:
                if t.clasificacion == self.incognita:
                    estado = 4
                else:
                    estado = f2
            elif estado == 8:
                if t.clasificacion == self.decimal:
                    estado = 7
                    denominador += t.contenido
                elif t.clasificacion == self.incognita:
                    estado = 4
                else:
                    estado = f2
            elif estado == 9:
                estado = f3
                incognita += t.contenido
            if estado not in (f1, f2, f3):
                self.tokens = self.tokens[1:]
        if estado == f1:
            denominador = 1
        if estado in (f1, f2, f3):
            if fracciones:
                coeficiente = Fraccion(float(numerador), float(denominador))
            else:
                return self.negativo

    def ecuacion(self):
        self.miembro()
        coincidencia = self.match(self.igual)
        if coincidencia is None:
            raise ErrorSintactico(self.get_attrib()["pos"])
        self.miembro()

    def miembro(self):
        coincidencia = self.termino()
        if coincidencia is None:
            raise ErrorSintactico(self.get_attrib()["pos"])
        terminos = [coincidencia]
        coincidencia = self.rest_terminos()

    def expandir_term(self, rest_term: tuple[dict]):
        """
        :parameter self: object
        :param rest_term: tuple(dict)
        :rtype: object
        """
        term = {}
        while True:
            for key in rest_term[0].keys():
                if key in term.keys():
                    term[key] += rest_term[0][key]
                else:
                    term[key] = rest_term[0][key]
            if rest_term[1] is None:
                return term
            rest_term = rest_term[1]

    def termino(self):
        coincidencia = self.match(self.signo)
        if coincidencia is None:
            signo = self.positivo
        else:
            signo = coincidencia
        coincidencia = self.numero()
        if coincidencia is None:
            hay_coef = False
            coeficiente = 1
        else:
            hay_coef = True
            coeficiente = coincidencia
        coincidencia = self.variable()
        if coincidencia is None:
            variable = "const"
        else:
            variable = coincidencia
        if not hay_coef and variable == "const":
            return
        return {variable: signo * coeficiente}

    def rest_terminos(self):
        coincidencia = self.match(self.signo)
        if coincidencia is None:
            return {"const": 0}, None
        else:
            signo = coincidencia
        coincidencia = self.numero()
        if coincidencia is None:
            hay_coef = False
            coef = 1
        else:
            hay_coef = True
            coef = coincidencia
        coincidencia = self.variable()
        if coincidencia is None:
            variable = "const"
        else:
            variable = coincidencia
        if (not hay_coef) and variable == "const":
            raise ErrorSintactico
        return {variable: signo * coef}, self.rest_terminos()

    def variable(self):
        attrib = self.get_attrib()
        coincidencia = self.match(self.incognita)
        if coincidencia is None:
            self.set_attrib(attrib)
            return
        variable = coincidencia
        attrib = self.get_attrib()
        coincidencia = self.match(self.entero)
        if coincidencia is None:
            return variable
        else:
            return str(variable) + str(coincidencia)

    def numero(self):
        attrib = self.get_attrib()
        coincidenca = self.fraccion()
        if coincidenca is None:
            self.set_attrib(attrib)
        else:
            return coincidenca
        attrib = self.get_attrib()
        coincidenca = self.match(self.entero)
        if coincidenca is None:
            self.set_attrib(attrib)
            entero = 0
        else:
            entero = coincidenca
        attrib = self.get_attrib()
        coincidenca = self.match(self.decimal)
        if coincidenca is None:
            self.set_attrib(attrib)
            decimal = 0
        else:
            decimal = coincidenca
        return entero + decimal

    def fraccion(self):
        attrib = self.get_attrib()
        coincidencia = self.match(self.entero)
        if coincidencia is None:
            self.set_attrib(attrib)
            return
        numerador = coincidencia
        attrib = self.get_attrib()
        coincidencia = self.match(self.cociente)
        if coincidencia is None:
            self.set_attrib(attrib)
            return
        coincidencia = self.match(self.entero)
        if coincidencia is None:
            self.set_attrib(attrib)
            return
        denominador = coincidencia
        if numerador / denominador == numerador // denominador:
            return numerador // denominador
        return numerador / denominador


class LectorSEL:
    def __init__(self, cuadrado=False, fracciones=True):
        self.cuadrada = cuadrado
        self.fracciones = fracciones
        self.matriz_coef = Matriz()
        self.matriz_indep = Matriz()

    def reducir(self, prim_miem, seg_miem):
        const = 0
        incog = {}
        for dicc in prim_miem:  # recorriendo lista de diccionarios
            if 'const' in dicc.keys():
                const += (-1) * dicc['const']  # "moviendo" costantes al segundo miembro
            else:
                for key in dicc.keys():  # selecciona la única clave del diccionario
                    if key not in incog.keys():  # buscando incognitas repetidas
                        incog[key] = dicc[key]  # agrega la incognita al diccionario de incognitas
                    else:  # cuando la incognita ya se encontro anteriormente en el primer miembro
                        incog[key] += dicc[key]  # el valor de los coeficientes
                        #  se suma para así reducir terminos semejantes
        prim_miem = []
        for key, value in incog.keys(), incog.values():
            prim_miem.append({key: value})  # el primer miembro ahora solo tiene incognitas no repetidas
        seg_miem.append({'const': const})
        const = 0
        incog = {}
        for dicc in seg_miem:
            if 'const' in dicc.keys():
                const += dicc['const']  # reduce las constantes del segundo miembro
            else:
                for key in dicc.keys():
                    if key not in incog.keys():
                        incog[key] = (-1) * dicc[key]  # "moviendo" incognitas al primer miembro
                    else:
                        incog[key] += (-1) * dicc[key]  # reduciendo incognitas del segundo miembro
                        # y "moviendolas" al primero
        seg_miem = const
        for dicc in prim_miem:
            for key in incog.keys():
                if key in dicc.keys():
                    dicc[key] += incog[key]  # reduciendo terminos semejantes en el primer miembro
                    # despues de "moverlos" desde el segundo
        incog = {}
        for dicc in prim_miem:
            for key in dicc:
                incog[key] = dicc[key]
        prim_miem = incog
        return prim_miem, seg_miem

    def ordenar(self, prim_miem):
        longitudes = {}
        for key in prim_miem.keys():  # obtiene las incognitas
            if str(len(key)) in longitudes.keys():  # obtiene la longitud del string que representa cada una
                longitudes[str(len(key))] = [key]  # crea una lista para las strings de longitud n
            else:
                longitudes[str(len(key))].append(key)  # todas las incognitas de longitud n van a una lista
        elementos = []
        for longitud in sorted(longitudes.keys()):  # se ordenan las longitudes
            for key in sorted(longitudes[longitud]):  # se ordenan las incognitas de longitud n
                elementos.append({key: prim_miem[key]})  # se agregan las incognitas en orden con sus coeficientes
        return elementos

    def convertir(self, raw_ecu):
        an_lex = AnalizadorLexico(raw_ecu)
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
        pos = len(elementos)
        for i in range(len(elementos)):
            if 'igual' in elementos[i].keys():
                pos = i
                break
        if pos in (0, len(elementos)):
            raise ErrorSintactico
        prim_miem = elementos[0:pos]
        seg_miem = elementos[pos+1:]
        prim_miem, indep = self.reducir(prim_miem, seg_miem)
        prim_miem = self.ordenar(prim_miem)
        coef = []
        incog = []
        for dicc in prim_miem:
            for key in dicc:
                incog.append(key)
                coef.append(dicc[key])
        return [coef, incog, indep]

    def leer_ecu(self, n_ecu=1):
        raw_ecu = None
        while True:
            raw_ecu = input("Ingrese ecuación {0}\n(E{0}): ".format(n_ecu))
            try:
                ecu = self.convertir(raw_ecu)
            except ErrorLexico as e_lex:
                print(e_lex)
                continue
            except ErrorSintactico as e_sint:
                print(e_sint)
                continue
            break
        return ecu

    def corregir(self, sel):
        while True:
            print(sel)
            answ = input("""¿Desea corregir algo?
    <Enter>\tTodo correcto
    2\tCorregir renglón
    3\tIngresar matriz de nuevo
    (opción): """)
            if answ == "1":
                n_ecu = None
                while True:
                    answ = input("¿Qué ecuación desea corregir?\n(n): ")
                    try:
                        n_ecu = int(answ)
                    except ValueError:
                        continue
                    except KeyboardInterrupt:
                        break
                    sel[n_ecu] = self.leer_ecu(n_ecu)
                    break
            elif answ == "2":
                raise Reingreso
            break
        return sel, False

    def leer_sel(self):
        i = 0
        j = -1
        sel = SEL()
        coef = None
        indep = None
        incog = None
        while True:
            while True and i != j:
                if i > 0:
                    print(sel)
                try:
                    sel.append(self.leer_ecu(i + 1))
                except FinMatriz:
                    break
                if i == 0 and self.cuadrada:
                    j = len(matriz_coef[0])
                i += 1
            try:
                bandera = True
                while bandera:
                    matriz_coef, bandera = self.corregir(matriz_coef)
            except FinMatriz:
                break
            except Reingreso:
                continue
            if not bandera:
                break
        return matriz_coef


if __name__ == '__main__':
    print("""Modulo que define funciones para leer matrices interactivamente
y convertir el texto ingresado en objetos Fraccion. Este archivo por si mismo no hace nada""")
