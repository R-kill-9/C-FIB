import * from blockchain
import * from rsa
import textwrap
import os

exit_flag = False

def generate_block_chain(output, limit=100, num_blocks=100):
    rsa = rsa_key()
    transactions = map(lambda i: transaction(messages[i], rsa), range(100))
    blockchain = block_chain(next(transactions))
    print(f'Block 0 created')

    for i in range(1, limit):
        blockchain.add_block(next(transactions))
        print(f'Block {i} created')

    if limit < num_blocks:
        for i in range(limit, num_blocks):
            blockchain.add_wrong_block(next(transactions))
            print(f'Invalid block {i} created')

    Path(output_folder).mkdir(exist_ok=True)
    output_path = os.path.join(output_folder, output)
    with open(output_path, 'wb') as output_file:
        pickle.dump(blockchain, output_file)

    valid, idx = blockchain.verify()
    if valid:
        print(f"Se ha creado el fichero {output_path}.\nEl Blockchain es válido.")
    else:
        print(f"Se ha creado el fichero {output_path}.\n"
              f"El Blockchain es válido hasta el bloque {idx} de {num_blocks}.")


def salir(): 
    exit_flag = True


def valid_blockchain():


def no_valid_blockchain():


def tcr_table():


def error():
    print("!!!!! INPUT ERROR !!!!!")


def menu():
    text = f'''\
    ****************************************************                                                                                                                                                                                       
      - 1: Crear blockchain válida                                                              
      - 2: Crear blockchain no válida
      - 3: Crear tabla comparativa sobre el TCR
      - 4: Salir                                                              
    ****************************************************
    '''
    text_f = textwrap.indent(textwrap.dedent(text), ' ' * 3)
    print("\n")
    print(text_f)

    #Possible actions
    actions = {"1": valid_blockchain, "2": no_valid_blockchain, "3": tcr_table, "4": salir}

    while True:
        if exit_flag:
            break
        inp = input()
        action = actions.get(inp, error)
        action()


def main():
        text=('''\
         _  .-')    .-')     ('-.     
        ( \( -O )  ( OO ).  ( OO ).-. 
        ,------. (_)---\_) / . --. / 
        |   /`. '/    _ |  | \-.  \  
        |  /  | |\  :` `..-'-'  |  | 
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