# suma = A^B
# multiplicacion = AES: m = 0x11B = 10001011 si estamos usando polinomio de grado siete necesitamos polinomio irreducible de grado 8. el resultado es mod m(x) B*B' = p(x) mod m(x) = r(X)
# xTime(a) = a(x)*x todos los coeficientes aumentan un grado -> si a < 128 (el bit de mas peso no es 1) a << 1, si a >= 128 nos queda un polinomio de grado 8, por lo que tenemos que dividirlo por m(x)y quedarnos con el resto 
# generadores = g != 0, 1g es generador si g^0 = 1, g^1 = g, g^2 = ... = g^254 son todos diferentes(g^255 = 1) en AES el generador es 3
# tablas = i    0   1   2 ... 254
#         g^i   1   g   gĝ 2  g^254
# hay que calcular otra tabla que se puede hacer a la vez haciendo log[g^i] = i
#
# Producto rápido = A = g^i i = log(A), B = g^j j = log(B), g^i*g^j = g^(i+j)%255, A*B= exp((log(A)+log(B))%255)
# A^-1 (A!=0) A = g^i, (g^i)^-1 = g^((-i)%255), exp(-log(A)+255) = A^-1

import numpy as np  

class G_F:
'''
Genera un cuerpo finito usando como polinomio irreducible el dado
representado como un entero. Por defecto toma el polinomio del AES.
Los elementos del cuerpo los representaremos por enteros 0<= n <= 255.
'''
    def __init__(self, Polinomio_Irreducible = 0x11B):
    '''
    Entrada: un entero que representa el polinomio para construir el cuerpo
    Tabla_EXP y Tabla_LOG dos tablas, la primera tal que en la posición
    i-ésima tenga valor a=g**i y la segunda tal que en la posición a-ésima
    tenga el valor i tal que a=g**i. (g generador del cuerpo finito
    representado por el menor entero entre 0 y 255.)
    '''
    self.Tabla_LOG

    self.Tabla_EXP = [0] * 256
    self.Tabla_LOG = [0] * 256

    # Inicializa la tabla Tabla_EXP y Tabla_LOG
    x = 1
    for i in range(256):
        self.Tabla_EXP[i] = x
        self.Tabla_LOG[x] = i
        x = self.xTimes(x)  # Calcula x^(i+1)

    def xTimes(self, n):
    '''
    Entrada: un elemento del cuerpo representado por un entero entre 0 y 255
    Salida: un elemento del cuerpo representado por un entero entre 0 y 255
    que es el producto en el cuerpo de ’n’ y 0x02 (el polinomio X).
    '''
    # Implementa la función para calcular n * 0x02 en el cuerpo finito.
    # Puedes usar el operador de desplazamiento a la izquierda (<<) para esto.
    result = n << 1
    # Verifica si el resultado es mayor que 255 y, si es así, aplica el XOR con el polinomio irreducible.
    if result > 255:
        result ^= self.Polinomio_Irreducible
    return result

    def producto(self, a, b):
    '''
    Entrada: dos elementos del cuerpo representados por enteros entre 0 y 255
    Salida: un elemento del cuerpo representado por un entero entre 0 y 255
    que es el producto en el cuerpo de la entrada.
    Atención: Se valorará la eficiencia. No es lo mismo calcularlo
    usando la definición en términos de polinomios o calcular
    usando las tablas Tabla_EXP y Tabla_LOG.
    '''
    # Implementa la función para calcular el producto de a y b en el cuerpo finito.
    # Puedes usar las tablas Tabla_EXP y Tabla_LOG para hacerlo de manera eficiente.
    if a == 0 or b == 0:
        return 0
    else:
        log_a = self.Tabla_LOG[a]
        log_b = self.Tabla_LOG[b]
        log_result = (log_a + log_b) % 255
        result = self.Tabla_EXP[log_result]
        return result

    def inverso(self, n):
    '''
    Entrada: un elementos del cuerpo representado por un entero entre 0 y 255
    Salida: 0 si la entrada es 0,
    el inverso multiplicativo de n representado por un entero entre
    1 y 255 si n <> 0.
    Atención: Se valorará la eficiencia.
    '''
    # Implementa la función para calcular el inverso multiplicativo de n en el cuerpo finito.
    if n == 0:
        return 0
    else:
        log_n = self.Tabla_LOG[n]
        log_result = 255 - log_n
        result = self.Tabla_EXP[log_result]
        return result


