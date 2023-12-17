import textwrap
import os
import subprocess



def box():
    text = '''\
               _   _  __ _           _                        _  __ _           
              | | (_)/ _(_)         | |                      (_)/ _(_)          
  ___ ___ _ __| |_ _| |_ _  ___ __ _| |_ ___  __   _____ _ __ _| |_ _  ___ _ __ 
 / __/ _ \ '__| __| |  _| |/ __/ _` | __/ _ \ \ \ / / _ \ '__| |  _| |/ _ \ '__|
| (_|  __/ |  | |_| | | | | (_| (_| | ||  __/  \ V /  __/ |  | | | | |  __/ |   
 \___\___|_|   \__|_|_| |_|\___\__,_|\__\___|   \_/ \___|_|  |_|_| |_|\___|_|
'''
    text_f = textwrap.indent(textwrap.dedent(text), ' ' * 3)
    print(text_f)

def dump1(certificate):
    subprocess.run(f"openssl x509 -in {certificate} -text", shell=True)

def dump2(certificate):
    subprocess.run(f"openssl x509 -in {certificate} -issuer", shell=True)

def dump3(certificate):
    subprocess.run(f"openssl x509 -in {certificate} -dates", shell=True)

def dump4(certificate):
    subprocess.run(f"openssl x509 -in {certificate} -fingerprint", shell=True)

def dump5(certificate):
    subprocess.run(f"openssl x509 -in {certificate} -text | grep -m 1 Issuer", shell=True)

def dump6(certificate):
    subprocess.run(f"openssl x509 -in {certificate} -text | grep -m 1 'Signature Algorithm'", shell=True)

def dump7(certificate):
    subprocess.run(f"openssl x509 -in {certificate} -text | grep -m 1 'Public Key Algorithm'", shell=True)
    subprocess.run(f"openssl x509 -in {certificate} -text | grep -m 1 'Public-Key'", shell=True)

def box2():
    text = f'''\
    ***********************************************************************************************                                                                            
      
      - 1: Este comando mostrará toda la información del certificado                                                                    
      - 2: Este comando mostrará el nombre del titular del certificado                                                              
      - 3: Este comando mostrará el nombre de la autoridad certificadora que firmó el certificado.                                                    
      - 4: Este comando mostrará las fechas de emisión y caducidad del certificado.  
      - 5: Este comando mostrará el nombre de la CN que ha emitido el certificado.
      - 6: Este comando mostrará el Signature Algorithm del certificado.
      - 7: Este comando mostrará la Public-Key del certificado.

    ***********************************************************************************************
    '''
    text_f = textwrap.indent(textwrap.dedent(text), ' ' * 3)
    print("\n")
    print(text_f)

    #Possible actions
    actions = {"1": dump1, "2": dump2, "3": dump3, "4": dump4, "5": dump5, "6": dump6, "7": dump7}

    certificate = input("Introduce la ruta de tu certificado con extension pem: ")
    if not os.path.exists(certificate):
        print("Wrong path")
        exit()

    while True:
        inp = input("Introduce la opción que quieras ejecutar: ")
        action = actions.get(inp)
        action(certificate)
        print("\n******************************************************************************************\n")


def main():
    box()
    box2()
    

if __name__ == "__main__":
    main()