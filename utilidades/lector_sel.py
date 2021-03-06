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

__doc__ = """Modulo que define funciones para leer matrices interactivamente
y convertir el texto ingresado en objetos. Este archivo por si mismo no hace nada"""

import logging
from .fracciones import *
from .matriz import Matriz, Renglon
from .sel import SEL
from typing import Sized

log = logging.getLogger(__name__)


class ErrorLexico(Exception):
    def __init__(self, col=0):
        self.col = col

    def __str__(self):
        return "Error léxico col: " + str(self.col) + "\n" + (" " * self.col) + "^"


class ErrorSintactico(Exception):
    def __init__(self, col=0):
        self.col = col

    def __str__(self):
        return "Error sintactico col: " + str(self.col)


class FinSEL(Exception):
    pass


class EntradaVacia(Exception):
    pass


class Token:
    contenido = ""
    clasificacion = 0

    desconocido = 0
    signo = 1
    entero = 2
    decimal = 3
    incognita = 4
    cociente = 5
    igual = 6
    fin_sel = 7

    positivo = 1
    negativo = -1

    def __repr__(self):
        return self.__str__()

    def str_clasif(self, clasificacion):
        if clasificacion == 0:
            return "desconocido"
        elif clasificacion == 1:
            return "signo"
        elif clasificacion == 2:
            return "entero"
        elif clasificacion == 3:
            return "decimal"
        elif clasificacion == 4:
            return "incognita"
        elif clasificacion == 5:
            return "cociente"
        elif clasificacion == 6:
            return "igual"
        elif clasificacion == 7:
            return "fin S.E.L."
        else:
            return "desconocido"


class AnalizadorLexico(Token):
    def __init__(self, raw_ecu: str):
        super().__init__()
        if len(raw_ecu) == 0:
            self.vacio = True
        else:
            self.vacio = False
        self.__raw_ecu = raw_ecu
        self.__pos_i = 0

    def get_attrib(self):
        return {"pos": self.__pos_i}

    def set_attrib(self, attrib: dict):
        self.__pos_i = attrib["pos"]

    def set_raw_ecu(self, raw_ecu: str):
        self.__raw_ecu = raw_ecu
        self.__pos_i = 0
        if len(raw_ecu) == 0:
            self.vacio = True
            raise EntradaVacia
        else:
            self.vacio = False

    def next_token(self):
        log.debug("next token()")
        log.debug("pos_i: " + str(self.__pos_i))
        f = -1
        estado = 0
        buffer = ""
        raw_ecu = self.__raw_ecu[self.__pos_i:]
        log.debug(raw_ecu)
        while estado != f:
            if len(raw_ecu) > 0:
                c = raw_ecu[:1].upper()
            else:
                c = ""
            log.debug(c)
            if c == '':
                break
            if estado == 0:
                if c.isspace():
                    pass
                elif c in ('+', '-'):
                    estado = 1
                    self.clasificacion = self.signo
                elif c.isdigit():
                    estado = 2
                    self.clasificacion = self.entero
                elif c == '.':
                    estado = 3
                    self.clasificacion = self.decimal
                elif c.isalpha():
                    estado = 5
                    self.clasificacion = self.incognita
                elif c == '/':
                    estado = 7
                    self.clasificacion = self.cociente
                elif c == '=':
                    estado = 9
                    self.clasificacion = self.igual
                elif c == ';':
                    estado = 10
                    self.clasificacion = self.fin_sel
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
                self.clasificacion = self.incognita
                estado = f
            elif estado in (1, 7, 9):
                estado = f
            elif estado == 10:
                self.clasificacion = self.fin_sel
                estado = f
            if estado > 0:
                buffer += c
            if estado != f:
                raw_ecu = raw_ecu[1:]
                self.__pos_i += 1
            if self.__pos_i == len(self.__raw_ecu):
                self.vacio = True
        self.contenido = buffer
        log.debug("clasif: {0}: {3}, cont: \"{1}\", pos_i: {2}".format(self.clasificacion, self.contenido, self.__pos_i, self.str_clasif(self.clasificacion)))


