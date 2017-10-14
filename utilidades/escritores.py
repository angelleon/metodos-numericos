#!/usr/bin/env python3

import sys
import __main__

__doc__ = """Módulo para escribir resultados a archivos de texto"""

class Escritor:
    def __init__(self, f_name="out.txt"):
        pass

print("Argumentos:", sys.argv[0])
print(__main__.__file__)

if __name__ == "__main__":
    print(__doc__)
