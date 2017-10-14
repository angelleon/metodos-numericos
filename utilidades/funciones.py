#!/usr/bin/env python3
# -*- coding: utf8 -*-

from utilidades.util import factorial
from math import sin, cos


class Funcion:
    """Clase base que representa funciones"""
    def __init__(self):
        pass

    def evaluar(self, a):
        pass

    @staticmethod
    def derivar(self):
        return Funcion()

    def integrar(self, a, b):
        pass


class Constante(Funcion):
    def __init__(self, y=0):
        super().__init__()
        self.y = y

    def __eq__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return self.y == other
        elif isinstance(other, Constante):
            return self.y == other.y
        raise ValueError

    def evaluar(self, a):
        return self.y


class Suma(Funcion):
    def __init__(self, terminos=()):
        super().__init__()
        self.terminos = []
        for i in terminos:
            self.terminos.append(i)

    def evaluar(self, a):
        """Evalua la función en x=a obteniendo así f(a)"""
        suma = None
        for i in self.terminos:
            suma += i.evaluar()
        return suma


class Potencia(Funcion):
    """Clase que rtepresenta las funciones de la forma x^n"""
    def __init__(self, n=1):
        super().__init__()
        self.n = n

    def evaluar(self, a):
        return a ** self.n


class Producto(Funcion):
    """Clase que representa en producto de dos funciones f y g"""
    def __new__(cls, f=Constante(1), g=Funcion()):
        """Para monomios con coeficioente 0 se regresa la funcioón constante y=0 en vez de un
        objeto de clase Producto"""
        if isinstance(f, (int, float, Constante)):
            if f == 0:
                return Constante(0)

    def __init__(self, f=Constante(1), g=Funcion()):
        super().__init__()
        if isinstance(f, (int, float)):
            f = Constante(f)
        if isinstance(g, (int, float)):
            g = Constante(g)
        self.f = f
        self.g = g

    def evaluar(self, a):
        return self.f.evaluar(a) * self.g.evaluar(a)

    def derivar(self):
        if isinstance(self.f, Constante):
            return Producto(self.f.evaluar(), self.g.derivar())
        elif isinstance(self.g, Constante):
            return Producto(self.g.evaluar(), self.f.derivar())
        else:
            return Suma((Producto(self.f, self.g.derivar()), Producto(self.f.derivar(), self.g)))


class Racional(Funcion):
    def __init__(self):
        super().__init__()


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
        return Producto(-1, Seno())


class Polinomio(Suma):
    def __init__(self, coeficientes=(1,0), exponentes=(1, 0), grado=None):
        terminos = []
        if grado is not None:
            pass
        for i, j in coeficientes, exponentes:
            terminos.append(Producto(i, Potencia(j)))
        super().__init__(terminos)


class PolTaylor(Polinomio):
    def __init__(self, f=Funcion(), k=None, c=None):
        if k < 0:
            raise ValueError
        self.k = k
        self.c = c
        self.f = f
        coeficientes = []
        exponentes = []
        if k  is None and c is None:
            raise ValueError
        for i in range(k):
            coeficientes.append(self.nuevo_coef())
            exponentes.append(k)
            f = f.derivar()
        super().__init__(coeficientes, exponentes)

    def nuevo_termino(self):
        self.k += 1
        self.terminos.append(Producto(self.nuevo_coef(), Potencia(self.k)))

    def nuevo_coef(self):
        return self.f.evaluar(self.c) / factorial(self.k)


class PolMaclaurin(PolTaylor):
    def __init__(self, f=Funcion(), k=0):
        super().__init__(f, k, 0)
