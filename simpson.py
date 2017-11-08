#!/usr/bin/python3
# -*- coding: utf8 -*-

"""
simpson

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
from utilidades.lectores import leer_intervalo, leer_csignif
from utilidades.util import calc_toler, continuar
import utilidades.funciones as funcion
import utilidades.lector_polinomios as lec_poly
from utilidades.matriz import Matriz, Renglon


def set_log_level(level=log.DEBUG):
    log.basicConfig(stream=sys.stderr, level=level)
    log.debug("Iniciando depuración\nArgumentos: " + str(sys.argv))


def print_lib_missing():
    print(
        """
        ===========================================================================================
        ¡¡¡ Su sistema no cuenta con las bibliotecas necesarias para graficar. !!!

        Para acceder a las funciones de graficación por favor instale:

        python3-mathplotlib >= 1.5.1

        e intentelo de nuevo.
        ===========================================================================================""")


try:
    from matplotlib import pyplot as plot
    from matplotlib.collections import PatchCollection
    from matplotlib.patches import Polygon
except ImportError:
    print_lib_missing()
    plot = None
    Polygon = None
    PatchCollection = None


def graficar(f=funcion.Funcion(), n=2, a=0, b=1):  # ToDo: definir método graficar()
    """Método que grafica la función. Requiere puntos que luego une con rectas,
    mientras más puntos mejor la aproximación a la curva.
    Las tapas de las figuras se grafican resolviendo el SEL asociado a los tres puntos por los que pasa la parabola
    """
    input("Presione <Enter> para mostrar la gráfica")
    if plot is None or Polygon is None or PatchCollection is None:
        print_lib_missing()
    else:
        intervalo = abs(b - a)
        fig_b = intervalo / n
        x_0 = a - intervalo * 0.2
        x_f = b + intervalo * 0.2
        ancho_tot = x_f - x_0
        delta_x = fig_b / 4  # FixMe: tal vez es necesario un valor mayor que 4 por las pocas figuras que requiere simpson
        # asegura que el poligono que representa al polinomio tiene una resolución (curvatura aparente) aceptable
        x_vals = [x_0 + delta_x * i for i in range(int(ancho_tot / delta_x) + 1)]
        y_vals = [f.evaluar(x) for x in x_vals]
        max_y = max(y_vals)
        min_y = min(y_vals)
        log.debug(
            "graficando {0}puntos (x,f(x))\nx0 = {1}\nxf = {2}\nmin_y = {3}\nmax_y={4}".format(len(x_vals), x_0, x_f,
                                                                                               min_y, max_y))
        x_ax_pos = 0
        y_ax_pos = 0
        if not x_0 < 0 < x_f:
            if x_f < 0:
                y_ax_pos = x_f - intervalo * 0.05
            elif x_0 > 0:
                y_ax_pos = x_0 + intervalo * 0.05
        base_coord = []
        base_coord.append([[a, f.evaluar(a)], [a, 0], [a + fig_b * 2, 0], [a + fig_b * 2, f.evaluar(a + fig_b * 2)]])
        cont = 0
        for i in range(2, n, 2):
            b_ant = base_coord[cont - 1]
            x_i = a + fig_b * i
            base_coord.append([[b_ant[3][0], b_ant[3][1]], [b_ant[2][0], 0], [x_i + fig_b * 2, 0], [x_i + fig_b * 2, f.evaluar(x_i + fig_b * 2)]])
            cont += 1
        tapa_coord = []
        for i in range(0, n, 2):
            reng = []
            m_b = []
            for j in range(i, i + 3):
                x_i = a + fig_b * j
                reng.append(Renglon((x_i ** 2, x_i, 1)))
                m_b.append(Renglon((f.evaluar(x_i),)))
            m_b = Matriz(m_b)
            log.debug("m_b={0}".format(m_b))
            m_a = Matriz(reng)
            log.debug("m_a={0}".format(repr(m_a)))
            m_a_inv = m_a.inversa()
            log.debug("m_a_inv = {0}".format(repr(m_a_inv)))
            m_x = m_a_inv * m_b  # resolución del SEL de los puntos por los que pasa la parabola
            log.debug("m_x={0}".format(repr(m_x)))
            p = funcion.Polinomio(coeficientes=(m_x[0][0], m_x[1][0], m_x[2][0]), exponentes=(2, 1, 0))
            log.debug("Tapa: p={0}".format(p))
            delta_x = fig_b / 20
            tapa = []
            for j in range(40):
                x_i = a + fig_b * i + delta_x * j
                tapa.append([x_i, p.evaluar(x_i)])
            tapa_coord.append(tapa)
        fig_coord = []
        for i in range(len(base_coord)):
            fig_coord.append(base_coord[i] + tapa_coord[i][::-1])
        log.debug("fig_coord={0}".format(fig_coord))
        figuras = []
        for coord in fig_coord:
            figuras.append(Polygon(coord, True))
        figuras_colecc = PatchCollection(figuras, facecolor='b', alpha=0.5, edgecolor="b")
        fig, ax = plot.subplots(1)
        for i in range(1, n, 2):
            x_i = a + fig_b * i
            ax.plot([x_i, x_i], [0, f.evaluar(x_i)], color="b", linestyle=":")
        ax.axhline(x_ax_pos, color='black')
        ax.axvline(y_ax_pos, color='black')
        ax.add_collection(figuras_colecc)
        ax.plot(x_vals, y_vals, color="magenta")
        plot.show()
        log.debug("Grficación completa")


def print_resultados(f, area_real, area_calc, a, b, n, error, toler, t, t_proc):
    print(
        "\n==========================================================================================================")
    print("Se encontró \n\u2320{0}\n|{1}{2} dx\n\u2321{3}".format(b, " " * (max((len(str(a)), len(str(b)))) + 1), f, a))
    print("Usando TFC:\n\t= {0}".format(area_real))
    print("Usando Simpson:\n\t\u2248 {0}".format(area_calc))
    print("\tNúmero de figuras: {0}".format(n // 2))
    print("\tTiempo empleado: {0} s".format(t))
    print("\tTimepo de procesador: {0} s".format(t_proc))
    print("Error:\n\tabsoluto: {0}\n\trelativo: {1} %".format(abs(area_real - area_calc), error))
    print("Tolerancia: {0}".format(toler))
    print(
        "==========================================================================================================\n")


def simpson(f=funcion.Funcion(), n=2, a=0, b=1):
    """Función que implementa el método de Simpson"""
    if n % 2 != 0:
        raise ValueError
    delta_x = abs(b - a) / n
    area = 0
    pares = 0
    impares = 0
    for i in range(1, n):
        if i % 2 != 0:
            impares += f.evaluar(a + delta_x * i)
        else:
            pares += f.evaluar(a + delta_x * i)
    area += f.evaluar(a)
    area += f.evaluar(b)
    area += 4 * impares
    area += 2 * pares
    return area * delta_x / 3


def integrar(f=funcion.Funcion(), a=0, b=1, toler=0.5):
    """Función que obtiene la integral mediante la aplicación iterativa del métod de Simpson"""
    log.debug(
        "función integrar(f={0} tipo={1}, a={2} tipo={3}, b={4} tipo={5}, toler={6} tipo={7}".format(f, type(f), a,
                                                                                                     type(a), b,
                                                                                                     type(b), toler,
                                                                                                     type(toler)))
    error = toler * 2
    n = 2
    area_calc = 0
    F = f.integrar()
    log.debug("Primitiva: F={0} tipo={1}".format(F, type(F)))
    area_real = F.evaluar(b) - F.evaluar(a)
    log.debug("Valor real integral: {0}".format(area_real))
    while error > toler:
        area_calc = simpson(f, n, a, b)
        if area_real == area_calc:
            break
        if area_real == 0:
            area_real += toler / 10
        error = 100 * abs(area_real - area_calc) / area_real
        n += 2
        # if log.level
        if n % 100 == 0:
            log.debug("Valor calculado: {0}".format(area_calc))
    return area_real, area_calc, n, error


def ingresar(f=None, a=None, b=None, toler=None, c_signif=None):
    """Función recursiva para el ingreso de datos"""
    if f is not None:
        while True:
            answ = input(
                "¿Son correctos los datos?\n\nP(x) = {0} [{1}, {2}]\nc.s. = {3}, toler = {4}\n\n<Enter> Todo correcto\n2. Corregir\n(opción): ".format(
                    f, a, b, c_signif, toler))
            if len(answ) == 0:  # caso base de la recursividad
                return f, a, b, toler, c_signif
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
    c_signif = leer_csignif()
    toler = calc_toler(c_signif)
    return ingresar(f, a, b, toler, c_signif)


def main(argv):
    if len(argv) > 1:
        if argv[1] == "-v":
            set_log_level()
        else:
            log.warning("No se reconocen los argumentos dados\nargv: " + str(argv))
    else:
        set_log_level(log.FATAL)
    log.debug("Iniciando funcion principal")
    f, a, b, toler, c_signif = ingresar()
    log.debug("Polinomio: f={0} tipo={1}".format(f, type(f)))
    print("Por favor espere\nIntegrando...")
    t_0 = time.time()
    t_0_proc = time.process_time()
    area_real, area_calc, n, error = integrar(f, a, b, toler)  # obtención de la integral
    t_proc = time.process_time() - t_0_proc
    t = time.time() - t_0
    print_resultados(f, area_real, area_calc, a, b, n, error, toler, t, t_proc)  # impresión de resultados
    graficar(f, n, a, b)
    continuar()


if __name__ == '__main__':
    try:
        while True:
            main(sys.argv)
    except KeyboardInterrupt:
        print("Saliendo...")
