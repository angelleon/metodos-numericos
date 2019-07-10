import sys
from utilidades.lector_puntos import AnalizadorSintactico
from utilidades.lector_polinomios import LectorPolinomios
import utilidades.funciones as funcion


def leer_puntos(f_list: list) -> (list, list):
    x_vect = []
    y_vect = []
    for f_name in f_list:
        with open(f_name, "r") as f:
            lineas = f.read()
            an_sint = AnalizadorSintactico(lineas)
            while True:
                x_i, y_i = an_sint.punto()
                if x_i is not None:
                    x_vect.append(x_i)
                    y_vect.append(y_i)
                if an_sint.vacio:
                    break
    return x_vect, y_vect


def main(argv):
    x_vect, y_vect = leer_puntos(argv[1:])
    lec_p = LectorPolinomios()
    p = lec_p.leer_polinomio()
    suma = sum_cuadrados(p, x_vect, y_vect)
    print(x_vect, y_vect)
    print(p)
    print(suma)


def sum_cuadrados(p: funcion.Polinomio, x_vect: list, y_vect: list):
    suma = 0
    for x_i, y_i in zip(x_vect, y_vect):
        print(x_i, y_i, suma)
        suma += (p.evaluar(x_i) - y_i) ** 2
    return suma


if __name__ == "__main__":
    main(sys.argv)

