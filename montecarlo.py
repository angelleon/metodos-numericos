#!/usr/bin/python3
# -*- coding: utf8 -*-

"""
monrtecarlo

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

import sys
import time
import logging as log
from utilidades.lectores import leer_intervalo, leer_csignif, leer_entero, leer_real
from utilidades.util import calc_toler, continuar
import utilidades.funciones as funcion
import utilidades.lector_polinomios as lec_poly
from random import random as rnd


def set_log_level(level=log.DEBUG):
    log.basicConfig(stream=sys.stderr, level=level)
    log.debug("Iniciando depuración\nArgumentos: " + str(sys.argv))


def print_lib_missing():
    print(
        """
        ===========================================================================================
        ¡¡¡ Su sistema no cuenta con las bibliotecas necesarias para graficar. !!!
    
        Para acceder a las funciones de graficación por favor instale:
    
        python3-matplotlib >= 1.5.1
    
        e intentelo de nuevo.
        ===========================================================================================""")


try:
    from matplotlib import pyplot as plot
except ImportError:
    print_lib_missing()
    plot = None


def graficar(f=funcion.Funcion(), n=2, a=0, b=1, puntos_ex=(), M=100, puntos_frac=()):
    """Método que grafica la función. Requiere puntos que luego une con rectas,
    mientras más puntos mejor la aproximación a la curva.
    """
    # ToDo: lo mismo de los otros programas de integración
    log.debug("graficar(puntos_ex={0}, puntos_frac={1}, n={2}".format(len(puntos_ex), len(puntos_frac), n))
    input("Presione <Enter> para mostrar la gráfica")
    if plot is None:
        print_lib_missing()
    else:
        if n > 1000:  # evita que la gráfica tarde mucho en procesarse
            proporcion_ex = len(puntos_ex) / n
            puntos_ex = puntos_ex[:int(1000 * proporcion_ex)]
            puntos_frac = puntos_frac[:1000-len(puntos_ex)]
            n = 1000  # el número de puntos sobre el polinomio se calculan en función del numero de puntos
        log.debug("graficando {0} puntos de exito, {1} puntos de fracaso".format(len(puntos_ex), len(puntos_frac)))
        intervalo = abs(b - a)
        trape_b = intervalo / n  # FixMe
        x_0 = a - intervalo * 0.2
        x_f = b + intervalo * 0.2
        ancho_tot = x_f - x_0
        delta_x = trape_b / 4  # los puntos sobre el polinomio son el cuadruple de los N puntos del método
        # asegura que el poligono que representa al polinomio tiene una resolución (curvatura aparente) aceptable
        x_vals = [x_0 + delta_x * i for i in range(int(ancho_tot / delta_x) + 1)]
        y_vals = [f.evaluar(x) for x in x_vals]
        max_y = max(y_vals)
        min_y = min(y_vals)
        log.debug(
            "graficando {0} puntos (x,f(x)) sobre la función\nx0 = {1}\nxf = {2}\nmin_y = {3}\nmax_y={4}".format(len(x_vals), x_0, x_f,
                                                                                               min_y, max_y))
        x_ax_pos = 0
        y_ax_pos = 0
        if not x_0 < 0 < x_f:
            if x_f < 0:
                y_ax_pos = x_f - intervalo * 0.05
            elif x_0 > 0:
                y_ax_pos = x_0 + intervalo * 0.05
        fig, ax = plot.subplots(1)
        ax.axhline(x_ax_pos, color='black')
        ax.axvline(y_ax_pos, color='black')
        ax.plot(x_vals, y_vals, color="magenta")
        ax.plot([x_0, x_f], [M, M], color="orange")
        ax.plot([a, a], [0, M], color="blue", linestyle="--")
        ax.plot([b, b], [0, M], color="blue", linestyle="--")
        for punto in puntos_ex:
            ax.scatter([punto[0]], [punto[1]], color="blue")
        for punto in puntos_frac:
            ax.scatter([punto[0]], [punto[1]], color="red")
        plot.show()
        log.debug("Grficación completa")


def print_resultados(f, area_real, area_calc, a, b, n, error, toler, t, t_proc, M, p_ex):
    print(
        "\n==========================================================================================================")
    print("Se encontró \n\u2320{0}\n|{1}{2} dx\n\u2321{3}".format(b, " " * (max((len(str(a)), len(str(b)))) + 1), f, a))
    print("Usando TFC:\n\t= {0}".format(area_real))
    print("Usando montecarlo:\n\t\u2248 {0}".format(area_calc))
    print("\tNúmero de puntos:\n\t\tN = {0}\n\t\tDe éxito: {1}".format(n, p_ex))
    print("\tCota superior: M={0}".format(M))
    print("\tTiempo empleado: {0} s".format(t))
    print("\tTimepo de procesador: {0} s".format(t_proc))
    print("Error:\n\tabsoluto: {0}\n\trelativo: {1} %".format(abs(area_real - area_calc), error))
    print("Tolerancia: {0}".format(toler))
    print(
        "==========================================================================================================\n")


def montecarlo(f=funcion.Funcion(), n=100, a=0, b=1, M=100):
    """Función que calcula n puntos, y los separa en exitos y fracasos
    media implementación del método Montecarlo, de esta forma se puede aumentar la eficiencia reduciendo el tiempo"""
    longitud = abs(b - a)
    puntos_ex = []
    puntos_frac = []
    for i in range(n):
        x_i = a + (rnd() * longitud)
        y_i = M * rnd()
        if y_i <= f.evaluar(x_i):
            puntos_ex.append([x_i, y_i])
        else:
            puntos_frac.append([x_i, y_i])
    return puntos_ex, puntos_frac


def integrar(f=funcion.Funcion(), a=0, b=1, toler=0.5, M=100, delta_n=100):
    """Función que obtiene la integral aplicando iterativamante el método Montecarlo.
    Está función implementa la mitad del método. En vez de pedir N + delta_N puntos
    en cada ciclo pide deltaN puntos y los agrega a los calculados en la interación anterior"""
    log.debug(
        "función integrar(f={0} tipo={1}, a={2} tipo={3}, b={4} tipo={5}, toler={6} tipo={7}".format(f, type(f), a,
                                                                                                     type(a), b,
                                                                                                     type(b), toler,
                                                                                                     type(toler)))
    error = toler * 2
    n = 100
    area_calc = 0
    F = f.integrar()
    log.debug("Primitiva: F={0} tipo={1}".format(F, type(F)))
    area_real = F.evaluar(b) - F.evaluar(a)
    log.debug("Valor real integral: {0}".format(area_real))
    puntos_ex = []
    puntos_frac = []
    area_rect = M * abs(b - a)
    bandera = True
    while error > toler:
        if bandera:  # primera iteración, se calculan n puntos
            puntos_ex, puntos_frac = montecarlo(f, n, a, b, M)
            bandera = False
        else:  # i-ésima iteración, se calculan deltaN puntos y se añaden a los calculados en interaciones anteriores
            p_e, p_f = montecarlo(f, delta_n, a, b, M)
            puntos_ex += p_e
            puntos_frac += p_f
        # las siguientes dos lineas se trasladarón de la función montecarlo() a aquí
        proporcion = len(puntos_ex) / n
        area_calc = area_rect * proporcion
        if area_real == area_calc:
            break
        if area_real == 0:
            area_real += toler / 10
        error = 100 * abs(area_real - area_calc) / area_real
        n += delta_n
        # if log.level
        if n % 100 == 0:
            log.debug("Valor calculado: {0}".format(area_calc))
    return area_real, area_calc, n, error, puntos_ex, puntos_frac  # devuelve los arrays con todos los puntos


def ingresar(f=None, a=None, b=None, toler=None, c_signif=None, M=None, delta_n=None):
    if f is not None:
        while True:
            answ = input(
                "¿Son correctos los datos?\n\nP(x) = {0} [{1}, {2}]\nM={3}\n\u0394N={4}\nc.s. = {5}, toler = {6}\n\n<Enter> Todo correcto\n2. Corregir\n(opción): ".format(
                    f, a, b, M, delta_n, c_signif, toler))
            if len(answ) == 0:
                return f, a, b, toler, c_signif, M, delta_n
            try:
                answ = int(answ)
            except ValueError:
                continue
            if answ == 2:
                break
    lect_func = lec_poly.LectorPolinomios()
    while True:
        f = lect_func.leer_polinomio()
        if f.grado >= 2:
            break
        else:
            print("¡ Ingrese un polinomio de grado >= 2 !")
    a, b = leer_intervalo(tag_min="a", tag_max="b")
    M = leer_real("una cota superior", "M")
    delta_n = leer_entero("aumento de N", "\u0394N")
    c_signif = leer_csignif()
    toler = calc_toler(c_signif)
    return ingresar(f, a, b, toler, c_signif, M, delta_n)


def main(argv):
    if len(argv) > 1:
        if argv[1] == "-v":
            set_log_level()
        else:
            log.warning("No se reconocen los argumentos dados\nargv: " + str(argv))
    else:
        set_log_level(log.FATAL)
    log.debug("Iniciando funcion principal")
    f, a, b, toler, c_signif, M, delta_n = ingresar()
    log.debug("Polinomio: f={0} tipo={1}".format(f, type(f)))
    print("Por favor espere\nIntegrando...")
    t_0 = time.time()
    t_0_proc = time.process_time()
    area_real, area_calc, n, error, puntos_ex, puntos_frac = integrar(f, a, b, toler, M, delta_n)
    t_proc = time.process_time() - t_0_proc
    t = time.time() - t_0
    print_resultados(f, area_real, area_calc, a, b, n, error, toler, t, t_proc, M, len(puntos_ex))
    graficar(f, n, a, b, puntos_ex, M, puntos_frac)
    continuar()


if __name__ == '__main__':
    try:
        while True:
            main(sys.argv)
    except KeyboardInterrupt:
        print("Saliendo...")






