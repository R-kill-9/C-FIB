import os
import random
import hashlib
from rsa import rsa_public_key



class transaction:
    
    def __init__(self, message, RSAkey):
        self.public_key = rsa_public_key(rsa_key)
        self.message = message
        self.signature = rsa_key.sign(message)


    def verify(self):
    '''
    Salida: el booleano True si "signature" se corresponde con la
    firma de "message" hecha con la clave RSA asociada a la clave
    p´ublica RSA;
    el booleano False en cualquier otro caso.
    '''
        return self.public_key.verify(self.message, self.signature)


class block:
    
    def __init__(self):
        self.block_hash
        self.previous_block_hash
        self.transaction
        self.seed

    
    def create_hash(self):
    '''genera un hash válido'''
        entrada=str(self.previous_block_hash)
        entrada=entrada+str(self.transaction.public_key.publicExponent)
        entrada=entrada+str(self.transaction.public_key.modulus)
        entrada=entrada+str(self.transaction.message)
        entrada=entrada+str(self.transaction.signature)
        entrada=entrada+str(seed)
        h=int(hashlib.sha256(entrada.encode()).hexdigest(),16)


    def genesis(self,transaction):
    '''
    genera el primer bloque de una cadena con la transacci´on "transaction"
    que se caracteriza por:
    - previous_block_hash=0
    - ser v´alido
    '''
    self.previous_block_hash = 0
    self.transaction = transaction
    self.seed = random.randrange(0,2**256)
    self.block_hash = self.create_hash()
    while not self.verify_block():
        self.seed = random.randrange(0,2**256)
        self.block_hash = self.create_hash()
    return self

    
    def next_block(self, transaction):
    '''
    genera un bloque v´alido seguiente al actual con la transacci´on "transaction"
    '''
        next_block = block()
        next_block.previous_block_hash = self.block_hash
        next_block.transaction = transaction
        next_block.seed = random.randrange(0,2**256)
        next_block.block_hash = next_block.create_hash()
        while not next_block.verify_block():
            next_block.seed = random.randrange(0,2**256)
            next_block.block_hash = next_block.create_hash()
        return next_block

    
    def verify_block(self):
    '''
    Verifica si un bloque es v´alido:
    -Comprueba que el hash del bloque anterior cumple las condiciones exigidas
    -Comprueba que la transacci´on del bloque es v´alida
    -Comprueba que el hash del bloque cumple las condiciones exigidas
    Salida: el booleano True si todas las comprobaciones son correctas;
    el booleano False en cualquier otro caso.
    '''
        # comprobacion bloque anterior
        assert self.previous_block_hash < 2**(256-16), "El hash del bloque anterior no cumple las condiciones exigidas"
        # comprobacion bloque actual
        assert self.transaction.verify() != True, "El hash del bloque no cumple las condiciones exigidas"
        # comprobacion bloque actual
        assert self.block_hash < 2**(256-16), "El hash del bloque no cumple las condiciones exigidas"


    def is_genesis(self):
        return previous_block_hash == 0


    def return_hash(self):
        return self.block_hash

class block_chain:
    
    def __init__(self,transaction):
    '''
    genera una cadena de bloques que es una lista de bloques,
    el primer bloque es un bloque "genesis" generado amb la transacci´o "transaction"
    '''
        
    
    
    def add_block(self,transaction):
    '''
    a~nade a la cadena un nuevo bloque v´alido generado con la transacci´on "transaction"
    '''
        self.list_of_blocks.append(self.list_of_blocks[-1].next_block(transaction))
    
    
    def verify(self):
    '''
    verifica si la cadena de bloques es v´alida:
    - Comprueba que todos los bloques son v´alidos
    - Comprueba que el primer bloque es un bloque "genesis"
    - Comprueba que para cada bloque de la cadena el siguiente es correcto
    Salida: el booleano True si todas las comprobaciones son correctas;
    en cualquier otro caso, el booleano False y un entero
    correspondiente al ´ultimo bloque v´alido
    '''
    # verifica que todos los bloques sean validos y que el siguiente bloque es correcto
    # recorre la lista desde el final empezando por la penultima posicion
        esperado = self.list_of_blocks[-2].return_hash()
        for i, block in range(reversed(self.list_of_blocks), 0, -1):
            block.verify()
            hash = block.return_hash()
            assert hash != esperado
            esperado = self.list_of_blocks[-1-i].return_hash()
        self.list_of_blocks[0].verify()
        self.list_of_blocks[-1].verify()
        return True

        # verifica que el primer bloque es genesis
        assert self.list_of_blocks[0].is_genesis != True, "el primer bloque NO es un bloque genesis"
        return True
