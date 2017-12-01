#!/usr/bin/python3
# -*- coding: utf8 -*-

"""Modulo que define las clases Matriz y Renglon. Este archivo por si mismo no hace nada"""


from math import sqrt
from .fracciones import *
import logging
log = logging.getLogger(__name__)

if __name__ == '__main__':
    print(__doc__)
    exit(0)


class MatrizNoRectangular(Exception):
    def __str__(self):
        return str(self.args[0]) + " elementos en renglón " + str(self.args[1])


class OperacionNoDefinida(Exception):
    pass


class SumaNoDefinida(OperacionNoDefinida):
    pass


class Renglon:
    def __init__(self, elementos=None, nombre="1"):
        log.debug("Renglon(elementos={0} tipo={1})".format(elementos, type(elementos)))
        self.elementos = []
        # print(elementos, type(elementos))
        if elementos is not None and hasattr(elementos, "__len__"):
            for i in elementos:
                self.elementos.append(i)
        self.ceros_i = 0
        self.ceros_d = 0
        self.pivote = self.elementos[0]
        self.pivote_d = self.elementos[-1]
        self.__contar_ceros_izq()
        self.n = len(self.elementos)
        self.buscar_pivote()
        self.nombre = "R" + str(nombre)

    def __str__(self):
        cadena = ""
        for i in self.elementos:
            cadena += "\t" + str(i) + "\t"
        return cadena

    def __repr__(self):
        return str(self)

    def __getitem__(self, item):
        return self.elementos[item]

    def __add__(self, other):
        log.debug("Renglon.__add__(other={0} tipo={1}".format(other, type(other)))
        """Sobrecarga del operador +"""
        # print("Metodo sum reng")
        if other.n != self.n:
            raise SumaNoDefinida
        elementos = []
        for i in range(self.n):
            elementos.append(self.elementos[i] + other.elementos[i])
        self.buscar_pivote()
        return Renglon(elementos)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        """Sobrecarga del operador -"""
        # print("metodo rest reng")
        if not isinstance(other, Renglon):
            raise SumaNoDefinida
        if other.n != self.n:
            raise SumaNoDefinida
        elementos = []
        for i in range(self.n):
            elementos.append(self.elementos[i] - other.elementos[i])
        self.buscar_pivote()
        return Renglon(elementos)

    def __rsub__(self, other):
        if not isinstance(other, Renglon):
            raise SumaNoDefinida
        if other.n != self.n:
            raise SumaNoDefinida
        elementos = []
        for i in range(self.n):
            elementos.append(other.elementos[i] - self.elementos[i])
        self.buscar_pivote()
        return Renglon(elementos)

    def __mul__(self, other):
        """Sobrecarga del operador *
        en la forma
        self * other"""
        # print("Metodo mult reng")
        if isinstance(other, (int, float, Fraccion)):
            elementos = []
            for i in self.elementos:
                elementos.append(i * other)
            self.buscar_pivote()
            return Renglon(elementos)
        if isinstance(other, Renglon):
            #print("multiplicacion de objetos renglon")
            raise Exception

    def __len__(self):
        return len(self.elementos)

    def __setitem__(self, key, value):
        self.elementos[key] = value
        self.contar_ceros()

    def norma(self):
        suma = 0
        for i in self.elementos:
            suma += i ** 2
        return sqrt(float(suma))

    def buscar_pivote(self):
        self.contar_ceros()
        if self.ceros_i == self.n:
            self.pivote = 0
            return
        if self.ceros_d == self.n:
            self.pivote_d = 0
            return
        self.pivote = self.elementos[self.ceros_i]
        self.pivote_d = self.elementos[(-1) - self.ceros_d]

    def __contar_ceros_izq(self):
        cont = 0
        for i in self.elementos:
            if i == 0:
                cont += 1
            else:
                break
        self.ceros_i = cont

    def __contar_ceros_der(self):
        cont = 0
        for i in reversed(self.elementos):
            if i == 0:
                cont += 1
            else:
                break
        self.ceros_d = cont

    def contar_ceros(self):
        self.__contar_ceros_der()
        self.__contar_ceros_izq()

    def recip_pivote(self): # obsoleto al definir __rtruediv__ en Renglon
        return self.pivote.reciproco()


