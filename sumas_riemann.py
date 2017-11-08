#!/usr/bin/python3
# -*- coding: utf8 -*-

"""
sumas_riemann.py

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
import utilidades.funciones as funcion  # modulo que define clases que representan funciones elementales
import utilidades.lector_polinomios as lec_poly  # modulo que convierte entrada de texto en polinomios del modulo funciones


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
    from matplotlib.patches import Rectangle
except ImportError:
    print_lib_missing()
    plot = None
    Rectangle = None
    PatchCollection = None


def graficar(f=funcion.Funcion(), n=2, a=0, b=1):  # ToDo: renombrar las variables delta_x y rect_b para que coincidan con el cambio en x para graficar la curva y el ancho del rectangulo respectivamente
    """Método que grafica la función. Requiere puntos que luego une con rectas,
    mientras más puntos mejor la aproximación a la curva.
    """
    input("Presione <Enter> para mostrar la gráfica")
    if plot is None or Rectangle is None or PatchCollection is None:
        print_lib_missing()
    else:
        intervalo = abs(b-a)
        rectang_b = intervalo / n  # base del rectangulo
        # ToDo: modificar el orden de las sentencias para que todo quede en terminos de delta_x
        x_0 = a - intervalo * 0.2
        x_f = b + intervalo * 0.2
        ancho = x_f - x_0
        delta_x = rectang_b / 4
        # el polinomio se grafica como un poligono de el cuadruple de rectangulos
        # asegura que el poligono que representa al polinomio tiene una resolución (curvatura aparente) aceptable
        x_vals = [x_0 + delta_x * i for i in range(int(ancho / delta_x) + 1)]  # absicsas de puntos sobre el polinomio
        y_vals = [f.evaluar(x) for x in x_vals]  # ordenadas de puntos sobre el polinomio
        max_y = max(y_vals)
        min_y = min(y_vals)
        log.debug("graficando {0}puntos (x,f(x))\nx0 = {1}\nxf = {2}\nmin_y = {3}\nmax_y={4}".format(len(x_vals), x_0, x_f, min_y, max_y))
        x_ax_pos = 0
        y_ax_pos = 0
        if not x_0 < 0 < x_f:
            if x_f < 0:
                y_ax_pos = x_f - intervalo * 0.05
            elif x_0 > 0:
                y_ax_pos = x_0 + intervalo * 0.05
        rectang_pb_x = []  # puntos base de los rectangulos
        rectang_h = []  # altura del rectangulo, f evaluada en el punto medio
        rectang = []
        for i in range(n):
            rectang_pb_x.append(a + rectang_b * i)
            rectang_h.append(f.evaluar(rectang_pb_x[i] + rectang_b / 2))  # f evaluada en el punto medio del subintervalo
            rectang.append(Rectangle((rectang_pb_x[i], 0), rectang_b, rectang_h[i], angle=0.0))
        fig, ax = plot.subplots(1)
        rectang_colecc = PatchCollection(rectang, facecolor='b', alpha=0.5, edgecolor="b")
        ax.axhline(x_ax_pos, color='black')
        ax.axvline(y_ax_pos, color='black')
        ax.add_collection(rectang_colecc)
        ax.plot(x_vals, y_vals, color="magenta")
        plot.show()
        log.debug("Grficación completa")


def print_resultados(f, area_real, area_calc, a, b, n, error, toler, t, t_proc):
    print("\n==========================================================================================================")
    print("Se encontró \n\u2320{0}\n|{1}{2} dx\n\u2321{3}".format(b, " " * (max((len(str(a)), len(str(b)))) + 1), f, a))
    print("Usando TFC:\n\t= {0}".format(area_real))
    print("Usando rectangulos:\n\t\u2248 {0}".format(area_calc))
    print("\tNúmero de rectangulos: {0}".format(n))
    print("\tTiempo empleado: {0} s".format(t))
    print("\tTimepo de procesador: {0} s".format(t_proc))
    print("Error:\n\tabsoluto: {0}\n\trelativo: {1} %".format(abs(area_real - area_calc), error))
    print("Tolerancia: {0}".format(toler))
    print("==========================================================================================================\n")


def riemann(f=funcion.Funcion(), n=2, a=0, b=1):
    """Función que implementa sumas de Riemann en el centro del subintervalo"""
    delta_x = abs(b - a) / n
    area = 0
    for i in range(n):
        area += f.evaluar(a + delta_x * i + delta_x / 2)  # evalua en el punto medio del intervalo
        # ToDo: asignar delta_x / 2 a una variable para no calcularla en cada ciclo
    return area * delta_x


def integrar(f=funcion.Funcion(), a=0, b=1, toler=0.5):
    """Función que obtiene el valor de la integral mediante la aplicación iterativa de sumas de Riemann"""
    log.debug("función integrar(f={0} tipo={1}, a={2} tipo={3}, b={4} tipo={5}, toler={6} tipo={7}".format(f, type(f), a, type(a), b, type(b), toler, type(toler)))
    error = toler * 2
    n = 1
    area_calc = 0
    F = f.integrar()  # primitiva del polinomio
    log.debug("Primitiva: F={0} tipo={1}".format(F, type(F)))
    area_real = F.evaluar(b) - F.evaluar(a)
    log.debug("Valor real integral: {0}".format(area_real))
    while error > toler:
        area_calc = riemann(f, n, a, b)
        if area_real == area_calc:
            break
        if area_real == 0:  # evitar ZeroDivisionError
            area_real += toler / 10
        error = 100 * abs(area_real - area_calc) / area_real
        n += 1
        # if log.level
        # if n % 1000 == 0:
            # log.debug("Valor calculado: {0}".format(area_calc))
    return area_real, area_calc, n, error


def ingresar(f=None, a=None, b=None, toler=None, c_signif=None):
    """Función recursiva para ingresar los datos"""
    if f is not None:
        while True:
            answ = input("¿Son correctos los datos?\n\nP(x) = {0} [{1}, {2}]\nc.s. = {3}, toler = {4}\n\n<Enter> Todo correcto\n2. Corregir\n(opción): ".format(f, a, b, c_signif, toler))
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



