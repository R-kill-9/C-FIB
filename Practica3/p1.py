from blockchain import block, block_chain, transaction
from rsa import rsa_key, rsa_public_key
import textwrap
import os
import pickle
import hashlib
import string
import random


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join((random.choice(letters_and_digits) for _ in range(length)))


messages = [int(hashlib.sha256(get_random_alphanumeric_string(20).encode()).hexdigest(), 16) for _ in range(100)]


def create_comp_table():
    print("Iniciando la comparación entre la firma con TXR y sin TXR.")

    rounds = 10
    bits_modulo = [512, 1024, 2048, 4096]
    output = [["Bits módulo", "Tiempo usando TXR (s)", "Tiempo sin usar TXR (s)"]]
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

    Path(output_folder).mkdir(exist_ok=True)
    output_path = os.path.join(output_folder, "tabla_comparativa.csv")
    with open(output_path, 'w', newline='') as file:
        csv_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_file.writerows(output)

    print(f"Se ha creado el fichero {output_path}")



def generate_block_chain(output, limit, num_blocks):
    rsa = rsa_key()
    transactions = map(lambda i: transaction(messages[i], rsa), range(100))
    blockchain = block_chain(next(transactions))

    for i in range(1, limit):
        blockchain.add_block(next(transactions))

    if limit < num_blocks:
        for i in range(limit, num_blocks):
            blockchain.add_wrong_block(next(transactions))
            print(f'Invalid block {i} created')

    
    with open(output, 'wb') as output_file:
        pickle.dump(blockchain, output_file)

    valid, idx = blockchain.verify()
    if valid:
        print(f"Se ha generado una Blockchain válida en el archivo {output}")
    else:
        print(f"Se ha creado el fichero {output}.\n"
              f"El Blockchain es válido hasta el bloque {idx} de {num_blocks}.")
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