#!/usr/bin/python3
# -*- coding: utf8 -*-

from utilidades.funciones import *

simb_func = frozenset(("x", "sen", "cos", "tan"))
simb_const = frozenset(("e", "pi"))
simbolos = simb_func.union(simb_const)


def en_alfabeto(c=''):
    en_alf = False
    if c.isalpha():
        if c in ('a', 'c', 'e', 'n', 'o', 's', 't', 'x'):  # sen, cos, tan, e, x
            en_alf = True
    return en_alf


class ErrorLexico(Exception):
    pass


class ErrorSintactico(Exception):
    pass


class Token:
    clasificacion = 0
    contenido = ''

    t_desconocido = -1
    t_signo = 0  # "+"|"-"
    t_entero = 1 # D+
    t_decimal = 2 # .D+
    t_cociente = 3 # /
    # t_constante = 4 #
    t_variable = 5
    t_sen = 6
    t_cos = 7
    t_tan = 9
    t_const_e = 10
    t_potencia = 11
    t_producto = 12
    t_parent_i = 13
    t_parent_d = 14
    t_const_pi = 15
    t_identificador = 16

    def __init__(self, contenido='', clasificacion=-1):
        self.contenido = contenido
        self.clasificacion = clasificacion

    def __repr__(self):
        cadena = ''
        cadena += '<Objeto Token, '
        cadena += self.__str_clasf()
        cadena += ', '
        cadena += self.contenido
        cadena += '>'
        return cadena

    def __str_clasf(self):
        if self.clasificacion == self.t_desconocido:
            return "desconocido"
        elif self.clasificacion == self.t_signo:
            return "signo"
        elif self.clasificacion == self.t_entero:
            return "entero"
        elif self.clasificacion == self.t_decimal:
            return "decimal"
        elif self.clasificacion == self.t_cociente:
            return "cociente"
        # elif self.clasificacion == self.t_constante:
        #    return "constante"
        elif self.clasificacion == self.t_variable:
            return "variable"
        elif self.clasificacion == self.t_sen:
            return "f_sen"
        elif self.clasificacion == self.t_cos:
            return "f_cos"
        elif self.clasificacion == self.t_tan:
            return "f_tan"
        elif self.clasificacion == self.t_const_e:
            return "const_e"
        elif self.clasificacion == self.t_potencia:
            return "potencia"
        elif self.clasificacion == self.t_producto:
            return "producto"
        elif self.clasificacion == self.t_parent_i:
            return "parent_i"
        elif self.clasificacion == self.t_parent_d:
            return "parent_d"
        elif self.clasificacion == self.t_const_pi:
            return "const_pi"
        elif self.clasificacion == self.t_identificador:
            return "identificador"


class AnalizadorLexico(Token):
    def __init__(self, raw_func):
        super().__init__()
        self.raw_func = raw_func
        self.vacio = True
        if len(raw_func) > 0:
            self.vacio = False

    def next_token(self):
        if self.vacio:
            return
        f = -1
        estado = 0
        buffer = ''
        while estado != f:
            if len(self.raw_func) > 0:
                c = self.raw_func[0]
            else:
                c = ''
            c = c.lower()
            if estado == 0:  # estado inicial
                if c.isspace():
                    pass
                elif en_alfabeto(c):
                    estado = 1
                    self.clasificacion = self.t_identificador
                elif c.isdigit():
                    estado = 2
                    self.clasificacion = self.t_entero
                elif c == '.':
                    estado = 3
                    self.clasificacion = self.t_decimal
                elif c == '/':
                    estado = 4
                    self.clasificacion = self.t_cociente
                elif c == '(':
                    estado = 5
                    self.clasificacion = self.t_parent_i
                elif c == ')':
                    estado = 6
                    self.clasificacion = self.t_parent_d
                elif c == '^':
                    estado = 7
                    self.clasificacion = self.t_potencia
                elif c in ('+', '-'):
                    estado = 8
                    self.clasificacion = self.t_signo
                elif c == '*':
                    estado = 10
                    self.clasificacion = self.t_producto
            elif estado == 1:  # identificadores
                if en_alfabeto(c):
                    pass
                else:
                    estado = f
            elif estado == 2:  # enteros
                if c.isdigit():
                    pass
                else:
                    estado = f
            elif estado == 3:  # decimales
                if c.isdigit():
                    estado = 9
                else:
                    raise ErrorLexico
            elif estado in (4, 5, 6, 7, 8, 10):
                estado = f
            elif estado == 9:
                if c.isdigit():
                    pass
                else:
                    estado = f
            if estado > 0:
                buffer += c
            if estado != f:
                self.raw_func = self.raw_func[1:]
            if len(self.raw_func) == 0:
                self.vacio = True
        return Token(buffer, self.clasificacion)


