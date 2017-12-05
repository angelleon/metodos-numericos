#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Modulo que define funciones elementales"""


from utilidades.util import factorial
from math import sin, cos
import logging
# import sys

log = logging.getLogger(__name__)


class Funcion:
    """Clase base que representa funciones"""
    def __init__(self):
        pass

    def __str__(self):
        return "Función"

    def __repr__(self):
        return "<" + self.__str__() + " >"

    def tex_repr(self):
        return "$f(x) = $"

    def evaluar(self, a):
        return 0

    def derivar(self):
        return Funcion()

    def integrar(self):
        return Funcion()


class Constante(Funcion):
    def __init__(self, y=0.0):
        log.debug("Constante(y={0} tipo={1})".format(y, type(y)))
        super().__init__()
        self.y = y

    def __eq__(self, other):
        if isinstance(other, (int, float)):
            return self.y == other
        elif isinstance(other, Constante):
            return self.y == other.y
        raise ValueError

    def __mul__(self, other):
        log.debug("Constante.__mul__(other={0} tipo={1})".format(other, type(other)))
        if isinstance(other, (int, float)):
            return Constante(self.y * other)
        elif isinstance(other, Constante):
            return Constante(self.y * other.y)
        elif isinstance(other, Funcion):
            return Producto(Constante(self.y), other)
        else:
            raise ValueError

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Constante(self.y + other)
        elif isinstance(other, Constante):
            return Constante(self.y + other.y)
        elif isinstance(other, Funcion):
            return Suma(self, other)
        else:
            raise ValueError

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError
        if isinstance(other, (int, float)):
            return Constante(self.y / other)
        elif isinstance(other, Constante):
            return Constante(self.y / other.y)
        else:
            raise ValueError

    def __int__(self):
        return int(self.y)

    def __float__(self):
        return float(self.y)

    def __repr__(self):
        return "<objeto FuncionConstante, y={0}>".format(self.y)

    def __str__(self):
        return str(self.y)

    def evaluar(self, a):
        return self.y


class Suma(Funcion):
    def __init__(self, f=None, g=None, terminos=()):
        log.debug("Suma(f={0} tipo={1}, g={2} tipo={3})".format(f, type(f), g, type(g)))
        super().__init__()
        self.terminos = []
        if f is None and g is None and len(terminos) > 1:
            g = Constante(0)
            for i in reversed(range(1, len(terminos))):
                f = terminos[i]
                g = Suma(f=f, g=g)
            self.f = terminos[0]
            self.g = g
        elif f is not None and g is not None and len(terminos) == 0:
            self.f = f
            self.g = g
        else:
            pass
            # raise ValueError

    def __repr__(self):
        return "<objeto FuncionSuma, {0} + {1}>".format(self.f, self.g)

    def evaluar(self, a):
        """Evalua la función en x=a obteniendo así f(a)"""
        return self.f.evaluar(a) + self.g.evaluar(a)

    def integrar(self):
        return Suma(self.f.integrar(), self.g.integrar())


class Potencia(Funcion):
    """Clase que rtepresenta las funciones de la forma x^n"""
    def __init__(self, n=1):
        super().__init__()
        self.n = n

    def __repr__(self):
        return "<objeto FuncionPotencia, n={0}>".format(self.n)

    def __str__(self):
        return "x^" + str(self.n)

    def evaluar(self, a):
        return a ** self.n


