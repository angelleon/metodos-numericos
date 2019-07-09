#!/usr/bin/python3
# -*- coding: utf8 -*-

"""
lector_puntos

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

import logging

log = logging.getLogger(__name__)


class ErrorLexico(Exception):
    def __init__(self, lin=0, col=0):
        self.lin = lin
        self.col = col

    def __str__(self):
        return "Error léxico {0}:{1}".format(self.lin, self.col)


class ErrorSintactico(Exception):
    def __init__(self, lin=0, col=0):
        self.lin = lin
        self.col = col

    def __str__(self):
        return "Error sintactico\nlin: {0}, col: {1}".format(self.lin, self.col)


class Token:
    desconocido = 0
    signo = 1
    entero = 2
    decimal = 3
    cociente = 4
    parent_i = 5
    parent_d = 6
    coma = 7
    t_EOF = 8

    contenido = ""
    clasificacion = 0

    def str_clasif(self, clasif):
        if clasif == 0:
            return "desconocido"
        elif clasif == 1:
            return "signo"
        elif clasif == 2:
            return "entero"
        elif clasif == 3:
            return "decimal"
        elif clasif == 4:
            return "cociente"
        elif clasif == 5:
            return "parent_i"
        elif clasif == 6:
            return "parent_d"
        elif clasif == 7:
            return "coma"
        elif clasif == 8:
            return "EOF"


class AnalizadorLexico(Token):
    def __init__(self, raw_points=""):
        self.__raw_points = raw_points
        self.__pos_i = 0
        self.pos_f = len(raw_points)
        if self.pos_f == 0:
            self.vacio = True
        else:
            self.vacio = False
        self.__lin = 1
        self.__col = 1

    def get_attrib(self):
        return {"lin": self.__lin, "col": self.__col, "pos": self.__pos_i}

    def set_attrib(self, attrib: dict):
        log.debug("método set_attrib({})".format(attrib))
        self.__col = attrib["col"]
        self.__lin = attrib["lin"]
        self.__pos_i = attrib["pos"]
        if self.__pos_i == len(self.__raw_points):
            self.vacio = True
        else:
            self.vacio = False

    def set_raw_points(self, raw_points):
        self.__raw_points = raw_points
        self.__pos_i = 0
        self.pos_f = len(raw_points)

    def next_token(self):
        log.debug("método next_token()")
        estado = 0
        f = -1
        raw_points = self.__raw_points[self.__pos_i:]
        log.debug('raw_points = "{}"'.format(raw_points))
        buffer = ""
        while estado != f:
            if not self.vacio:
                c = raw_points[:1]
            else:
                c = ""
            log.debug("c = '{}'".format(c if c != "\n" else r"\n"))
            if estado == 0:
                if c.isspace():
                    if c == '\n':
                        pass
                elif c.isdigit():
                    estado = 2
                    self.clasificacion = self.entero
                elif c == '.':
                    estado = 3
                    self.clasificacion = self.decimal
                elif c in ('+', '-'):
                    estado = 1
                    self.clasificacion = self.signo
                elif c == '(':
                    estado = 6
                    self.clasificacion = self.parent_i
                elif c == ')':
                    estado = 7
                    self.clasificacion = self.parent_d
                elif c == ",":
                    estado = 5
                    self.clasificacion = self.coma
                elif c == '/':
                    estado = 4
                    self.clasificacion = self.cociente
                elif len(c) == 0:
                    self.clasificacion = self.t_EOF
                    self.contenido = ''
                else:
                    raise ErrorLexico
            elif estado == 2:
                if c.isdigit():
                    estado = 2
                else:
                    estado = f
            elif estado == 3:
                if c.isdigit():
                    estado = 9
                else:
                    raise ErrorLexico
            elif estado == 9:
                if c.isdigit():
                    pass
                else:
                    estado = f
            else:
                estado = f
            if len(raw_points) == 0:
                self.vacio = True
                break
            if estado >= 0:
                raw_points = raw_points[1:]
                buffer += c
                self.__pos_i += 1
                self.__col += 1
                if c == "\n":
                    self.__lin += 1
                    self.__col = 1
        self.contenido = buffer
        log.debug("Token: clasif={0} contenido=\"{1}\"".format(self.str_clasif(self.clasificacion), self.contenido))


class AnalizadorSintactico(AnalizadorLexico):
    def __init__(self, raw_points):
        super().__init__(raw_points)

    def match(self, clasificacion: int):
        log.debug("método match({})".format(self.str_clasif(clasificacion)))
        self.next_token()
        if self.clasificacion != clasificacion:
            return
        if clasificacion == self.entero:
            return int(self.contenido)
        elif clasificacion == self.decimal:
            return float(self.contenido)
        else:
            return True

    def punto(self):
        log.debug("método punto()")
        attrib = self.get_attrib()
        coincidencia = self.match(self.parent_i)
        if coincidencia is None:
            self.set_attrib(attrib)
            parentesis = False
        else:
            parentesis = True
        coincidencia = self.numero()
        if coincidencia is None:
            if self.vacio:
                return None, None
            raise ErrorSintactico(attrib["lin"], attrib["col"])
        else:
            abscisa = coincidencia
        coincidencia = self.match(self.coma)
        if coincidencia is None:
            if self.vacio:
                return None, None
            raise ErrorSintactico(attrib["lin"], attrib["col"])
        coincidencia = self.numero()
        if coincidencia is None:
            raise ErrorSintactico(attrib["lin"], attrib["col"])
        else:
            ordenada = coincidencia
        if parentesis:
            coincidencia = self.match(self.parent_d)
            if coincidencia is None:
                raise ErrorSintactico(attrib["lin"], attrib["col"])
        return abscisa, ordenada

    def numero(self):
        log.debug("método numero()")
        attrib = self.get_attrib()
        coincidencia = self.match(self.signo)
        if coincidencia is None:
            signo = 1
            self.set_attrib(attrib)
        else:
            signo = -1
        attrib = self.get_attrib()
        coincidencia = self.fraccion()
        if coincidencia is None:
            self.set_attrib(attrib)
        else:
            numero = coincidencia
            return numero
        coincidencia = self.match(self.entero)
        if coincidencia is None:
            self.set_attrib(attrib)
            entero = 0
        else:
            entero = coincidencia
        attrib = self.get_attrib()
        coincidencia = self.match(self.decimal)
        if coincidencia is None:
            self.set_attrib(attrib)
            decimal = 0
        else:
            decimal = coincidencia
        numero = entero + decimal
        return signo * numero

    def fraccion(self):
        log.debug("método fraccion()")
        attrib = self.get_attrib()
        coincidencia = self.match(self.entero)
        if coincidencia is None:
            self.set_attrib(attrib)
            return None
        else:
            numerador = coincidencia
        attrib = self.get_attrib()
        coincidencia = self.match(self.cociente)
        if coincidencia is None:
            self.set_attrib(attrib)
            return None
        attrib = self.get_attrib()
        coincidencia = self.match(self.entero)
        if coincidencia is None:
            self.set_attrib(attrib)
            raise ErrorSintactico(attrib["lin"], attrib["col"])
        else:
            denominador = coincidencia
        return numerador / denominador







