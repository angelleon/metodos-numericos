import sys

from utilidades.lector_matrices import LectorMatrices


def preguntar_usar_fracciones():
    while True:
        answ = input("""
        Desea usar Fracciones (por defecto Sí)\n1\tSí\n2\tNo\n3\tSalir\n(opción): """)
        try:
            answ = int(answ)
        except ValueError:
            if len(answ) == 0:
                return True
            continue
        if answ == 1:
            return True
        elif answ == 2:
            return False
        elif answ == 3:
            raise KeyboardInterrupt


def main(argv):
    f = preguntar_usar_fracciones()
    lector = LectorMatrices(cuadrada=True, fracciones=f)
    matriz = lector.leer_matriz()
    lector = LectorMatrices(cuadrada=False, fracciones=f)
    x = lector.leer_matriz()
    matriz.determinar()
    if matriz.det == 0:
        print("La matriz no tiene inversa")
    else:
        matriz = matriz.inversa()
        print("Se encontró la inversa de la matriz A como A^-1 = \n\n")
        print(matriz)
        print("Solucion del sistema:\n")
        print(matriz * x)


if __name__ == '__main__':
    while True:
        try:
                main(sys.argv)
        except KeyboardInterrupt:
            print("\n\nSaliendo...")
            break
        except Exception:
            raise
