import textwrap
import os
import pickle
import hashlib
import string
import random
from time import time
import csv
import sympy
import math 

##########################################################################################################
############################################### BLOCKCHAIN ###############################################
##########################################################################################################

class transaction:
    
    def __init__(self, message, RSAkey):
        self.public_key = rsa_public_key(RSAkey)
        self.message = message
        self.signature = RSAkey.sign(message)


    def verify(self):
        return self.public_key.verify(self.message, self.signature)


class block:
    
    def __init__(self):
        self.block_hash = None
        self.previous_block_hash = None
        self.transaction = None
        self.seed = None


    def genesis(self,transaction):
        self.previous_block_hash = 0
        self.transaction = transaction
        self.seed = random.randrange(0,2**256)
        self.block_hash = self.create_hash()
        while not self.verify_block():
            self.seed = random.randrange(0,2**256)
            self.block_hash = self.create_hash()
        return self


    def create_hash(self):
    # genera un hash válido
        entrada=str(self.previous_block_hash)
        entrada=entrada+str(self.transaction.public_key.publicExponent)
        entrada=entrada+str(self.transaction.public_key.modulus)
        entrada=entrada+str(self.transaction.message)
        entrada=entrada+str(self.transaction.signature)
        entrada=entrada+str(self.seed)
        h=int(hashlib.sha256(entrada.encode()).hexdigest(),16)
        return h 


    def next_block(self, transaction):
    # genera un bloque v´alido seguiente al actual con la transacci´on "transaction"
        next_block = block()
        next_block.previous_block_hash = self.block_hash
        next_block.transaction = transaction
        next_block.seed = random.randrange(0,2**256)
        next_block.block_hash = next_block.create_hash()
        while not next_block.verify_block():
            next_block.seed = random.randrange(0,2**256)
            next_block.block_hash = next_block.create_hash()
        return next_block


    def next_invalid_block(self, transaction):
        """
        Genera el següent bloc invàlid amb la transacció "transaction".
        """
        next_block = block()
        next_block.previous_block_hash = int(1234)
        next_block.transaction = transaction
        next_block.seed = random.randrange(0,2**256)
        next_block.block_hash = next_block.create_hash()
        while not next_block.verify_invalid_block():
            next_block.seed = random.randrange(0,2**256)
            next_block.block_hash = next_block.create_hash()
        return next_block


    def verify_invalid_block(self):
    # Verifica si un bloque es v´alido:
    # -Comprueba que el hash del bloque cumple las condiciones exigidas
    # Salida: el booleano True si todas las comprobaciones son correctas;
    # el booleano False en cualquier otro caso.
        # comprobacion transaccion ----comprobacion bloque actual
        return (self.block_hash > 2**(256-16))


    def verify_block(self):

    # Verifica si un bloque es v´alido:
    # -Comprueba que el hash del bloque anterior cumple las condiciones exigidas
    # -Comprueba que la transacci´on del bloque es v´alida
    # -Comprueba que el hash del bloque cumple las condiciones exigidas
    # Salida: el booleano True si todas las comprobaciones son correctas;
    # el booleano False en cualquier otro caso.
        # comprobacion bloque anterior ---- comprobacion transaccion ----comprobacion bloque actual
        return (self.previous_block_hash < 2**(256-16)) and (self.transaction.verify() != True) and (self.block_hash < 2**(256-16))
        

class block_chain:
    
    def __init__(self,transaction):
    
    # genera una cadena de bloques que es una lista de bloques, el primer bloque es un bloque "genesis" generado amb la transacci´o "transaction"
        self.list_of_blocks = [block().genesis(transaction)]
    

    def add_block(self,transaction, valid):
    #a~nade a la cadena un nuevo bloque v´alido generado con la transacci´on "transaction"
        if valid:
            self.list_of_blocks.append(self.list_of_blocks[-1].next_block(transaction))
        else:
            self.list_of_blocks.append(self.list_of_blocks[-1].next_invalid_block(transaction))

    
    def verify(self):
    # verifica si la cadena de bloques es v´alida:
    # - Comprueba que todos los bloques son v´alidos
    # - Comprueba que el primer bloque es un bloque "genesis"
    # - Comprueba que para cada bloque de la cadena el siguiente es correcto
    # Salida: el booleano True si todas las comprobaciones son correctas;
    # en cualquier otro caso, el booleano False y un entero
    # correspondiente al ´ultimo bloque v´alido
    
    # verifica que todos los bloques sean validos y que el siguiente bloque es correcto
    # recorre la lista desde el final empezando por la penultima posicion
        i = 1
        for block in self.list_of_blocks[1:]:
            actual_previous = self.list_of_blocks[i].previous_block_hash
            previous = self.list_of_blocks[i-1].block_hash
            okay = (actual_previous == previous)
            if not block.verify_block() or not okay:
                return False
            i=i+1
        return True


