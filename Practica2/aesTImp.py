import os
import argparse
import random


class G_F:

    def __init__(self, Polinomio_Irreducible):
        self.Tabla_EXP = [0] * 256
        self.Tabla_LOG = [0] * 256
        self.Polinomio_Irreducible = Polinomio_Irreducible

        # Inicializa la tabla Tabla_EXP y Tabla_LOG
        
        x = 1
        for i in range(256):
            self.Tabla_EXP[i] = x
            self.Tabla_LOG[x] = i
            x = self.xTimes(x)
            

    def xTimes(self, n):
        result = n << 1
        # Si el resultado nos da mayor que 255 hacemos XOR con el polinomio irreducible.
        if result > 255:
            result ^= self.Polinomio_Irreducible
        return result


    def producto(self, a, b):
        if a == 0 or b == 0:
            return 0
        else:
            log_a = self.Tabla_LOG[a]
            log_b = self.Tabla_LOG[b]
            log_result = (log_a + log_b) % 255
            result = self.Tabla_EXP[log_result]
            return result


    def inverso(self, n):
        if n == 0:
            return 0
        else:
            log_n = self.Tabla_LOG[n]
            log_result = 255 - log_n
            result = self.Tabla_EXP[log_result]
            return result



class AES:
    
    def generate_s_boxes(self):
        t = [0] * 256
        x = 1
        for i in range(256):
            t[i] = x
            x ^= (x << 1) ^ ((x >> 7) * self.Polinomio_Irreducible)

        Sbox = [0] * 256
        Sbox[0] = 0x63
        InvSbox = [0] * 256
        for i in range(255):
            x = t[255 - i]
            x |= x << 8
            x ^= (x >> 4) ^ (x >> 5) ^ (x >> 6) ^ (x >> 7)
            Sbox[t[i]] = (x ^ 0x63) & 0xFF
            InvSbox[Sbox[t[i]]] = t[i]
        self.SBox = Sbox
        self.InvSBox = InvSbox


    def generate_rcon(self):
        Rcon = [0x01]
        for i in range(1, 32):
            previous = Rcon[-1]
            if previous < 0x80:
                current = (previous << 1)
            else:
                current = (previous << 1) ^ self.Polinomio_Irreducible 
            Rcon.append(current & 0xFF)  
        return Rcon


    def __init__(self, key, Polinomio_Irreducible):
        self.Polinomio_Irreducible = Polinomio_Irreducible
        self.gf = G_F(self.Polinomio_Irreducible)
        self.SBox = [0]*256
        self.InvSBox = [0]*256
        self.generate_s_boxes()

        self.Rcon = self.generate_rcon()

        self.InvMixMatrix=(
            [0x0E, 0x0B, 0x0D, 0x09],
            [0x09, 0x0E, 0x0B, 0x0D],
            [0x0D, 0x09, 0x0E, 0x0B],
            [0x0B, 0x0D, 0x09, 0x0E]
        )
        self.Nk = 4  
        self.Nr = 10
        self.Expanded_KEY = self.KeyExpansion(key)


    def SubBytes(self, State):
        for i in range(4):
            for j in range(4):
                State[i][j] = self.SBox[State[i][j]]


    def InvSubBytes(self, State):
        for i in range(4):
            for j in range(4):
                State[i][j] = self.InvSBox[State[i][j]]


    def ShiftRows(self, State):
        State[0][1], State[1][1], State[2][1], State[3][1] = State[1][1], State[2][1], State[3][1], State[0][1]
        State[0][2], State[1][2], State[2][2], State[3][2] = State[2][2], State[3][2], State[0][2], State[1][2]
        State[0][3], State[1][3], State[2][3], State[3][3] = State[3][3], State[0][3], State[1][3], State[2][3]


    def InvShiftRows(self, State):
        State[0][1], State[1][1], State[2][1], State[3][1] = State[3][1], State[0][1], State[1][1], State[2][1]
        State[0][2], State[1][2], State[2][2], State[3][2] = State[2][2], State[3][2], State[0][2], State[1][2]
        State[0][3], State[1][3], State[2][3], State[3][3] = State[1][3], State[2][3], State[3][3], State[0][3]


    def mix_column(self, State):
        column_bytes = State[0] ^ State[1] ^ State[2] ^ State[3]
        column_first_byte = State[0]
        State[0] ^= column_bytes ^ self.gf.xTimes(State[0] ^ State[1])
        State[1] ^= column_bytes ^ self.gf.xTimes(State[1] ^ State[2])
        State[2] ^= column_bytes ^ self.gf.xTimes(State[2] ^ State[3])
        State[3] ^= column_bytes ^ self.gf.xTimes(State[3] ^ column_first_byte)


    def MixColumns(self, State):
        for i in range(4):
            self.mix_column(State[i])


    def InvMixColumns(self, State):
        for i in range(4):
            a = self.gf.xTimes(self.gf.xTimes(State[i][0] ^ State[i][2]))
            b = self.gf.xTimes(self.gf.xTimes(State[i][1] ^ State[i][3]))
            State[i][0] ^= a
            State[i][1] ^= b
            State[i][2] ^= a
            State[i][3] ^= b

        self.MixColumns(State)
    

    def AddRoundKey(self, State, roundKey):
        for i in range(4):
            for j in range(4):
                State[i][j] ^= roundKey[i][j]
    

    def bytes2matrix(self, text):
        matrix = []
        for i in range(0, len(text), 4):
            row = []
            for j in range(4):
                if i + j < len(text):
                    row.append(text[i + j])
                else:
                    row.append(0)
            matrix.append(row)
        return matrix


    def matrix2bytes(self, matrix):
        text = []
        for row in matrix:
            text.extend(row)
        return bytes(text)


    def xor_bytes(self, a, b):
        bytes_xored = []
        for i, j in zip(a, b):
            bytes_xored.append(i ^ j)
        return bytes(bytes_xored)

    def schedule_core(self, word, iteration):
        word.append(word.pop(0))
        word = [self.SBox[b] for b in word]
        word[0] ^= self.Rcon[iteration]
        return word


    def KeyExpansion(self, key):
        # Inicializa las columnas de las claves con el material de clave crudo.
        columns = self.bytes2matrix(key)
        it = len(key) // 4

        i = 1
        while len(columns) < (self.Nr + 1) * 4:
            # Copia la word anterior.
            word = list(columns[-1])

            # Realiza schedule_core una vez cada "fila".
            if len(columns) % it == 0:
                word = self.schedule_core(word, i)
                i += 1
            elif len(key) == 32 and len(columns) % it == 4:
                # Ejecuta la word a través de S-box en la cuarta iteración cuando se usa una clave de 256 bits.
                word = [self.SBox[b] for b in word]

            # XOR con la word equivalente de la iteración anterior.
            word = self.xor_bytes(word, columns[-it])
            columns.append(word)

        # Agrupa las words clave en matrices de 4x4 bytes.
        return [columns[4*i: 4*(i+1)] for i in range(len(columns) // 4)]




    def Cipher(self, State, Nr, Expanded_KEY):
        pt_state = self.bytes2matrix(State)
        self.AddRoundKey(pt_state, self.Expanded_KEY[0])
        for i in range(1, self.Nr):
            self.SubBytes(pt_state)
            self.ShiftRows(pt_state)
            self.MixColumns(pt_state)
            roundKey = self.Expanded_KEY[i]  
            self.AddRoundKey(pt_state, roundKey)
        self.SubBytes(pt_state)
        self.ShiftRows(pt_state)
        self.AddRoundKey(pt_state, self.Expanded_KEY[-1])

        State = self.matrix2bytes(pt_state)
        return State


    def InvCipher(self, State, Nr, Expanded_KEY):
        cipher_state = self.bytes2matrix(State)
        
        self.AddRoundKey(cipher_state, self.Expanded_KEY[-1])   
        self.InvShiftRows(cipher_state)
        self.InvSubBytes(cipher_state)

        for i in range(self.Nr - 1, 0, -1):             
            roundKey = self.Expanded_KEY[i]  
            self.AddRoundKey(cipher_state, roundKey)
            self.InvMixColumns(cipher_state)
            self.InvShiftRows(cipher_state)
            self.InvSubBytes(cipher_state)

        roundkey = self.Expanded_KEY[0]
        self.AddRoundKey(cipher_state, roundkey)

        State = self.matrix2bytes(cipher_state)
        return State


    def pad(self, plaintext):
        block_size = 16
        length = block_size - (len(plaintext) % block_size)
        padding = bytes([length] * length)
        return plaintext + padding


    def unpad(self, plaintext):
        block_size = 16
        length = plaintext[-1]
        assert length > 0
        message, padding = plaintext[:-length], plaintext[-length:]
        assert all(p == length for p in padding)
        return message


    def split_blocks(self, message):
        block_size = 16
        assert len(message) % block_size == 0
        
        blocks = []
        for i in range(0, len(message), block_size):
            block = message[i:i+block_size]
            blocks.append(block)
        
        return blocks


    def encrypt_file(self, fichero):
        iv = os.urandom(16)

        # Obtenemos el nombre del archivo cifrado
        output_filename = fichero + ".enc"

        # Abrimos el archivo de entrada y lectura
        with open(fichero, 'rb') as input_file:
            plaintext = input_file.read()

        plaintext = self.pad(plaintext)

        # Dividimos el texto en bloques de 16 bytes
        block_size = 16
        encrypted_blocks = []
        previous = iv
        for i in self.split_blocks(plaintext):
            encrypted_block = self.Cipher(self.xor_bytes(i, previous), self.Nr, self.Expanded_KEY)
            encrypted_blocks.append(encrypted_block)
            previous = encrypted_block

        with open(output_filename, 'wb') as output_file:
            output_file.write(iv)
            for encrypted_block in encrypted_blocks:
                output_file.write(encrypted_block)

        print(f"Archivo cifrado y guardado como {output_filename}")


    def decrypt_file(self, fichero):
        # Obtenemos el nombre del archivo original sin la extensión ".enc"
        output_filename = "decrypted_" + fichero[:-4] 

        iv = 0

        # Leer el IV del archivo cifrado
        with open(fichero, 'rb') as input_file:
            iv = input_file.read(16)
            input_file.seek(16)
            ciphertext = input_file.read()

        decrypted_blocks = []
        
        previous = iv
        # Abrimos el archivo cifrado y leer los bloques cifrados
        with open(fichero, 'rb') as input_file:
            for i in self.split_blocks(ciphertext):
                decrypted_block = self.InvCipher(i, self.Nr, self.Expanded_KEY)
                decrypted_blocks.append(self.xor_bytes(previous, decrypted_block))
                previous = i

        # Unimos los bloques descifrados
        decrypted_data = b"".join(decrypted_blocks)

        # Eliminamos el padding 
        decrypted_data = self.unpad(decrypted_data)

        with open(output_filename, 'wb') as output_file:
            output_file.write(decrypted_data)

        print(f"Archivo descifrado y guardado como {output_filename}")

        


def main():
    parser = argparse.ArgumentParser(description="Algoritmo de cifrado y descifrado AES")
    # Argumentos y opciones
    parser.add_argument("-c", action="store_true", help="Cifrar un archivo")
    parser.add_argument("-d", action="store_true", help="Descifrar un archivo")
    parser.add_argument("-k", required=True, help="Clave")
    parser.add_argument("-p", required=True, help="Polinomio Irreducible")
    parser.add_argument("-i", required=True, help="Archivo de entrada")

    args=parser.parse_args()
    
    if args.c or args.d:
        if args.k and args.p:
            # Convertir el valor del polinomio irreducible a entero
            polinomio_irreducible = int(args.p, 16)
            key = bytes.fromhex(args.k)
            aes = AES(key, polinomio_irreducible)
            if args.c:
                aes.encrypt_file(args.i)
            elif args.d:
                aes.decrypt_file(args.i)
        else:
            print("Se requieren los argumentos -k y -p.")
    else:
        parser.print_usage()

if __name__ == "__main__":
    main()