class AnalizadorSintactico(AnalizadorLexico):
    def __init__(self, raw_ecu: str):
        super().__init__(raw_ecu)

    def match(self, clasificacion: int):
        log.debug("match({0}: {1})".format(clasificacion, self.str_clasif(clasificacion)))
        attrib = self.get_attrib()
        self.next_token()
        if self.clasificacion != clasificacion:
            self.set_attrib(attrib)
            log.debug("Not found: {0}: {1}".format(clasificacion, self.str_clasif(clasificacion)))
            return
        log.debug("Found: {0}: {1}".format(clasificacion, self.str_clasif(clasificacion)))
        if clasificacion == self.entero:
            return int(self.contenido)
        if clasificacion == self.decimal:
            return float(self.clasificacion)
        if clasificacion == self.signo:
            if self.contenido == '+':
                return self.positivo
            else:
                return self.negativo
        if clasificacion == self.incognita:
            return self.contenido
        else:
            return True

    def ecuacion(self):
        log.debug("ecuacion()")
        prim_miem = self.miembro()
        coincidencia = self.match(self.igual)
        if coincidencia is None:
            raise ErrorSintactico(self.get_attrib()["pos"])
        seg_miem = self.miembro()
        fin_sel = self.match(self.fin_sel)
        return ((prim_miem, seg_miem), fin_sel)

    def miembro(self):
        log.debug("miembro()")
        coincidencia = self.termino()
        if coincidencia is None:
            raise ErrorSintactico(self.get_attrib()["pos"])
        terminos = coincidencia
        coincidencia = self.rest_terminos()
        rest_term = self.expandir_term(coincidencia)
        for key, value in rest_term.items():
            if key in terminos.keys():
                terminos[key] += value
            else:
                terminos[key] = value
        log.debug(str(type(terminos)) + str(terminos) + str(type(rest_term)) + str(rest_term))
        return terminos

    @staticmethod
    def expandir_term(rest_term: tuple):
        """
        :parameter self: object
        :param rest_term: Sized
        :rtype: dict
        """
        log.debug("expandir_term()")
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
        log.debug("termino()")
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
        """
        :rtype: tuple
        """
        log.debug("rest_term()")
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
        log.debug("variable()")
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
        log.debug("numero()")
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
        log.debug("fraccion()")
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
        self.an_sint = AnalizadorSintactico("")
        self.cuadrada = cuadrado
        self.fracciones = fracciones
        self.matriz_coef = Matriz()
        self.matriz_indep = Matriz()

    def corregir(self):
        pass

    def leer_ecu(self, n_ecu):
        while True:
            raw_ecu = input("Ingrese ecuación\n(E{0}): ".format(n_ecu + 1))
            self.an_sint.set_raw_ecu(raw_ecu)
            try:
                return self.an_sint.ecuacion()
            except (ErrorLexico, ErrorSintactico) as error:
                print(error)
                continue

    def leer_sel(self):
        sel = SEL()
        ecuaciones = []
        n_ecu = 0
        while True:
            ecu, fin_sel = self.leer_ecu(n_ecu)
            ecu = self.reducir(ecu)
            if fin_sel:
                break
            ecuaciones.append(ecu)
            n_ecu += 1
        return ecuaciones
    

    @staticmethod
    def reducir(ecu):
        prim_miem = ecu[0]
        seg_miem = ecu[1]
        for key, value in seg_miem.items():
            if key != "const":
                if key in prim_miem.keys():
                    prim_miem[key] -= value
                    del seg_miem[key]
        if "const" in prim_miem.keys():
            seg_miem["const"] -= prim_miem["const"]
            del prim_miem["const"]
        return prim_miem, seg_miem


if __name__ == '__main__':
    print(__doc__)
