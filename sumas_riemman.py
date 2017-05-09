#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
sumas_riemman.py 

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

import os
from lector_polinomios import *

def sumas_riemman(poly, a, b, error, tolerancia):
	#acum = 0
	n = 10
	delt_x = abs(b - a) / n
	while error > tolerancia:
		acum = 0
		for i in range(n):
			for j in poly:
				acum += j.evaluar(a + delt_x * i)



def main():
	poly = leer_poly()
	cifras_sig = leer_cif_sig()
	interv = leer_interv()
	integ_real = poly.integrar(interv[0], interv[1])
	sumas_riemman(poly)



