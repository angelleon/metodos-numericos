from .matriz import Matriz, Renglon
from .fracciones import Fraccion

class Parametro:
    def __init__(self, c=1,  l='t', n=1, const=''):
        l = l[:1]
        self.l = l
        self.n = n
        self.c = c
        self.const = const

    def __str__(self):
        cadena = ''
        cadena += str(self.const) if str(self.const)[0] == '-' else '+' + self.const
        cadena += str(self.c) if str(self.c)[0] == '-' else '+' + str(self.c)
        cadena += self.l + str(self.n)
        return cadena

    def __mul__(self, other):
        if isinstance(other, Parametro):
            raise ValueError
        self.c *= other
        return Parametro(self.c, self.l, self.n)

    def __add__(self, other):
        self.const += str(other) if str(other)[0] == '-' else '+' + str(other)
        return Parametro(self.c, self.l, self.n, self.const)




class SEL:
    def __init__(self, m_coef=Matriz(), m_indep=Matriz(), incognitas=()):
        self.m_coef = Matriz(m_coef.renglones)
        self.m_indep = Matriz(m_indep.renglones)
        self.incognitas = []
        for i in incognitas:
            self.incognitas.append(i)

    def __str__(self):
        cadena = ''
        for i in range(self.m_coef.m):
            for j in range(self.m_coef.n):
                cadena += str(self.m_coef[i][j]) + self.incognitas[j]
            cadena += '=' + str(self.m_indep[i])
        return cadena

    def __repr__(self):
        cadena = '<objeto SEL:\n'
        cadena += self.__str__()
        cadena += '\n>'
        return cadena

    def __setitem__(self, key, value):
        self.m_coef[key] = value[0]
        self.incognitas[key] = value[1]
        self.m_indep[key] = value[2]

    def append(self, ecu):
        self.m_coef.append(ecu[0])
        self.incognitas.append(ecu[1])
        self.m_indep.append(ecu[2])

    def gauss_jordan(self):
        if self.m_coef.cuadrada:
            reng_indep = []
            m = Matriz(self.m_coef.renglones, self.m_indep.renglones)
            m.determinar()
            if m.det == 0:
                return
            else:
                return Matriz(m.reng_aum)
        """m = Matriz(self.m_coef.renglones)
        if self.m_coef.cuadrada:
            m.determinar()
            if m.det == 0:
                return
            

        reng = []
        reng_indep = []
        r = []
        r_indep = []
        for i in range(self.m_coef.m):
            for j in range(self.m_coef.n):
                r.append(self.m_coef[i][j])
            r_indep.append(self.m_indep[i])
            reng.append(Renglon(r))
            reng_indep.append(Renglon(reng_indep))
        m_aument = Matriz(renglones=reng, renglones_indep=reng_indep)
        m_aument.gauss_jordan()
        result = {}
        for incog in self.incognitas:
            result[incog] = None
        incog_libres = self.m_coef.m - self.m_coef.n
        incog = None
        cont_param = 1
        for i in reversed(range(self.m_coef.m)):
            if self.m_coef[i].ceros_i + self.m_coef[i].ceros_d == self.m_coef.n - 1:
                incog = self.incognitas[self.m_coef[i].ceros_i]
                if result[incog] is not None:
                    result[incog] = self.m_indep[self.m_coef[i].ceros_i] *( 1 / self.m_coef[i][self.m_coef[i].ceros_i])
        for i in reversed(range(self.m_coef.m)):
            if self.m_coef[i].ceros_i + self.m_coef[i].ceros_d < self.m_coef.n - 1:
                for j in range(self.m_coef[i].ceros_i, self.m_coef.n - self.m_coef[i].ceros_d):
                    if result[self.incognitas[j]] is not None:"""

    def jacobi(self, toler):
        if isinstance(m[0][0], Fraccion):
            tipo = Fraccion
        elif isinstance(m[0][0], (int, float)):
            tipo = float
        reng_x = []
        elem_e = []
        reng_d = []
        reng_r = []
        b = Matriz(self.m_indep.renglones)
        m = Matriz(self.m_coef.renglones)
        for i in m.m:
            reng_x.append(tipo(0))
            elem_e.append(tipo(10))
            for j in range(m.m):
                if j == i:
                    reng_d.append(m[i][i])
                    reng_r.append(tipo(0))
                else:
                    reng_d.append(tipo(0))
                    reng_r.append(m[i][j])
        d = Matriz(reng_d)
        r = Matriz(reng_r)
        x_0 = Matriz(reng_x)
        e = Renglon(elem_e)
        d_inv = d.inversa()
        x_i = None
        while e.norma() > toler:
            x_i = d_inv * (b - r * x_0)
            for j in range(m.n):
                e[j] = x_i[j] - x_0[j]
        return x_i