class Matriz:
    def __init__(self, renglones=(), renglones_indep=()):
        # ToDo: definir banderas para no llamar a métodos que ya han sido llamados
        # FixMe: actualmente reduccion_gaussiana puede ser llaamdo hasta cuatro veces con una sola llamada a un método
        self.m = len(renglones)
        if self.m != 0:
            maxi = len(renglones[0])
        else:
            maxi = 0
        for i in range(self.m):
            # print("longitud", len(renglones[i]))
            if maxi != len(renglones[i]):
                raise MatrizNoRectangular(len(renglones[i]), i+1)
        self.n = 0
        if self.m != 0:
            self.n = len(renglones[0])
        if self.m == self.n:
            self.cuadrada = True
        else:
            self.cuadrada = False
        self.renglones = []
        cont = 1
        # print(self.m)
        for i in range(self.m):
            renglones[i].nombre = 'R' + str(i)
            self.renglones.append(renglones[i])
            cont += 1
        self.reng_ident = []  # matriz (vector de renglones) que representa la parte aumentada al buscar la inversa en matrices cuadradas
        for i in range(self.m):
            r = []
            for j in range(self.n):
                if j == i:
                    r.append(1)
                else:
                    r.append(0)
            r = Renglon(r)
            self.reng_ident.append(r)
        self.escalonada = False
        self.escal_reducida = False
        self.diag_dom = False
        self.triangular = False
        self.det = None
        self.acum = None  # acumulador por el que se multiplica el determinante de
        # la matriz triangular obtenida al llamar al método reduccion_gaussiana()
        self.reng_aum = []
        if len(renglones_indep) != 0:
            self.aumentada = True
            for i in renglones_indep:
                self.reng_aum.append(i)
        else:
            self.aumentada = False
            for i in range(self.m):
                self.reng_aum.append(Renglon((0,)))
    def __str__(self):
        cadena = ''
        for i in range(self.m):
            cadena += str(self.renglones[i])
            cadena += '\n'
        return cadena

    def __repr__(self):
        cadena = '<objeto matriz\n'
        longitudes_reng = self.__long_reng()
        longitudes_aum = self.__long_reng_aum()
        longitudes_reng_ident = self.__long_reng_ident()
        for i in range(self.m):
            for j in range(self.n):
                cadena += " " * (longitudes_reng[j] - len(str(self.renglones[i][j]))) + str(self.renglones[i][j]) + " "
            if self.aumentada:
                for j in range(len(self.reng_aum[0])):
                    cadena += "|" + " " * (longitudes_aum[j] - len(str(self.reng_aum[i][j]))) + str(self.reng_aum[i][j]) + " "
            if self.cuadrada:
                cadena += "|"
                for j in range(self.n):
                    cadena +=" " * (longitudes_reng_ident[j] - len(str(self.reng_ident[i][j]))) + str(self.reng_ident[i][j]) + " "
            cadena += "\n"
        cadena += "m={0}, n={1}, cuadrada={2}, aumentada={3}>".format(self.m, self.n, self.cuadrada, self.aumentada)
        return cadena

    def __long_reng(self):
        """

        :rtype: list(int)
        """
        longitudes = [[] for j in range(self.n)]
        for i in range(self.m):
            for j in range(self.n):
                longitudes[j].append(len(str(self.renglones[i][j])))
        for j in range(len(longitudes)):
            longitudes[j] = max(longitudes[j])
        return longitudes

    def __long_reng_aum(self):
        """

        :rtype: list(int)
        """
        if not self.aumentada:
            return
        longitudes = [[] for j in range(len(self.reng_aum[0]))]
        for i in range(len(self.reng_aum)):
            for j in range(len(self.reng_aum[0])):
                longitudes[j].append(len(str(self.reng_aum[i][j])))
        for j in range(len(longitudes)):
            longitudes[j] = max(longitudes[j])
        return longitudes

    def __long_reng_ident(self):
        """

        :rtype: list(int)
        """
        if not self.cuadrada:
            return
        longitudes = [[] for j in range(self.n)]
        for i in range(self.m):
            for j in range(self.n):
                longitudes[j].append(len(str(self.reng_ident[i][j])))
        for j in range(len(longitudes)):
            longitudes[j] = max(longitudes[j])
        return longitudes


    def __getitem__(self, item):
        return self.renglones[item]

    def __setitem__(self, key, value):
        # print(key, type(key), "\t", value, type(value))
        self.renglones[key] = value

    def __len__(self):
        return len(self.renglones)

    def __mul__(self, other):
        # print(self.__repr__(), other.__repr__())
        if isinstance(other, Matriz):
            # print("multiplicacion de matrices")
            if self.n != other.m:
                raise OperacionNoDefinida
            reng = []
            for i in range(self.m):
                elementos = []
                for j in range(other.n):
                    elem = 0
                    for k in range(self.n):
                        elem = self.renglones[i][k] * other.renglones[k][j] + elem
                    elementos.append(elem)
                reng.append(Renglon(elementos))
            return Matriz(reng)
        elif isinstance(other, (int, float)):
            reng = []
            for i in range(self.m):
                elementos = []
                for j in range(self.n):
                    elementos.append(self.renglones[i][j] * other)
                reng.append(Renglon(elementos))
            return Matriz(reng)

    def __sub__(self, other):
        if not isinstance(other, Matriz):
            raise OperacionNoDefinida
        else:
            if self.m != other.m or self.n != other.n:
                raise ValueError
            reng = []
            for i in range(self.m):
                r = []
                for j in range(self.n):
                    r.append(self.renglones[i][j] - other[i][j])
                reng.append(Renglon(r))
            return Matriz(reng)

    def diag_domin(self):
        if not self.cuadrada:
            raise OperacionNoDefinida
        for i in range(self.m):
            elmnt = abs(self.renglones[i][i])
            sum = 0
            for j in range(self.n):
                if j != i:
                    if elmnt < abs(self.renglones[i][j]):
                        self.diag_dom = False
                        return False
                    sum += abs(self.renglones[i][j])
            if elmnt < sum:
                self.diag_dom = False
                return False
        self.diag_dom = True
        return True

    def append(self, renglon):
        if self.n == 0:
            self.n = len(renglon)
        else:
            if len(renglon) != self.n:
                raise MatrizNoRectangular
        self.renglones.append(renglon)
        r = []
        for j in range(self.n):
            if j == self.m:
                r.append(1)
            else:
                r.append(0)
        self.reng_ident.append(Renglon(r))
        self.m += 1
        if self.m == self.n:
            self.cuadrada = True
        else:
            self.cuadrada = False
        self.renglones[self.m-1].nombre = 'R' + str(self.m)
        self.__contar_ceros(self.m-1)

    def __contar_ceros(self, m=None):
        if m is not None:
            self.renglones[m].contar_ceros()
        else:
            for i in self.renglones:
                i.contar_ceros()
            for i in self.reng_ident:
                i.contar_ceros()

    def __ordenar(self):
        """Método que intercambia los renglones de acuerdo con los el
        número de ceros que tienen del lado izquierdo"""
        r = None
        self.__contar_ceros()
        cont = 0
        for i in range(self.m):  # bubble sort
            for j in range(self.m-i-1):
                #print(i, j)
                if self.renglones[j].ceros_i > self.renglones[j+1].ceros_i:
                    self.renglones[j], self.renglones[j+1] = self.renglones[j+1], self.renglones[j]
                    if self.cuadrada:
                        self.reng_ident[j], self.reng_ident[j+1] = self.reng_ident[j+1], self.reng_ident[j]
                    cont += 1
        return cont

    def reduccion_gaussiana(self):
        """Método que obtiene la matriz triangular superior utilizando
        operaciones elementales con renglones
        Itera desde el primer hasta el último renglón"""
        # ToDo: hacer algo para los indices incomprensibles, tal vez se puede usar self[indice][otro[indice]
        # ToDo: en vez de la llamada larga self.reng[indice][self.reng[indice].atributo]  <-- queda feo :c
        log.debug("reduccion_gaussiana()\n{0}".format(self.__repr__()))
        alfa = 1  # escalar por el que se multiplica el renglon para hacer cero el elemento debajo del pivote
        self.__contar_ceros()
        if self.cuadrada:
            cambios = self.__ordenar()  # intercambia los renglones según el número de ceros que tienen a la izquierda
            if self.acum is None:
                self.acum = (-1) ** cambios
        else:
            self.__ordenar()
        for i in range(self.m - 1):  # se pivotea sobre el i-esimo renglón
            alfa = 1 / self.renglones[i].pivote
            self.renglones[i] *= alfa
            if self.renglones[i].pivote != 1:
                log.debug("Corrigiendo pivote")
                log.debug(self.__repr__())
                self.renglones[i][self.renglones[i].ceros_i] = 1
                log.debug(self.__repr__())
            if self.cuadrada:
                self.reng_ident[i] *= alfa
            if self.aumentada:
                self.reng_aum[i] *= alfa
            if self.renglones[i].ceros_i == self.n:
                break
            for j in range(i+1, self.m): # se usa para hacer ceros desde el siguiente hasta el último
                log.debug("antes sumar reng: {}".format(self.__repr__()))
                if self.renglones[i].ceros_i == self.renglones[j].ceros_i:
                    alfa = self.renglones[i].pivote
                    alfa *= self.renglones[j].pivote * -1
                    log.debug("{0} += {1} * {2}".format(self[j], self[i], alfa))
                    self.renglones[j] += self.renglones[i] * alfa  # sumar el multiplo de un renglon a otro
                    if self.renglones[j][self.renglones[i].ceros_i] != 0:
                        """Por las restricciones de las operaciones en punto flotante
                        el elemneto debajo del pivote que se supone se hizo cero con la suma de renglones
                        puede ser un flotante muy cercano a cero, esto no afecta el algoritmo de la 
                        reducción gaussiana pero altera gauss-jordan al sumar a los pivotes
                        números que se supone deben ser cero peno no lo son"""
                        self.renglones[j][self.renglones[i].ceros_i] = 0  # asegurandose que el elemento debajo del
                        # pivote es cero
                    if self.cuadrada:
                        log.debug("{0} += {1} * {2}".format(self.reng_ident[j], self.reng_ident[i], alfa))
                        self.reng_ident[j] += self.reng_ident[i] * alfa
                        # opera sobre la matriz identidad asociada para obtener la inversa (de existir)
                    # de esta forma no se puede calcular el determinante (modificando la matriz)
                    # sin que se "pierdan" las operaciones elementales hechas en la reducción gaussiana
                    if self.aumentada:
                        self.reng_aum[j] += self.reng_aum[i] * alfa
                else:
                    break
                log.debug("despues de sum reng: {0}".format(self.__repr__()))
        log.debug("Fin reduccion_gaussiana()")

    def gauss_jordan(self):
        """Método que obtiene la matriz escalonada reducida a partir de la
        triangular superior obtenida por el método reduccion_gaussiana
        este metodo hace lo mismo que aquel pero iterando en sentido inverso"""
        # ToDo: hacer lo mismo que en reduccion_gaussiana para los flotantes cercanos a cero que deberian ser cero
        log.debug("gauss_jordan()\n{0}".format(self.__repr__()))
        self.reduccion_gaussiana()
        alfa = 1
        for i in range(self.m-1, 0, -1):
            ##if self.renglones[i].ceros_d == self.n:
            #    continue
            for j in range(i - 1, -1, -1):
                if self.renglones[i].ceros_d == self.renglones[j].ceros_d:
                    alfa = 1 / self.renglones[i].pivote_d
                    alfa *= self.renglones[j].pivote_d * -1
                    self.renglones[j] += self.renglones[i] * alfa
                    self.acum = (1 / alfa) * self.acum
                    if self.cuadrada:
                        self.reng_ident[j] += self.reng_ident[i] * alfa
                    if self.aumentada:
                        self.reng_aum[j] += self.reng_aum[i] * alfa
                    if self.renglones[j][-1 - self.renglones[i].ceros_d] != 0:
                        """Por las restricciones de las operaciones en punto flotante
                        el elemneto debajo del pivote que se supone se hizo cero con la suma de renglones
                        puede ser un flotante muy cercano a cero, esto no afecta el algoritmo de la 
                        reducción gaussiana pero altera gauss-jordan al sumar a los pivotes
                        números que se supone deben ser cero peno no lo son"""
                        self.renglones[j][-1 - self.renglones[i].ceros_d] = 0
        for i in range(self.m):
            self.__contar_ceros()
            if self.renglones[i].ceros_d != self.n:
                alfa = 1 / self.renglones[i].pivote_d
                self.renglones[i] *= alfa
                if self.cuadrada:
                    self.reng_ident[i] *= alfa
                # print(self.renglones[i], self.renglones[i].pivote_d)
                # print("pivote derecho", self.renglones[i].pivote_d)
                if self.aumentada:
                    self.reng_aum[i] *= alfa
            else:
                break

    def determinar(self):
        """Método que calcula el determinante en matrices cuadradas"""
        log.debug("determinar()\n{0}".format(self.__repr__()))
        if not self.cuadrada:
            return
        else:
            self.reduccion_gaussiana()
            if self.det is None:
                self.det = 1
                for i in range(self.m):
                    self.det = self.renglones[i][i] * self.det
                self.det *= self.acum
                self.acum = None
            return self.det

    def inversa(self):
        log.debug("inversa()\n{0}".format(self.__repr__()))
        if not self.cuadrada:
            raise OperacionNoDefinida
        self.determinar()
        if self.det != 0:
            self.gauss_jordan()
        else:
            raise OperacionNoDefinida
        reng = []
        # print(self.reng_ident)
        for i in range(self.m):
            elem = []
            for j in range(self.n):
                elem.append(self.reng_ident[i][j])
            reng.append(Renglon(elem))
        return Matriz(reng)



