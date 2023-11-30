import os
import random
import hashlib
from rsa import rsa_public_key



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
        print("verified")
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
