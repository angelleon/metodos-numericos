"""escribir un programa que lea un intervalo x0 xf y un valor c de cifras significativas
el programa aproximara pi con la presicion dada imprimira la cantidad de iteraciones
y la última aproximacion de pi"""





from utilidades.util import es_cuadrado


def leer_csignif(min=None, max=None):  # ToDo: Completar la definicion del metodo
    c = None
    while True:
        c = input("Ingrese la canidad de cifras significativas\n(c): ")
        try:
            c = int(c)
        except ValueError:
            print("\n\n¡ ¡ Ingrese un entero ! !\n\n")
            continue
        if c < 1:
            print("¡ Ingrese un número positivo !")
        elif c > 25:
            print("\nIngrese un número igual o menor a 25")
        else:
            break
    return  c


def leer_cuadrado():
    c = None
    while True:
        c = input("Ingrese un cuadrado\n(n): ")
        try:
            c = int(c)
        except ValueError:
            print("Ingrese un número")
            continue
        if not es_cuadrado(c):
            print("\n\t¡¡¡Ingrese un cuadrado perfecto!!!\n")
        else:
            break
    return c


def leer_entero(texto="(n): "):
    c = None
    while True:
        break


def leer_real(texto="(n): "):
    k = None
    while True:
        k = input(texto)
        try:
            k = float(k)
        except ValueError:
            print("\n¡ Ingrese un valor numérico !")
            continue
        break
    return k


def leer_intervalo(val_min=0, val_max=1):
    while True:
        print("Ingrese un intervalo entre {0} y {1}".format(val_min, val_max))
        x0 = leer_real("Ingrese x0\n(x0): ")
        xf = leer_real("Ingrese xf\n(xf): ")
        x0, xf = sorted((x0, xf))
        if x0 < val_min or xf > val_max:
            print("\n¡ Intervalo no valido !\n")
        else:
            break
    return x0, xf


def leer_poly():
    term = 0
    while True:
        term = input("Introduzca la cantidad de terminos\n(terminos): ")
        if term == ";":
            raise KeyboardInterrupt
        try:
            term = int(term)
        except ValueError:
            print("Introduzca un entero")
            continue
        break
    coef = []
    exp = []
    i = 0
    error = False
    while i < term:
        if error:
            coef[i] = input("Introduzca el coeficiente {}\n(coef{})".format(i+1, i))
        else:
            coef.append(input("Introduzca el coeficiente {}\n(coef{})".format(i+1, i)))
        if coef[i] == ";":
            raise KeyboardInterrupt
        try:
            num = ""
            denom = ""
            fraccion = False
            for j in range(len(coef[i])):
                #print(type(coef[i]))
                if coef[i][j] == '/':
                    fraccion = True
                    continue
                if fraccion:
                    denom += coef[i][j]
                    continue
                num += coef[i][j]
            if not fraccion:
                coef[i] = float(coef[i])
            else:
                coef[i] = float(num) / float(denom)
            error = False
        except ValueError:
            print("Ingrese un número o fracción")
            error = True
            continue
        i += 1
    i = 0
    error = False
    while i < term:
        if error:
            exp[i] = input("Ingrese el exponente del termino {}\n(exp{})".format(i+1, i+1))
        else:
            exp.append(input("Ingrese el exponente del termino {}\n(exp{})".format(i+1, i+1)))
        if coef[i] == ';':
            raise KeyboardInterrupt
        try:
            exp[i] = int(exp[i])
            error = False
        except ValueError:
            error = True
            print("Ingrese un número entero")
            continue
        i += 1
    return coef, exp




