import os

class G_F:
#0x1f3

    def __init__(self, Polinomio_Irreducible = 0x11b):#cambiar polinomio irreducile(antes 0x1f3)


        self.Polinomio_Irreducible = Polinomio_Irreducible
        self.Tabla_EXP = [0] * 256
        self.Tabla_LOG = [0] * 256
        self.generar_tablas()

    def generar_tablas(self):
        g = 0x02  # Generador del cuerpo finito
        elemento = 0x01
        for i in range(256):
            self.Tabla_EXP[i] = elemento
            self.Tabla_LOG[elemento] = i
            elemento = self.xTimes(elemento)


    def xTimes(self, n):
        result = n << 1
        if result > 255:
            result ^= self.Polinomio_Irreducible
        return result

    def producto(self, a, b):   
       p= 0
       while a and b:
              if b & 1:
                p ^= a
              b >>= 1
              a = self.xTimes(a)
       return p
    

    def inverso(self, n):
        if n == 0:
            return 0
        return self.Tabla_EXP[255 - self.Tabla_LOG[n]]
    
    

gf = G_F()
print("El resultado del producto es: "+str(gf.producto(0x44, 0x05))) 
invers=gf.inverso(0x033)
print("El resultado del inverso en decimal es: "+str(invers)+", en hexadecimal: "+str(hex(invers))) 