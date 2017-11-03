#!/usr/bin/python3
# -*- coding: utf8 -*-

from .fracciones import Fraccion
from .funciones import *


class ErrorLexico(Exception):
    def __init__(self, pos=0):
        self.pos = pos


class ErrorSintactico(ErrorLexico):
    def __init__(self, pos=0):
        super().__init__(pos)


class Token:
    contenido = ""
    clasificacion = 0

    t_desconocido = 0
    t_signo = 1
    t_entero = 2
    t_decimal = 3
    t_cociente = 4
    t_variable = 5
    t_potencia = 6


class AnalizadorLexico(Token):
    def __init__(self, raw_poly):
        self.raw_poly = raw_poly
        self.pos_inic = 0
        self.pos_fin = 0

    def next_token(self):
        raw_poly = self.raw_poly[self.pos_inic:]
        estado = 0
        f = -1
        buffer = ''
        pos = 0
        while estado != f:
            if len(raw_poly) > 0:
                c = raw_poly[:1]
            else:
                c = ''
            if estado == 0:
                if c.isspace():
                    pass
                elif c in ('+', '-'):
                    estado = 1
                elif c.isdigit():
                    estado = 2
                elif c == '.':
                    estado = 3
                elif c == '/':
                    estado = 4
                elif c == '^':
                    estado = 5
                elif c.isalpha():
                    estado = 7
            elif estado == 1:
                self.clasificacion = self.t_signo
                estado = f
            elif estado == 2:
                self.clasificacion = self.t_entero
                if c.isdigit():
                    pass
                else:
                    estado = f
            elif estado == 3:
                if c.isdigit():
                    estado = 6
                else:
                    raise ErrorLexico(pos)
                self.clasificacion = self.t_decimal
            elif estado == 4:
                estado = f
                self.clasificacion = self.t_cociente
            elif estado == 5:
                estado = f
                self.clasificacion = self.t_potencia
            elif estado == 7:
                estado = f
                self.clasificacion = self.t_variable
            if self.pos_inic == len(self.raw_poly):
                break
            if estado > 0:
                pos += 1
                buffer += c
                self.pos_inic += 1
        self.contenido = buffer


class AnalizadorSintactico(AnalizadorLexico):
    def __init__(self, raw_poly):
        super().__init__(raw_poly)

    def match(self, t):
        match = False
        if t == self.clasificacion:
            match = True
        else:
            return None
        if t == self.t_signo:
            if self.contenido == '+':
                return Constante(1)
            else:
                return Constante(-1)

    def polinomio(self):
        polinomio = None
        prim_term = self.prim_term()
        if prim_term:
            seg_term = self.rest_term()
            if seg_term:
                pass
            else:
                pass
        else:
            raise ErrorSintactico(self.pos_inic)
        polinomio = Suma(prim_term, seg_term)
        return polinomio

    def prim_term(self):
        p_i = self.pos_inic
        coincidencia = self.match(self.t_signo)
        coef = 1
        if coincidencia in (1, -1):
            coef = coincidencia
        else:
            self.pos_inic = p_i
        coincidencia = self.termino()
        if coincidencia:
            termino = coincidencia * coef
        else:
            raise ErrorSintactico(self.pos_inic)

    def rest_term(self):
        if self.pos_inic == len(self.raw_poly):
            return
        else:
            coef = self.match(self.t_signo)
            if coef:
                term = self.termino()
                if term:
                    return term * coef
                else:
                    raise ErrorSintactico(self.pos_inic)

    def termino(self):
        p_i = self.pos_inic
        coincidencia = self.num()
        if  coincidencia:
            coef = coincidencia
        else:
            self.pos_inic = p_i
            coef = 1
        p_i = self.pos_inic
        coincidencia = self.match(self.t_variable)
        if coincidencia:
            const = False
        else:
            self.pos_inic = p_i
            const = True
        if const:
            return Constante(coef)
        else:
            p_i = self.pos_inic
            coincidencia = self.match(self.t_potencia)
            if coincidencia:
                coincidencia = self.match(self.t_entero)
                if coincidencia:
                    exp = coincidencia
                else:
                    raise ErrorSintactico(self.pos_inic)
            else:
                exp = 1
            return Producto(Constante(coef), Potencia(exp))

    def num(self):
        p_i = self.pos_inic
        coincidencia = self.fraccion()
        if coincidencia:
            return coincidencia
        else:
            self.pos_inic = p_i
        p_i = self.pos_inic
        coincidencia = self.match(self.t_entero)
        entero = 0
        if coincidencia is not None:
            entero = coincidencia
        else:
            self.pos_inic = p_i
        p_i = self.pos_inic
        coincidencia = self.match(self.t_decimal)
        if coincidencia:
            return float(entero + coincidencia)
        else:
            if entero == 0:
                raise ErrorSintactico(self.pos_inic)
            else:
                return float(entero)

    def fraccion(self):
        p_i = self.pos_inic
        coincidencia = self.match(self.t_entero)
        if coincidencia:
            numerador = coincidencia
        else:
            self.pos_inic = p_i
            return False
        p_i = self.pos_inic
        coincidencia = self.match(self.t_cociente)
        if coincidencia:
            pass
        else:
            self.pos_inic = p_i
            return False
        denominador = self.match(self.t_entero)
        if denominador:
            return numerador / denominador
        else:
            raise ErrorSintactico(self.pos_inic)


class LectroPolinomios:
    def leer_polinomio(self):
        while True:
            raw_poly = input("Ingrese un polinomio\nP(x) = ")
            a_sint = AnalizadorSintactico(raw_poly)
            try:
                p = a_sint.polinomio()
            except ErrorSintactico as e_sint:
                print("Error sintactico\n{0}\n{1}".format(raw_poly, (" " * e_sint.pos + "^~~~~~~")))
                continue
            except ErrorLexico as e_lex:
                print("Error léxico\n{0}\n{1}".format(raw_poly, (" " * e_lex.pos + "^~~~~~~")))
                continue
            break