class Producto(Funcion):
    """Clase que representa en producto de dos funciones f y g"""
    def __new__(cls, f=Constante(1), g=Funcion()):
        """Para productos con algún factor cero se regresa la función constante y=0 en vez de un
        objeto de clase Producto"""
        log.debug("Producto.__new__(f={0} tipo={1}, g={2} tipo={3}".format(f, type(f), g, type(g)))
        if isinstance(f, (int, float)):
            f = Constante(f)
        if isinstance(g, (int, float)):
            g = Constante(g)
        if isinstance(f, Constante):
            if f == 0:
                return Constante(0)
        if isinstance(g, Constante):
            if g == 0:
                return Constante(0)
        if isinstance(f, (int, float, Constante)) and isinstance(g, (int, float, Constante)):
            return Constante(f * g)
        if isinstance(g, Constante) and isinstance(f, Funcion):
            return Producto(g, f)
        return super().__new__(cls)

    def __init__(self, f=Constante(1), g=Funcion()):
        log.debug("Producto(f={0} tipo={1}, g={2} tipo={3}".format(f, type(f), g, type(g)))
        super().__init__()
        self.f = f
        self.g = g

    def __mul__(self, other):
        log.debug("Producto.__mul__(other={0} tipo={1})".format(other, type(other)))
        log.debug("Producto: f={0} tipo={1}, g={2} tipo={3}".format(self.f, type(self.f), self.g, type(self.g)))
        if isinstance(other, (int, float)) and isinstance(self.f, Constante):
            return Producto(Constante(self.f.y * other), self.g)
        elif isinstance(other, Constante) and isinstance(self.f, Constante):
            return Producto(Constante(self.f.y * other.y), self.g)
        elif isinstance(self.f, Funcion):
            return Producto(other, Producto(self.f, self.g))
        else:
            raise ValueError

    def __repr__(self):
        return "<objeto FuncionProducto, {0} * {1}>".format(self.f, self.g)

    def __str__(self):
        return str(self.f) + '*' + str(self.g)

    def evaluar(self, a):
        return self.f.evaluar(a) * self.g.evaluar(a)

    def derivar(self):
        if isinstance(self.f, Constante):
            return Producto(Constante(self.f.evaluar(0)), self.g.derivar())
        elif isinstance(self.g, Constante):
            return Producto(Constante(self.g.evaluar(0)), self.f.derivar())
        else:
            return Suma((Producto(self.f, self.g.derivar()), Producto(self.f.derivar(), self.g)))


class Racional(Funcion):
    def __init__(self):
        super().__init__()


class Identidad(Funcion):
    def __init__(self):
        super().__init__()

    def evaluar(self, a):
        return a

    def derivar(self):
        return Constante(1)

    def integrar(self):
        return Potencia(2)


class Seno(Funcion):
    def __init__(self):
        super().__init__()

    def evaluar(self, a):
        return sin(a)

    def derivar(self):
        return Coseno()


class Coseno(Funcion):
    def __init__(self):
        super().__init__()

    def evaluar(self, a):
        cos(a)

    def derivar(self):
        return Producto(Constante(-1), Seno())


