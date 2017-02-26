#!/bin/env python3
# -*- coding: utf8 -*-

"""
funciones.py

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


class TipoFuncion(enumerate):
	constante = 0
	identidad = 1


class Funcion(object):
	def __init__(self, tipo, subtipo=0):
		self.tipo = tipo
		self.subtipo = subtipo

	def __str__(self):
		return "prototipo de funcion vacia"

	def derivar(self):
		pass