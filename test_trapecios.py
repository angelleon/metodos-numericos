#!/usr/bin/python3
# -*- coding: utf8 -*-

"""
test_trapecios

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

try:
    from matplotlib import pyplot as plot
    from matplotlib.collections import PatchCollection
    from matplotlib.patches import Polygon
except ImportError:
    # print_lib_missing()
    plot = None
    Rectangle = None
    PatchCollection = None


def graficar():  # ToDo: definir método graficar()
        fig, ax = plot.subplots(1)
        trap = [Polygon([[0, 0], [1, 0], [1, 2], [0, 1]], True)]
        rectang_colecc = PatchCollection(trap, facecolor='b', alpha=0.5, edgecolor="b")
        ax.axhline(0, color='black')
        ax.axvline(0, color='black')
        ax.add_collection(rectang_colecc)
        # ax.plot(x_vals, y_vals)
        plot.show()
        # log.debug("Grficación completa")

graficar()

