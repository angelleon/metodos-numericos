#!/usr/bin/env python3

import sys
import time
from math import sqrt, pi


class Euler:
    def __init__(self):
        self.f = None
        self.f_path = None


def write_2f(f, k, pi_aprox):
    if f is None:
        raise Exception #  Especificar excepcion para puntero nulo
    f.write(str(k) + '\t' + str(pi_aprox) + "\n")
        

def leer_csignif():
    c = None
    while True:
        c = input("Ingrese la cantidad de cifras significativas\n(c): ")
        try:
            c = int(c)
            if c < 1:
                raise ValueError
            else:
                break
        except ValueError:
            print("\nIngrese un entero mayor que cero")
    return c


def calc_toler(c_signif):
    return 0.5 * 10 ** (2 - c_signif)
    

def euler(tolerancia, f):
    #print(tolerancia)
    k = 1
    error = tolerancia * 2
    pi_aprox = pi_anter = 0.0
    #pi_anter = pi
    suma = 0
    try:
        while error > tolerancia:
            suma += 1.0 / (k ** 2)
            pi_anter = pi_aprox
            pi_aprox = sqrt(6 * suma)
            #error = abs((pi_aprox - pi_anter) / pi_aprox) * 100
            error = abs((pi - pi_aprox) / pi) * 100
            write_2f(f, k, pi_aprox)
            k += 1
    except KeyboardInterrupt:
        print("\n\n*****************************************************")
        print("\t¡ ¡ ¡ Proceso interrumpido ! ! !")
        print("*****************************************************\n\n")
    return pi_aprox, error, int(k)
    

def print_info(pi_aprox, k, error, t_seg, t_proc, c_signif):
    #t_seg *= 1000
    #t_proc *= 1000
    print("\n\n===========================================================================")
    print("Valor calculado: {}".format(pi_aprox))
    print("Tolerancia: {}".format(calc_toler(c_signif)))
    print("Error: {0}".format(error))
    print("Iteraciones: {0:d}".format(k))
    print("Timepo empleado: {0} min {1:.3f} seg".format(int(t_seg // 60), t_seg % 60))
    print("Tiempo empleado (procesador): {0} min {1:.3f} seg".format(int(t_proc // 60), t_proc % 60))
    print("===========================================================================\n\n")
        

def main(argv):
    f = None
    f_name = "EULER.TXT"
    ruta = "./"
    if len(argv) == 2:
        ruta = argv[1]
    try:
        f = open(ruta + f_name, "w")
    except PermissionError as e:
        print(e)
        print("No se pudo abrir el archivo " + ruta + f_name + " en modo escritura")
        exit()
    c_signif = leer_csignif()
    tolerancia = calc_toler(c_signif)
    
    inicio_seg = time.time()
    inicio_proc = time.process_time()
    
    pi_aprox, error, k = euler(tolerancia, f)
    
    tiempo_proc = time.process_time() - inicio_proc
    tiempo_seg = time.time()- inicio_seg
    f.close()

    print_info(pi_aprox, k, error, tiempo_seg, tiempo_proc, c_signif)
    
    
if __name__ == "__main__":
    main(sys.argv)
