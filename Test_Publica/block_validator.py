import os
import textwrap
import hashlib


def box():
    text = '''\
 _     _             _                    _  _     _                        
| |   | |           | |                  | |(_)   | |        _              
| |__ | | ___   ____| |  _    _   _ _____| | _  __| |_____ _| |_ ___   ____ 
|  _ \| |/ _ \ / ___) |_/ )  | | | (____ | || |/ _  (____ (_   _) _ \ / ___)
| |_) ) | |_| ( (___|  _ (    \ V // ___ | || ( (_| / ___ | | || |_| | |    
|____/ \_)___/ \____)_| \_)    \_/ \_____|\_)_|\____\_____|  \__)___/|_|
'''
    text_f = textwrap.indent(textwrap.dedent(text), ' ' * 3)
    print(text_f)

def create_hash(previous_hash, publicExponent, modulus, message, signature, seed):
    # genera un hash válido
    entrada=str(previous_hash)
    entrada=entrada+str(publicExponent)
    entrada=entrada+str(modulus)
    entrada=entrada+str(message)
    entrada=entrada+str(signature)
    entrada=entrada+str(seed)
    h=int(hashlib.sha256(entrada.encode()).hexdigest(),16)
    return h

def main():
    previous_hash = int(input("Introduce el hash del bloque previo:"))
    hash = int(input("Introduce el hash del bloque actual:"))
    seed = int(input("Introduce la seed:"))
    publicExponent = int(input("Introduce el puclicExponent:"))
    modulus = int(input("Introduce el modulo:"))
    message = int(input("Introduce el mensaje:"))
    signature = int(input("Introduce la signature:"))
    d = int(input("Introduce la dificultad:"))
    ch = int(create_hash(previous_hash, publicExponent, modulus, message, signature, seed))
    if ch != hash:
        print("hash acutal valor incorrecto")
    if not (previous_hash < 2**(256-d)):
        print("hash previo incorrecto")
    if not (hash < 2**(256-d)):
        print("hash acutal longitud incorrecta")
    if not pow(signature, publicExponent, modulus) == message:
        print("transaccion incorrecta")
    
    
    
    



if __name__ == '__main__':
    box()
    main()