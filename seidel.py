#!/usr/bin/python3
# -*- coding: utf8 -*-

"""

"""

import sys, time
from utilidades.util import calc_toler
from utilidades.lectores import leer_csignif
from utilidades.lector_matrices import LectorMatrices
from utilidades.matriz import Matriz, Renglon


def main(argv):
    lector = LectorMatrices(cuadrada=True, fracciones=True)
    c_signif = leer_csignif()
    tolerancia = calc_toler(c_signif)
    matriz = lector.leer_matriz()
    m_copy = Matriz(matriz.renglones)
    t_0 = []
    t_f = []
    t_proc_0 = []
    t_proc_f = []
    t_0.append(time.time())
    t_proc_0.append(time.process_time())
    matriz.determinar()
    if matriz.det == 0:
        print("La matriz no tiene inversa")
        return
    matriz = matriz.inversa()
    t_f.append(time.time())
    t_proc_f.append(time.process_time())
    matriz = Matriz(m_copy.renglones)
    matriz.diag_domin()
    if not matriz.diag_dom:
        t








if __name__ == '__main__':
    try:
        while True:
            main(sys.argv)
    except KeyboardInterrupt:
        print("Saliendo...")
        exit(0)