from blockchain import block, block_chain, transaction
from rsa import rsa_key, rsa_public_key
import textwrap
import os
import pickle
import hashlib
import string
import random
from time import time
import csv


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
            print(i)
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