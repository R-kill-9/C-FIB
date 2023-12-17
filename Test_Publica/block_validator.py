import os
import textwrap


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


def main():
    previous_hash = int(input("Introduce el hash del bloque previo:"))
    hash = int(input("Introduce el hash del bloque actual:"))
    seed = int(input("Introduce la seed:"))
    publicExponent = int(input("Introduce el puclicExponent:"))
    modulus = int(input("Introduce el modulo:"))
    message = int(input("Introduce el mensaje:"))
    signature = int(input("Introduce la signature:"))
    d = int(input("Introduce la dificultad:"))

    if not (previous_hash < 2**(256-d)):
        print("hash previo incorrecto")
    if not (hash < 2**(256-d)):
        print("hash acutal incorrecto")
    if not pow(signature, publicExponent, modulus) == message:
        print("transaccion incorrecta")
    
    
    
    



if __name__ == '__main__':
    box()
    main()