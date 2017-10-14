#!/usr/bin/python3
# -*- coding: utf8 -*-

"""

"""

from .fracciones import Fraccion
from .matriz import *


def jacobi(toler, m=Matriz(), b=Matriz()):
    if isinstance(m[0][0], Fraccion):
        tipo = Fraccion
    elif isinstance(m[0][0], (int, float)):
        tipo = float
    reng_x = []
    elem_e = []
    reng_d = []
    reng_r = []
    for i in m.m:
        reng_x.append(tipo(0))
        elem_e.append(tipo(10))
        for j in range(m.m):
            if j == i:
                reng_d.append(m[i][i])
                reng_r.append(tipo(0))
            else:
                reng_d.append(tipo(0))
                reng_r.append(m[i][j])
    d = Matriz(reng_d)
    r = Matriz(reng_r)
    x_0 = Matriz(reng_x)
    e = Renglon(elem_e)
    d_inv = d.inversa()
    x_i = None
    while e.norma() > toler:
        x_i = d_inv * (b - r * x_0)
