#!/usr/bin/python3

"""
fracciones.py

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


def mcm(a, b):
    """print("funcion mcm")
    print("a", type(a), a)
    print("b", type(b), b)"""
    return a * b // mcd(a, b)  # mas economico que descomponer en factores primos


def mcd(a, b):  # algoritmo de Euclides para encontrar el mcd
    """print("funcion mcd")
    print("a", type(a), a)
    print("b", type(b), b)"""
    if a < 0 and b < 0:
        a = abs(a)
        b = abs(b)
    if a < 0:
        a *= -1
    if b < 0:
        b *= -1
    if a == 0 and b != 0:
        return b
    elif b == 0 and a != 0:
        return a
    elif a == 0 and b == 0:
        return 1
    while a != b:
        if a > b:
            a -= b
        elif a < b:
            b -= a
    return a


class Fraccion:
    def __init__(self, numerador, denominador=1):
        if denominador == 0:
            raise ZeroDivisionError
        if isinstance(numerador, float):
            numerador, potencia = self.a_entero(numerador)
            denominador *= 10 ** potencia
        if isinstance(denominador, float):
            denominador, potencia = self.a_entero(denominador)
            numerador *= 10 ** potencia
        if denominador < 0:
            numerador *= -1
            denominador = abs(denominador)
        if numerador % 1 == 0 and denominador % 1 == 0:
            numerador = int(numerador)
            denominador = int(denominador)
        divisor = mcd(numerador, denominador)  # reducir fraccion antes de asignar los atributos
        numerador //= divisor
        denominador //= divisor
        if denominador == 0:
            numerador = 0
            denominador = 1
        # print(numerador, type(numerador), " / ", denominador, type(denominador))
        self.numerador = numerador
        self.denominador = denominador

    def __str__(self):
        if self.denominador == 1:
            return str(self.numerador)
        return str(self.numerador) + "/" + str(self.denominador)

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        """Sobrecarga del operador +
        self + other"""
        if other == 0:
            return Fraccion(self.numerador, self.denominador)
        if isinstance(other, int):
            other = Fraccion(other)
        if other.denominador == self.denominador:
            return Fraccion(self.numerador + other.numerador, self.denominador)
        else:
            d = mcm(self.denominador, other.denominador)
            return Fraccion((d // self.denominador * self.numerador) + (d // other.denominador * other.numerador), d)

    def __sub__(self, other):
        """Sobrecarga del operador -
        self - other"""
        if isinstance(other, int):
            other = Fraccion(other)
        if other.denominador == self.denominador:
            return Fraccion(self.numerador - other.numerador, self.denominador)
        else:
            d = mcm(self.denominador, other.denominador)
            return Fraccion((d // self.denominador * self.numerador) - (d // other.denominador * other.numerador), d)

    def __mul__(self, other):
        """Sobrecarga del operador *
        self * other"""
        if isinstance(other, int):
            other = Fraccion(other)
        elif isinstance(other, float):
            other = Fraccion(other)
        return Fraccion(self.numerador * other.numerador, self.denominador * other.denominador)

    # def __rmul__(self, other):
    #    """Sobrecarga del operador *
    #    other * self"""
    #    return self.__mul__(other)

    def __truediv__(self, other):
        """Sobrecarga del operador /
        self / other"""
        if isinstance(other, Fraccion):
            return self.__mul__(other.reciproco())
        elif isinstance(other, int):
            return self.__mul__(Fraccion(1, other))
        else:
            raise ValueError

    def __rtruediv__(self, other):
        """Sobrecarga del operador /
        other / self"""
        # Se usa para que no sea requerido llamar a self.reciproco() para obtener 1 / self
        # Hace posible usar objetos que no implementen el método reciproco() como elementos
        # de la clase matriz (por ejemplo los built-in types)
        if isinstance(other, Fraccion):
            return self.reciproco() * other
        elif isinstance(other, int):
            return self.reciproco() * other
        else:
            raise ValueError

    def __radd__(self, other):
        return self.__add__(other)

    def __lt__(self, other):
        if isinstance(other, int):
            other = Fraccion(other)
        divisor = mcd(self.denominador, other.denominador)
        if self.numerador//divisor < other.numerador//divisor:
            return True
        else:
            return False

    def __iadd__(self, other):
        return self.__add__(other)

    def __gt__(self, other):
        if isinstance(other, int):
            other = Fraccion(other)
        divisor = mcd(self.denominador, other.denominador)
        if self.numerador//divisor > other.numerador//divisor:
            return True
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, int):
            other = Fraccion(other)
        divisor = mcd(self.denominador, other.denominador)
        if self.numerador // divisor == other.numerador // divisor:
            return True
        else:
            return False

    def __abs__(self):
        return Fraccion(abs(self.numerador), abs(self.denominador))

    def __pow__(self, power, modulo=None):
        return Fraccion(self.numerador ** power, self.denominador ** power)

    def __float__(self):
        return self.numerador / self.denominador

    def reciproco(self):
        if self.numerador == 0:
            # return Fraccion(0)
            raise ValueError
        return Fraccion(self.denominador, self.numerador)

    def a_entero(self, a):
        if isinstance(a, float):
            cont = 0
            if a % 1 == 0:
                a = int(a)
            else:
                while True:
                    a *= 10
                    if a % 1 == 0:
                        break
                    if cont > 15:
                        break
            return a, cont
        else:
            return a, 0

if __name__ == '__main__':
    print("Modulo que define la clase fracciones. Este archivo por si mismo no hace nada")
