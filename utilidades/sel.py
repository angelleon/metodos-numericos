from .matriz import Matriz, Renglon
from .fracciones import Fraccion


class Parametro:
    pass


class Ecuacion:
    def __init__(self, prim_miem: dict, seg_miem:dict):
        


class SEL:
    def __init__(self, ecuaciones: tuple = None, variables: tuple = None):
        self.m = 0
        self.n = 0
        if ecuaciones is not None:
            self.ecuciones = list(ecuaciones)
            self.m = len(ecuaciones)
            n = 0
            for i in ecuaciones:

        if variables is not None:
            self.variables = tuple(variables)

    def __repr__(self):
        cadena = ''

    def append(self, ecu: Ecuacion):
        self.ecuciones.append(ecu)
        self.n += 1


