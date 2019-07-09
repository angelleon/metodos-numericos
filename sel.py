#!/usr/bin/python3
# -*- coding: utf8 -*-

"""
sel

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

from utilidades.lector_sel import LectorSEL
import time
import logging

logging.basicConfig(level=logging.DEBUG)


def leer_sel():
    lector = LectorSEL()
    sel = lector.leer_sel()
    return sel


def main():
    sel = leer_sel()
    raise KeyboardInterrupt
    t_0 = time.time()
    t_0_proc = time.process_time()
    solucion = sel.resolver()
    t_f_proc = time.process_time()
    t_f = time.time()
    t = t_f - t_0
    t_proc = t_f_proc - t_0_proc
    print_resultados(solucion, t, t_proc)


if __name__ == "__main__":
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("\nSaliendo...")