class AnalizadorSintactico(AnalizadorLexico): # ToDo: redefinir las producciones que contienen t_const :'v
    func = 17
    func_const = 18
    func_ident = 19
    func_prod = 20
    func_sen = 21
    func_cos = 22
    func_tan = 23
    func_exp = 24
    func_poten = 25
    func_comp = 26
    func_prim_factor = 27
    func_prim_sum = 28
    func_suma = 29
    func_seg_sum = 30
    func_seg_factor = 31
    t_fraccion = 32

    """
        func := func_sen | func_cos | func_tan | func_exp | func_poten | func_ident | func_comp | func_sum | func_prod | func_cost
        func_sen := t_sen (func_ident | func_comp)
        func_cos := t_cos (func_ident | func_comp)
        func_tan := t_tan (func_ident | func_comp)
        func_exp := t_cost_e t_poten (func_ident | func_comp)
        func_poten := func_ident t_poten (func_const | func_comp)
        func_ident := t_variable
        func_comp := t_parent_i func t_parent_d
        func_sum := func_prim_sum func_rest_sum
        func_prim_sum := func_sen | func_cos | func_tan | func_exp | func_poten | func_ident | func_comp | func_prod | func_const
        func_rest_sum := (t_signo func) | epsilon
        func_prod := func_prim_fact func_rest_fact
        func_prim_fact := func_sen | func_cos | func_tan | func_exp | func_poten | func_ident | func_comp | func_sum | func_const
        func_rest_fact := (t_prod func) | epsilon
        func_const := fraccion | numero
        fraccion := numero t_cociente numero
        numero := t_const_e | t_const_pi | t_entero (t_decimal)?
    """

    def __init__(self, raw_func=""):
        super().__init__(raw_func)

        # producciones gramaticales / derivaciones para construir el parser tree
        self.deriv_func = ((self.func_const,), (self.func_ident,), (self.func_prod,), (self.func_sen,),
                           (self.func_cos,), (self.func_tan,), (self.func_exp,), (self.func_poten,), (self.func_comp,))
        self.deriv_func_const = ((self.t_fraccion,), (self.t_entero,), (self.t_const_e,), (self.t_const_pi,), (self.t_decimal,))
        self.deriv_func_ident = ((self.t_variable,),)
        self.deriv_func_prod = ((self.func_prim_factor, self.t_producto, self.func), (self.func_prim_factor,
                                                                                      self.func_comp))
        self.deriv_func_sen = ((self.t_sen, self.func_comp), (self.func_const,))
        self.deriv_func_cos = ((self.t_cos, self.func_comp),)
        self.deriv_func_tan = ((self.t_tan, self.func_comp),)
        self.deriv_func_exp = ((self.t_const_e, self.t_potencia, self.func_ident), (self.t_const_e, self.t_potencia,
                                                                                    self.func_comp))
        self.deriv_func_poten = ((self.func_ident, self.t_potencia, self.func_const), (self.func_ident, self.t_potencia,
                                                                                       self.func_comp))
        self.deriv_func_comp = ((self.t_parent_i, self.func, self.t_parent_d),)
        self.deriv_func_prim_fact = ((self.func_const,), (self.func_ident,), (self.func_sen,), (self.func_cos,),
                                     (self.func_tan,), (self.func_exp,), (self.func_poten,), (self.func_comp,))
        self.deriv_func_prim_sum = ((self.func_const,), (self.func_ident,), (self.func_sen,), (self.func_cos,),
                                    (self.func_tan,), (self.func_exp,), (self.func_poten,), (self.func_comp,))
        self.deriv_func_sum = ((self.func_prim_sum, self.func_seg_sum),)
        self.deriv_func_seg_sum = ((self.t_signo, self.func_seg_sum), (-1,))
        self.deriv_func_seg_factor = ((self.t_producto, self.func_seg_factor), (-2,))
        self.t = self.next_token()

    def funcion(self):
        self.parse(self.deriv_func)

    def parse(self, deriv=()):
        for derivacion in deriv:
            pass
        """f = None
        for i in deriv:
            if self.t.clasificacion == i[0]:
                f = self.match(i)
            if f is None:
                continue
        if f is None:
            raise ErrorSintactico
        return f"""


    def match(self, i):
        g = None
        if i == self.func_const:
            self.parse(self.deriv_func_const)
        elif i == self.func_ident:
            self.parse(self.deriv_func_ident)
        elif i == self.func_prod:
            self.parse(self.deriv_func_prod)
        elif i == self.func_sen:
            self.parse(self.deriv_func_sen)
        elif i == self.func_cos:
            self.parse(self.deriv_func_cos)
        elif i == self.deriv_func_tan:
            self.parse(self.deriv_func_tan)
        elif i == self.func_exp:
            self.parse(self.func_exp)
        elif i == self.func_comp:
            self.parse(self.deriv_func_comp)
        elif i == self.func_prim_factor:
            self.parse(self.deriv_func_prim_fact)
        elif i == self.func_prim_sum:
            self.parse(self.deriv_func_prim_sum)
        elif i == self.func_suma:
            self.parse(self.deriv_func_sum)
        elif i == self.func_seg_sum:
            self.parse(self.deriv_func_seg_sum)
        elif i == self.func_seg_factor:
            self.parse(self.deriv_func_seg_factor)
        elif i == self.t_desconocido:
            raise ErrorLexico
        elif i == self.t_signo:
            return self.t.clasificacion == self.t_signo
        elif i == self.t_entero:
            return self.t.clasificacion == self.t_signo
        elif i == self.t_decimal:
            return self.t.clasificacion == self.t_decimal
        elif i == self.t_cociente:
            return self.t.clasificacion == self.t_cociente
        elif i == self.t_variable:
            return self.t.clasificacion == self.t_variable
        elif i == self.t_sen:
            return self.t.clasificacion == self.t_sen
        elif i == self.t_cos:
            return self.t.clasificacion == self.t_cos
        elif i == self.t_tan:
            return self.t.clasificacion == self.t_tan
        elif i == self.t_const_e:
            return self.t.clasificacion == self.t_const_e
        elif i == self.t_potencia:
            return self.t.clasificacion == self.t_potencia
        elif i == self.t_producto:
            return self.t.clasificacion == self.t_producto
        elif i == self.t_parent_i:
            return self.t.clasificacion == self.t_parent_i
        #elif
        else:
            if i == -1:
                pass
            if i == -2:
                pass
            else:
                raise ErrorSintactico
        return False

    def obtener_func(self):
        self.parse(self.deriv_func)


class LectorFunciones:
    def __init__(self, fracciones=False):
        self.fracciones = fracciones

    def leer_funcion(self):
        while True:
            raw_func = input("Ingrese una función de x\nf(x) = ")
            an_sint = AnalizadorSintactico(raw_func)
            try:
                f = an_sint.obtener_func()
            except ErrorLexico:
                print("Error léxico")
                continue
            except ErrorSintactico:
                print("Error sintactico")
                continue
            break




