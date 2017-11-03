#!/usr/bin/python3
# -*- coding: utf8 -*-

"""

"""

import sys, time
from utilidades.util import calc_toler
from utilidades.lectores import leer_csignif
from utilidades.lector_matrices import LectorMatrices
from utilidades.matriz import Matriz, Renglon
from utilidades.lector_sel import LectorSEL


def main(argv):
    lector = LectorSEL(cuadrado=False, fracciones=False)
    c_signif = leer_csignif()
    tolerancia = calc_toler(c_signif)
    sel = lector.leer_sel()
    matriz = Matriz(sel.m_coef.renglones)
    b = Matriz(sel.m_indep.renglones)
    t_0 = []
    t_f = []
    t_proc_0 = []
    t_proc_f = []
    t_0.append(time.time())
    t_proc_0.append(time.process_time())
    v_incog = sel.gauss_jordan()
    t_proc_f.append(time.process_time())
    t_f.append(time.time())
    if not matriz.diag_dom:
        input("""
===============================================================================

A la matriz ingresada no se le pueden aplicar los métodos de Jacobi o Gauss-Seidel
================================================================================

Presione enter para continuar""")
    else:
        sel.m_coef = Matriz(matriz.renglones)
        sel.m_indep = Matriz(b.renglones)
        t_0.append(time.time())
        t_proc_0.append(time.process_time())
        sel.jacobi(tolerancia)
        t_proc_f.append(time.process_time())
        t_f.append(time.time())
    for i in v_incog:
        print(i)











if __name__ == '__main__':
    try:
        while True:
            main(sys.argv)
    except KeyboardInterrupt:
        print("Saliendo...")
        exit(0)