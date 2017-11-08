#!/usr/bin/python3
# -*- coding: utf8 -*-

# funciones comunes para los programas de metodos numericos
# este script no hace nada por si solo

# Se recomienda no usar el modo interactivo de los programas porque no
# ha sido probado completamente, en lugar de eso se recomienda usar el modo
# no interactivo desde consola
# probado en Python 3.6 (3.6.0 [GCC 6.3.1 20170109]) sobre Linux 4.4

"""
polinomios.py

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


import re  # modulo de expresiones regulares
from fracciones import *

"""
funciones comunes para los programas de metodos numericos
"""

# ToDo: hacer algo para centralizar el manejo de las cosas por hacer (ToDo's)
# ToDo: a medio hacer. implementar el paradigma OO
# ToDo: lanzar excepciones, por algo están declaradas
# ToDo: reimplementar el modo interactivo en todos los programas
# ToDo: hacer funcion main más modular en todos los programas
# ToDo: mover analizador lexico a otro archivo


class Potencia:
    """Clase que define las funciones de la forma ax^n"""
    def __init__(self, coef=1, exp=0):
        #print(repr(Potencia.__doc__))
        self.coef = coef
        self.exp = exp

    def __str__(self):
        """Método que define la conversión del objeto en string"""
        cadena = ''
        if self.coef != 0:
            cadena += str(self.coef)
        if self.exp != 0:
            cadena += 'x^' + str(self.exp)
        else:
            cadena += '1'
        return cadena

    def __repr__(self):
        """Método que define la representación de el objeto dentro del programa"""
        return self.__str__()

    def evaluar(self, x):
        """Método que evalua la potencia en x"""
        return self.coef * x ** self.exp


class Polinomio:
    """Clase que representa polinomios de la forma a0 + a1x + a2x^2 + ... + anx^n"""
    def __init__(self, coef=None, exp=None):
        """Se cran objetos potencia y se guardan coeficiente y esponentes para los metodos derivar e integrar"""
        self.terminos = []
        if coef is not None:
            for i in range(len(coef)):
                try:
                    self.terminos.append(Potencia(coef[i], exp[i]))
                except Exception as ex:
                    print(ex)
            self.coef = coef
            self.exp = exp
        else:
            self.terminos.append(Potencia())
            self.coef = [1]
            self.exp = [0]

    def __str__(self):
        cadena = ''
        for i in self.terminos:
            term = str(i)
            if i != self.terminos[0] and (term[0] != '-' or term[0] != '+'):
                term = '+' + term
            cadena += term
        return cadena

    def __repr__(self):
        return self.__str__()

    def evaluar(self, x):
        imagen = 0
        for i in self.terminos:
            imagen += i.evaluar(x)
        return imagen

    def derivar(self):
        coef_deriv = []
        exp_deriv = []
        for i in range(len(self.coef)):
            if self.exp[i] > 0:
                exp_deriv.append(self.exp[i] - 1)
                coef_deriv.append(self.coef[i] * self.exp[i])
        return Polinomio(coef_deriv, exp_deriv)  # Devuelve la derivada del polinomio como objeto

    def integrar(self, a=None, b=None):
        coef = []
        exp = []
        for i, j in zip(self.coef, self.exp):
            coef.append(i/(j+1))
            exp.append(j+1)
        primitiva = Polinomio(coef, exp)
        #print(coef, exp, primitiva)
        if a is None and b is None:
            return primitiva
        return primitiva.evaluar(b) - primitiva.evaluar(a)

    def sum_riemman(self, a, b, n):
        delta_x = abs(b - a)/n
        sum_imag = 0
        for i in range(n):
            sum_imag += self.evaluar(a + (i * delta_x))
        return sum_imag * delta_x


try:
    import numpy as np
    import matplotlib.pyplot as plt


    def graficar_poly(coeficientes, exponentes, x0, xf, raiz, intervalo_original=None):
        if intervalo_original is not None:  # cuando se ha usado un subintervalo porque hay varias raices se grafica
            # el intervalo original para mostrar las multiples intersecciones con el eje x
            x0 = intervalo_original[0]
            xf = intervalo_original[1]
        if abs(x0 - raiz) < abs(raiz - xf): # graficar en un intervalo simetrico
            xf = raiz + abs(x0 - raiz)
        else:
            x0 = raiz - abs(raiz - xf)
        x_vals = np.linspace(x0, xf, 51)  # valores de x a graficar, 51 puntos equidistantes en el intervalo
        y_vals = None #[evaluar_poly(x, coeficientes, exponentes) for x in x_vals] # imagenes de los valores de x de la
        # linea previa
        plt.axhline(0, color='black')  # ejes, por defecto no aparecen
        plt.axvline(0, color='black')
        plt.grid(True)
        plt.plot(x_vals, y_vals, linewidth=1.0)
        plt.scatter([raiz], [0.0])  # graficar la raiz
        plt.grid(True)  # rejilla
        plt.plot(x_vals, y_vals) # graficar polinomio
        plt.gca().set_aspect('equal', 'datalim')
        plt.show()
except ImportError:
    np = None
    plt = None

    def graficar_poli(coeficientes, exponentes, x0, xf, raiz, intervalo_original=None):
        print("Los modulos necesarios para graficar no se han encontrado.\nInstale NumPy y Matplotlib e intentelo de "
              "nuevo")


max_iteraciones = 1000

if __name__ == '__main__':
    print("Funciones comunes para metodos numericos\nEste archivo no hace nada por si mismo, importe para usar las "
          "funciones declaradas aqui en otros programas")

"""
Escribir un programa que lea un polinomio de grado n>1 e implemente el metodo de newton para aproximar una raiz
graficar el polinomio y las rectas

comparar los metodos de newton y el metodo de la secante.
el usuario introducira un polinomio al programa y este buscará la raiz con newton
dado x0 con el metodo de la secante
con el mismo x0 pidiendo x1
el programa imprimirá la cantidad de iteraciones de cada metodo y el tiempo de ejecución del metodo
la aprox de la raiz

"""
