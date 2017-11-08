#!/usr/bin/python3
# -*- coding: utf8 -*-

import logging
import traceback
import sys
# from .fracciones import Fraccion
import utilidades.funciones as funcion

log = logging.getLogger(__name__)


class ErrorLexico(Exception):
    def __init__(self, pos=0):
        self.pos = pos


class ErrorSintactico(ErrorLexico):
    def __init__(self, pos=0):
        super().__init__(pos)


class Token:
    """Clase que define los tokens básicos a reconocer en la entrada de texto"""
    contenido = ""
    clasificacion = 0

    t_desconocido = 0
    t_signo = 1
    t_entero = 2
    t_decimal = 3
    t_cociente = 4
    t_variable = 5
    t_potencia = 6
    t_EOS = 7

    def str_casif(self, clasificacion):
        if clasificacion == self.t_desconocido:
            return "desconocido"
        elif clasificacion == self.t_signo:
            return "signo"
        elif clasificacion == self.t_entero:
            return "entero"
        elif clasificacion == self.t_decimal:
            return "decimal"
        elif clasificacion == self.t_cociente:
            return "cociente"
        elif clasificacion == self.t_variable:
            return "variable"
        elif clasificacion == self.t_potencia:
            return "potencia"
        elif clasificacion == self.t_EOS:
            return "EndOfString"
        else:
            raise ValueError


class AnalizadorLexico(Token):
    """Clase que obtiene cada token el la entrada cruda (raw_poly)"""
    def __init__(self, raw_poly):
        log.debug("Analizador léxico inicializado con argumento: rawpoly=\"{0}\"".format(raw_poly))
        self.raw_poly = raw_poly
        self.pos_inic = 0
        self.pos_fin = 0

    def next_token(self):
        log.debug("método next_token()")
        raw_poly = self.raw_poly[self.pos_inic:]
        log.debug("raw_poly: " + raw_poly)
        estado = 0
        f = -1
        buffer = ''
        pos = 0
        while estado != f:
            if len(raw_poly) > 0:
                c = raw_poly[:1]
            else:
                c = ''
            log.debug("c: " + c)
            log.debug("estado: {0}".format(estado))
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
                elif len(c) == 0:
                    self.clasificacion = self.t_EOS
                    self.contenido = ''
                else:
                    raise ErrorLexico(self.pos_inic)
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
            elif estado == 6:
                if c.isdigit():
                    pass
                else:
                    estado = f
            elif estado == 7:
                estado = f
                self.clasificacion = self.t_variable
            if self.pos_inic == len(self.raw_poly):
                break
            if estado > 0:
                raw_poly = raw_poly[1:]
                pos += 1
                buffer += c
                self.pos_inic += 1
        self.contenido = buffer
        log.debug("Token: clasif={0} contenido=\"{1}\"".format(self.str_casif(self.clasificacion), self.contenido))


