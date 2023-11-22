import random
import sympy
import math 

class rsa_key:
    
    def __init__(self,bits_modulo=2048,e=2**16+1):
        self.publicExponent = e
        self.privateExponent = None
        self.modulus = None
        self.primeP = None
        self.primeQ = None
        self.privateExponentModulusPhiP = None
        self.privateExponentModulusPhiQ = None
        self.inverseQModulusP = None


    # Generamos dos primos diferentes coprimnos con e
        while True:
            self.primeQ = sympy.randprime(2**(bits_modulo - 1), 2**bits_modulo)
            self.primeP = sympy.randprime(2**(bits_modulo - 1), 2**bits_modulo)
            different = bool(self.primeP != self.primeQ)
            coprimes = bool(math.gcd(self.publicExponent, self.primeP) == 1 and math.gcd(self.publicExponent, self.primeQ) == 1)
            if different and coprimes:
                break
        
        self.modulus = self.primeQ*self.primeP
        z = (self.primeQ - 1)*(self.primeP)

        # Calcular clave privada
        self.privateExponent = pow(e, -1, z)
        self.inverseQModulusP = pow(self.primeQ, -1, self.primeP)

        


    def sign(self,message):
    # Salida= un entero que es la firma de message hecha con la clave RSA usando el TCR
        self.privateExponentModulusPhiP = self.privateExponent % (self.primeP - 1)
        self.privateExponentModulusPhiQ = self.privateExponent % (self.primeQ - 1)

        em1 = pow(message, self.privateExponentModulusPhiP, self.primeP)
        em2 = pow(message, self.privateExponentModulusPhiQ, self.primeQ)

        firma = em1 * self.inverseQModulusP * self.primeQ + em2 * (1 - self.inverseQModulusP * self.primeQ)
        return firma % self.modulus
    
    
    def sign_slow(self,message):
    # Salida: un entero que es la firma de "message" hecha con la clave RSA sin usar el TCR
        return pow(message, self.privateExponent, self.modulus)


class rsa_public_key:
    
    def __init__(self, rsa_key):
        self.publicExponent = rsa_key.publicExponent
        self.modulus = rsa_key.modulus
    

    def verify(self, message, signature):
    # Salida: el booleano True si "signature" se corresponde con la
    # firma de "message" hecha con la clave RSA asociada a la clave
    # p´ublica RSA;
    # el booleano False en cualquier otro caso.
        return pow(signature, self.publicExponent, self.modulus) == message