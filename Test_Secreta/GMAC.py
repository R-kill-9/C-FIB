from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
from Crypto.Util.number import long_to_bytes, bytes_to_long

def gmac(message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    subkeys = [cipher.encrypt(bytes([i])) for i in range(128)]
    
    # Paso 1: Dividir el mensaje en bloques de 128 bits
    blocks = [message[i:i+16] for i in range(0, len(message), 16)]
    
    # Paso 3: Inicializar y como un bloque de 16 bytes lleno de ceros
    y = bytes([0] * 16)
    
    # Paso 4 y 5: XOR y multiplicación por la matriz de Galois
    for block in blocks:
        y = strxor(y, block)
        y = cipher.encrypt(y)
    
    # Paso 6: XOR el resultado de la multiplicación con el último bloque del mensaje
    tag = strxor(y, blocks[-1])
    
    return tag

# Mensaje y clave de autenticación en formato hexadecimal
mensaje = 0x80000000000000000000000000000000.to_bytes(16, 'big')
clave_autenticacion = 0x00000000000000000000000000000002.to_bytes(16, 'big')

# Calcular el valor de y
valor_y = gmac(mensaje, clave_autenticacion)

# Imprimir el resultado en formato hexadecimal
print("Valor de y:", valor_y.hex())