class AnalizadorSintactico(AnalizadorLexico):
    """Clase que define las gramaticas a reconocer en la entrada, hace el parseo a objetos Polinomio
    del modulo funcion"""
    def __init__(self, raw_poly):
        log.debug("Analizador sintactico inicializado con argumento: rawpoly=\"{0}\"".format(raw_poly))
        super().__init__(raw_poly)

    def match(self, t):
        """Método que reconoce tokens en la entrada"""
        log.debug("método match(t={0} tipo={1})".format(self.str_casif(t), type(t)))
        log.debug("posicion actual: {0}\n{1}\n{2}".format(self.pos_inic, self.raw_poly, (" " * self.pos_inic) + "^~~~~~"))
        match = False
        pos = self.pos_inic
        self.next_token()
        if t == self.clasificacion:
            match = True
        else:
            self.pos_inic = pos
            return
        if t == self.t_signo:
            if self.contenido == '+':
                return funcion.Constante(1)
            elif self.contenido == "-":
                return funcion.Constante(-1)
            else:
                return
        elif t == self.t_entero:
            try:
                match = int(self.contenido)
            except ValueError:
                raise ErrorSintactico
        elif t == self.t_decimal:
            try:
                match = float(self.contenido)
            except ValueError:
                raise ErrorSintactico
        log.debug("coincidencia={0} tipo={1}".format(match, type(match)))
        return match

    def polinomio(self):
        """Gramatica de nivel superior en el lenguaje"""
        log.debug("método polinomio()")
        polinomio = None
        prim_term = self.prim_term()
        if prim_term is not None:
            seg_term = self.rest_term()
            if seg_term is None:
                seg_term = funcion.Constante(0)
            else:
                pass
        else:
            raise ErrorSintactico(self.pos_inic)
        polinomio = funcion.Suma(prim_term, seg_term)
        return funcion.Polinomio(terminos=polinomio)  # convierte de objeto FuncionSuma a objeto FuncionPolinomio
        # para aplicar TFC de forma "simple"

    def prim_term(self):
        """Gramatica que define el primer termino del polinomio.
        Éste tiene que ser No Vacio"""
        log.debug("método prim_term()")
        p_i = self.pos_inic
        coincidencia = self.match(self.t_signo)
        coef = 1
        if coincidencia in (1, -1):
            coef = coincidencia
        else:
            self.pos_inic = p_i
        coincidencia = self.termino()
        log.debug("termino={0} tipo={1}".format(coincidencia, type(coincidencia)))
        if coincidencia is not None:
            return coincidencia * coef
        else:
            raise ErrorSintactico(self.pos_inic)

    def rest_term(self):
        """Gramatica que define el resto de los terminos.
        Puede ser una lista de terminos, en cuyo caso devuelve una suma recursiva
        o una lista vacia en cuyo caso devuelve None"""
        log.debug("método rest_term()")
        if self.pos_inic == len(self.raw_poly):
            return funcion.Constante(0)
        else:
            coef = self.match(self.t_signo)
            if coef is not None:
                poly = self.polinomio()
                if poly is not None:
                    poly.coeficientes[0] *= coef if isinstance(coef, (int, float)) else coef.y
                    return poly
                else:
                    raise ErrorSintactico(self.pos_inic)
            else:
                coef = funcion.Constante(0)
            return coef

    def termino(self):
        """Gramatica que define un termino cualquiera del polinomio"""
        log.debug("método termino()")
        p_i = self.pos_inic
        coincidencia = self.coeficiente()
        if coincidencia is not None:
            coef = coincidencia
        else:
            self.pos_inic = p_i
            coef = 1
        p_i = self.pos_inic
        coincidencia = self.match(self.t_variable)
        if coincidencia is not None:
            const = False
        else:
            self.pos_inic = p_i
            const = True
        if const:
            return funcion.Constante(coef)
        else:
            p_i = self.pos_inic
            coincidencia = self.match(self.t_potencia)
            if coincidencia is not None:
                coincidencia = self.match(self.t_entero)
                if coincidencia is not None:
                    exp = coincidencia
                else:
                    raise ErrorSintactico(self.pos_inic)
            else:
                exp = 1
                self.pos_inic = p_i
            return funcion.Producto(funcion.Constante(coef), funcion.Potencia(exp))

    def coeficiente(self):
        """Gramatica que define el coeficiente de un termino del polinomio"""
        log.debug("método coeficiente()")
        p_i = self.pos_inic
        coincidencia = self.fraccion()
        if coincidencia is not None:
            return coincidencia
        else:
            self.pos_inic = p_i
        p_i = self.pos_inic
        coincidencia = self.match(self.t_entero)
        entero = 1
        hay_entero = True
        if coincidencia is not None:
            entero = coincidencia
        else:
            hay_entero = False
            self.pos_inic = p_i
        p_i = self.pos_inic
        coincidencia = self.match(self.t_decimal)
        if coincidencia is not None:
            return float((entero if hay_entero else 0) + coincidencia)
        else:
            if entero is None:
                self.pos_inic = p_i
                raise ErrorSintactico(self.pos_inic)
            else:
                return float(entero if hay_entero else 1)

    def fraccion(self):
        """Gramatica que define una fraccion entero / entero"""
        log.debug("método fraccion()")
        p_i = self.pos_inic
        coincidencia = self.match(self.t_entero)
        if coincidencia:
            numerador = coincidencia
        else:
            self.pos_inic = p_i
            return
        p_i = self.pos_inic
        coincidencia = self.match(self.t_cociente)
        if coincidencia:
            pass
        else:
            self.pos_inic = p_i
            return
        denominador = self.match(self.t_entero)
        if denominador:
            return numerador / denominador
        else:
            raise ErrorSintactico(self.pos_inic)


class LectorPolinomios:
    """Clase que lee polinomios (podría ser solo un función :("""
    def leer_polinomio(self):
        log.debug("método leer_polinomio()")
        while True:
            raw_poly = input("Ingrese un polinomio\nP(x) = ")
            a_sint = AnalizadorSintactico(raw_poly)
            try:
                poly = a_sint.polinomio()
            except ErrorSintactico as e_sint:
                log.warning("Error sintactico\n{0}\n{1}".format(raw_poly, (" " * e_sint.pos + "^~~~~~~")))
                if log.level == logging.WARNING:
                    traceback.print_exception(*sys.exc_info())
                continue
            except ErrorLexico as e_lex:
                log.warning("Error léxico\n{0}\n{1}".format(raw_poly, (" " * e_lex.pos + "^~~~~~~")))
                if log.level == logging.WARNING:
                    traceback.print_exception(*sys.exc_info())
                continue
            return poly




