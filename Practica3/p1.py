import block_chain 
import block
import transaction
import rsa_public_key
import rsa_key
import textwrap


def options():
    print("Introduce el número correspondiente a la opción que quieres ejecutar: ")
    print

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
        
        options()

if __name__ == '__main__':
    main()