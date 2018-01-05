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

<<<<<<< HEAD
import logging as log
=======
__doc__ = """Modulo que define funciones para leer matrices interactivamente
y convertir el texto ingresado en objetos. Este archivo por si mismo no hace nada"""

import logging
>>>>>>> :u
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


class FinSEL(Exception):
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
    vacio = False

    def __init__(self, raw_reng=""):
        super().__init__()
<<<<<<< HEAD
        if len(raw_reng) == 0:
            raise EntradaVacia
        self.raw_rang = raw_reng
=======
        if len(raw_ecu) == 0:
            self.vacio = True
        else:
            self.vacio = False
        self.__raw_ecu = raw_ecu
        self.__pos_i = 0
>>>>>>> :u

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
<<<<<<< HEAD
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
=======
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
>>>>>>> :u
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
        :param rest_term: iterable
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
        raw_ecu = ''
        while True:
            raw_ecu = input("Ingrese ecuación\n(E{0}): ".format(n_ecu + 1))
            self.an_sint.set_raw_ecu(raw_ecu)
            try:
                return self.an_sint.ecuacion()
            except (ErrorLexico, ErrorSintactico) as error:
                print(error)
                continue
<<<<<<< HEAD
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
=======
>>>>>>> :u

    def leer_sel(self):
        sel = SEL()
        ecuaciones = []
        n_ecu = 0
        while True:
            ecu, fin_sel = self.leer_ecu(n_ecu)
            ecu = self.reducir(ecu)
            if fin_sel:
                break
<<<<<<< HEAD
            except Reingreso:
                continue
            if not bandera:
                break
        return matriz_coef
=======
            ecuaciones.append(ecu)
            n_ecu += 1
        return 0

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
>>>>>>> :u


if __name__ == '__main__':
    print(__doc__)