###################################################################################################
############################################### RSA ###############################################
###################################################################################################


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


####################################################################################################
############################################### MAIN ###############################################
####################################################################################################

messages = [int(hashlib.sha256(f"Marcel y Ricard Blockchain {i}".encode()).hexdigest(), 16) for i in range(100)]


def create_comp_table():
    rounds = 10
    bits_modulo = [512, 1024, 2048, 4096]
    output = [["Bits módulo", "Segundos con TCR", "Segundos sin TCR"]]
    for modulo in bits_modulo:
        rsa = rsa_key(bits_modulo=modulo)

        time_to_sign = 0
        time_to_sign_slow = 0
        for i in range(rounds):
            start = time()
            for message in messages:
                rsa.sign(message)
            time_to_sign += time() - start

            start = time()
            for message in messages:
                rsa.sign_slow(message)
            time_to_sign_slow += time() - start
        time_to_sign /= rounds
        time_to_sign_slow /= rounds

        output.append([modulo, f'{time_to_sign:.4f}', f'{time_to_sign_slow:.4f}'])

    
    with open("comparativa.csv", 'w', newline='') as file:
        csv_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_file.writerows(output)

    print(f"La tabla comparativa se ha guardado en el archivo comparativa.csv")
    exit()



def generate_block_chain(output, limit, num_blocks):
    rsa = rsa_key()
    transactions = map(lambda i: transaction(messages[i], rsa), range(100))
    blockchain = block_chain(next(transactions))

    for i in range(1, limit):
        blockchain.add_block(next(transactions), True)

    if limit < num_blocks:
        for i in range(limit, num_blocks):
            blockchain.add_block(next(transactions), False)

    
    with open(output, 'wb') as output_file:
        pickle.dump(blockchain, output_file)

    valid = blockchain.verify()
    if valid:
        print(f"Se ha generado una Blockchain válida en el archivo {output}")
    else:
        print(f"Se ha generado una Blockchain NO válida en el archivo {output}")
    exit()



def valid_blockchain():
    print("Introduce un nombre para tu Blockchain")
    name = input()
    generate_block_chain(name, 100, 100)

def no_valid_blockchain():
    print("Introduce un nombre para tu Blockchain")
    name = input()
    generate_block_chain(name, 42, 100)

def tcr_table():
    create_comp_table()

def error():
    print("!!!!! INPUT ERROR !!!!!")


def menu():
    text = f'''\
    ****************************************************                                                                                                                                                                                       
      - 1: Crear blockchain válida                                                              
      - 2: Crear blockchain no válida
      - 3: Crear tabla comparativa sobre el TCR
                                                         
    ****************************************************
    '''
    text_f = textwrap.indent(textwrap.dedent(text), ' ' * 3)
    print("\n")
    print(text_f)

    #Possible actions
    actions = {"1": valid_blockchain, "2": no_valid_blockchain, "3": tcr_table}

    while True:
        inp = input()
        action = actions.get(inp, error)
        action()


def main():
        text=('''\
         _  .-')    .-')     ('-.     
        ( \( -O )  ( OO ).  ( OO ).-. 
        ,------. (_)---\_) / . --. / 
        |   /`. '/    _ |  | \-.  \  
        |  /  | |\  :` `..-'-'  |  |                By: Ricard Medina & Marcel Sanchez
        |  |_.' | '..`''.)\| |_.'  | 
        |  .  '.'.-._)   \ |  .-.  | 
        |  |\  \ \       / |  | |  | 
        `--' '--' `-----'  `--' `--'
        ''')
        text_f = textwrap.indent(textwrap.dedent(text), ' ' * 3)
        print(text_f)
        
        while True:
            menu()

if __name__ == '__main__':
    main()