class Polinomio(Funcion):
    def __init__(self, coeficientes=None, exponentes=None, terminos=None):
        super().__init__()
        log.debug("Polinomio(coef={0} tipo={1}, exp={2} tipo={3}, terminos={4} tipo={5})".format(coeficientes, type(coeficientes), exponentes, type(exponentes), terminos, type(terminos)))
        self.coeficientes = []
        self.exponentes = []
        self.grado = None
        if coeficientes is None and exponentes is None and isinstance(terminos, Suma):
            """Necesario para convertir en arreglos las Sumas recursivas obtenidas del parser.
            Podría ser más eficiente pero no hay tiempo para eso :("""
            cont = 0
            f = terminos.f
            while True:
                log.debug("Convirtiendo suma {0}\n a polinomio\nf= {1} tipo={2}\ncont: {3}".format(terminos, f, type(f), cont))
                if isinstance(terminos, Constante):
                    if terminos == 0:
                        break
                if isinstance(f, Producto):
                    if isinstance(f.f, Constante):
                        self.coeficientes.append(f.f.y)
                    else:
                        raise ValueError
                    if isinstance(f.g, Potencia):
                        self.exponentes.append(f.g.n)
                    elif isinstance(f.g, Identidad):
                        self.exponentes.append(1)
                    else:
                        raise ValueError
                elif isinstance(f, Constante):
                    log.debug("termino constante: {0}".format(f))
                    log.debug("terminos restantes: {0}".format(terminos))
                    self.coeficientes.append(f.y)
                    self.exponentes.append(0)
                    if f.y == 0:
                        break
                else:
                    raise ValueError
                if isinstance(terminos, Suma):
                    log.debug("Encontrada Suma en los terminos de la suma")
                    terminos = terminos.g
                    if isinstance(terminos, Suma):
                        log.debug("Asignando el primer gtermino de la suma")
                        f = terminos.f
                if isinstance(terminos, Polinomio):
                    log.debug("Encontrado Polinomio en los terminos de la suma")
                    for i in range(len(terminos.coeficientes)):
                        self.coeficientes.append(terminos.coeficientes[i])
                        self.exponentes.append(terminos.exponentes[i])
                    break
                cont += 1
                log.debug(str(f))
                if cont > 10:
                    raise ValueError
        elif coeficientes is not None and exponentes is not None:
            try:
                iter(coeficientes)
                iter(exponentes)
                if len(coeficientes) != len(exponentes):
                    raise ValueError
                for i in range(len(coeficientes)):
                    self.coeficientes.append(coeficientes[i])
                    self.exponentes.append(exponentes[i])
            except TypeError:
                log.warning("Error de tipo")  # FixMe: no queremos este mensaje en la versión release
                raise
        self.grado = max(self.exponentes)

    def __repr__(self):
        return "<objeto FuncionPolinomio, coef= {0}, exp= {1}>".format(self.coeficientes, self.exponentes)

    def __str__(self):
        cadena = ''
        for i in range(len(self.coeficientes)):
            coef = self.coeficientes[i]
            exp = self.exponentes[i]
            if coef > 0:
                if i != 0:
                    cadena += '+'
                if coef != 1:
                    cadena += str(coef)
            elif self.coeficientes[i] < 0:
                if coef != -1:
                    cadena += str(coef)
                else:
                    cadena += '-'
            if exp != 0:
                cadena += 'x'
                if exp != 1:
                    cadena += '^' + str(exp)
        return cadena

    def tex_repr(self, decimales=-1):
        cadena = "$"
        if decimales >= 0:
            for i in range(len(self.coeficientes)):
                coef = self.coeficientes[i]
                exp = self.exponentes[i]
                entero = int(coef)
                mantisa = coef - entero
                if mantisa < 0:
                    mantisa = str(mantisa)[3:]
                else:
                    mantisa = str(mantisa)[2:]
                if decimales == -1:
                    decimales = len(mantisa)
                if i != 0:
                    if coef >= 0:
                        cadena += "+"
                    else:
                        if entero == 0:
                            cadena += "-"
                cadena += str(entero)
                if len(mantisa) > decimales:
                    cadena += "." + mantisa[:decimales]
                else:
                    cadena += "." + mantisa
                if exp != 0:
                    cadena += "x"
                    if exp > 1:
                        cadena += "^" + str(exp)
            cadena += "$"
            return cadena
        else:
            return "$" + self.__str__() + "$"

    def integrar(self):
        coef = []
        exp = []
        for i in range(len(self.coeficientes)):
            exp.append(self.exponentes[i] + 1)
            coef.append(self.coeficientes[i] / (self.exponentes[i] + 1))
        return Polinomio(coeficientes=coef, exponentes=exp)

    def evaluar(self, a):
        imagen = 0
        for i in range(len(self.coeficientes)):
            imagen += self.coeficientes[i] * a ** self.exponentes[i]
        return imagen


class PolTaylor(Polinomio):
    def __init__(self, f=Funcion(), k=None, c=None):
        if k < 0:
            raise ValueError
        self.k = k
        self.c = c
        self.f = f
        coeficientes = []
        exponentes = []
        if k is None and c is None:
            raise ValueError
        for i in range(k):
            coeficientes.append(self.nuevo_coef())
            exponentes.append(k)
            f = f.derivar()
        super().__init__(coeficientes, exponentes)

    def nuevo_termino(self):  # ToDo: arreglar método roto
        self.k += 1
        # self.terminos.append(Producto(self.nuevo_coef(), Potencia(self.k)))

    def nuevo_coef(self):
        return self.f.evaluar(self.c) / factorial(self.k)


class PolMaclaurin(PolTaylor):
    def __init__(self, f=Funcion(), k=0):
        super().__init__(f, k, 0)
