#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
from math import sqrt
from utilidades.lectores import leer_csignif, leer_cuadrado
from utilidades.util import calc_toler


class Tangente:
    def __init__(self, n):
        """Constructor del objeto que representa a la tangente
        según la ecuación de la recta
        y = sqrt(n) + [1 / (2 sqrt(n))](x - n) """
        self.m = 1 / (2 * sqrt(n))  # Pendiente de la tangente
        self.b = sqrt(n) -n / (2 * sqrt(n)) # Ordenada al origen
        self.x = n  # Valor de x donde la recta toca a la función raíz

    def __str__(self):
        return "y = sqrt({0}) + [1 / (2 sqrt({0})] * (x - {0})".format(self.x)

    def __repr__(self):
        return "Recta tangente a raíz: " + self.__str__()

    def evaluar(self, x):
        return self.m * x + self.b
        

def calc_inter_confi(x, tolerancia, linea):
    delta_x = tolerancia / 10
    intervalo = []
    x_i = None
    val_real = None
    for i in range(2): # i controla el signo de delta_x
        j = 0 # contador del ciclo
        error = tolerancia / 2
        while error < tolerancia:
            x_i = x + delta_x * j * (-1) ** i # suma cuando i=0, resta cuando i=1
            val_real = sqrt(x_i)
            error = 100 * abs((val_real - linea.evaluar(x_i)) / val_real)
            j += 1
        intervalo.append(x_i)
    return intervalo

def print_info(n, toler, linea, intervalo):
    epsilon = abs(n - min(intervalo))
    print("\n\n===============================================================")
    print(linea)
    print("Intervalos de aprox. aceptable:")
    print("\tSimétrico desde: x = {0}, hasta: x = {1}".format( n - epsilon, n + epsilon))
    print("\tAsimétrico desde: x = {0}, hasta: x = {1}".format(min(intervalo), max(intervalo)))
    print("Tolerancia: {}".format(toler))
    print("===============================================================\n\n")


def main(argv):
    c = leer_csignif()
    toler = calc_toler(c)
    n = leer_cuadrado()
    linea = Tangente(n)
    intervalo = calc_inter_confi(n, toler, linea)
    print_info(n, toler, linea, intervalo)
    
    

if __name__ == "__main__":
    main(sys.argv)
