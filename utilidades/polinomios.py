def evaluar_poly(coef, exp, a):
    imagen = 0.0
    for i in range(len(coef)):
        imagen += coef[i] * a ** exp[i]
    return imagen


def derivar_poly(coef, exp):
    coef_deriv = []
    exp_deriv = []
    for i in range(len(coef)):
        if exp[i] - 1 < 0:
            continue
        coef_deriv.append(coef[i] * exp[i])
        exp_deriv.append(exp[i] - 1)
    return coef_deriv, exp_deriv