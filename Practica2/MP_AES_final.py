import array
from itertools import product
import numpy as np

class G_F:

    def __init__(self, Polinomio_Irreducible = 0x11B):


        self.Polinomio_Irreducible = Polinomio_Irreducible
        self.Tabla_EXP = [0] * 256
        self.Tabla_LOG = [0] * 256
        self.generar_tablas()

    def generar_tablas(self):
        g = 0x02  # Generador del cuerpo finito
        elemento = 0x01
        for i in range(256):
            self.Tabla_EXP[i] = elemento
            self.Tabla_LOG[elemento] = i
            elemento = self.xTimes(elemento)


    def xTimes(self, n):
        if n & 0x80:  # Comprobar si el bit mas significativo es 1
            resultado = (n << 1) ^ self.Polinomio_Irreducible
        else:
            resultado = n << 1
        return resultado & 0xFF

    def producto(self, a, b):   
        if a == 0 or b == 0:
            return 0
        exp_a = self.Tabla_LOG[a]
        exp_b = self.Tabla_LOG[b]
        exp_resultado = (exp_a + exp_b) % 255
        return self.Tabla_EXP[exp_resultado]

    def inverso(self, n):
        if n == 0:
            return 0
        return self.Tabla_EXP[255 - self.Tabla_LOG[n]]

class AES:

    def generate_Sbox_InvSbox(self):
        p = self.Polinomio_Irreducible
        t = [0] * 256
        x = 1
        for i in range(256):
            t[i] = x
            x ^= (x << 1) ^ ((x >> 7) *p)

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
        return 
    
    def generate_RCon(self):
        RCon = [1]
        for i in range(1, 10):
            RCon.append(self.gf.xTimes(RCon[i-1]))
        return RCon

    def __init__(self, key, Polinomio_Irreducible=0x11B):
        self.Polinomio_Irreducible = Polinomio_Irreducible
        self.gf = G_F(self.Polinomio_Irreducible)
        self.SBox = [0] * 256
        self.InvSBox = [0] * 256
        self.Rcon = self.generate_RCon()  # Debes completar con la tabla 5
        self.InvMixMatrix = [
            [0x0E, 0x0B, 0x0D, 0x09],
            [0x09, 0x0E, 0x0B, 0x0D],
            [0x0D, 0x09, 0x0E, 0x0B],
            [0x0B, 0x0D, 0x09, 0x0E]
        ]  # Debes completar con la matriz inversa de MixColumns
        self.Nk = 4  # Número de palabras en la clave (4, 6 u 8)
        self.Nr = 11  # Número de rondas (depende de Nk)
        self.Expanded_KEY = self.KeyExpansion(key)
        self.generate_Sbox_InvSbox()

    # Definir los métodos restantes de acuerdo a las especificaciones del AES

    def SubBytes(self, State):
        for i in range(4):
            for j in range(4):
                State[i][j] = self.SBox[State[i][j]]

    def InvSubBytes(self, State):
        for i in range(4):
            for j in range(4):
                State[i][j] = self.InvSBox[State[i][j]]

    def ShiftRows(self, State):
        for i in range(1, 4):
            State[i] = State[i][i:] + State[i][:i]

    def InvShiftRows(self, State):
        for i in range(1, 4):
            State[i] = State[i][-i:] + State[i][:-i]

    def MixColumns(self, State):
        for i in range(4):
            s0 = State[0][i]
            s1 = State[1][i]
            s2 = State[2][i]
            s3 = State[3][i]

            State[0][i] = self.xTimes(s0) ^ s1 ^ self.xTimes(s1) ^ s2 ^ s3
            State[1][i] = s0 ^ self.xTimes(s1) ^ s1 ^ self.xTimes(s2) ^ s3
            State[2][i] = s0 ^ s1 ^ self.xTimes(s2) ^ s2 ^ self.xTimes(s3)
            State[3][i] = self.xTimes(s0) ^ s0 ^ s1 ^ s2 ^ self.xTimes(s3)

    def InvMixColumns(self, State):
        for i in range(4):
            s0 = State[0][i]
            s1 = State[1][i]
            s2 = State[2][i]
            s3 = State[3][i]

            State[0][i] = self.xTimes(self.xTimes(self.xTimes(s0) ^ s1)) ^ \
                           self.xTimes(self.xTimes(s1 ^ s2)) ^ \
                           self.xTimes(s2 ^ s3) ^ s3
            State[1][i] = s0 ^ self.xTimes(self.xTimes(s1 ^ s2)) ^ \
                           self.xTimes(self.xTimes(s2 ^ s3)) ^ \
                           self.xTimes(s3 ^ s0)
            State[2][i] = self.xTimes(s0 ^ s1) ^ s1 ^ \
                           self.xTimes(self.xTimes(s2 ^ s3)) ^ \
                           self.xTimes(self.xTimes(s3 ^ s0))
            State[3][i] = self.xTimes(self.xTimes(s0 ^ s1)) ^ \
                           self.xTimes(s1 ^ s2) ^ s2 ^ \
                           self.xTimes(self.xTimes(s3 ^ s0))

    def xTimes(self, n):
        if n & 0x80:
            result = (n << 1) ^ self.Polinomio_Irreducible
        else:
            result = n << 1
        return result & 0xFF
    
    def AddRoundKey(self, State, roundKey):
        for i in range(4):
            for j in range(4):
                State[i][j] ^= roundKey[i][j]

    def KeyExpansion(self, key):
        expanded_key = []  # Aquí debes crear la lista de palabras expandidas
        return expanded_key

    def Cipher(self, State):
        self.AddRoundKey(State, self.Expanded_KEY[0])

        for round_num in range(1, self.Nr):
            self.SubBytes(State)
            self.ShiftRows(State)
            self.MixColumns(State)
            self.AddRoundKey(State, self.Expanded_KEY[round_num])

        self.SubBytes(State)
        self.ShiftRows(State)
        self.AddRoundKey(State, self.Expanded_KEY[self.Nr])

    def InvCipher(self, State):
        self.AddRoundKey(State, self.Expanded_KEY[self.Nr])

        for round_num in range(self.Nr - 1, 0, -1):
            self.InvShiftRows(State)
            self.InvSubBytes(State)
            self.AddRoundKey(State, self.Expanded_KEY[round_num])
            self.InvMixColumns(State)

        self.InvShiftRows(State)
        self.InvSubBytes(State)
        self.AddRoundKey(State, self.Expanded_KEY[0])

    def encrypt_file(self, input_file, output_file, iv):
      #iv = os.urandom(16)  # Genera un IV aleatorio de 16 bytes

        cipher = AES.new(self.Expanded_KEY[0], AES.MODE_CBC, iv)

        with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
            f_out.write(iv)  # Escribe el IV en el archivo cifrado

            while True:
                chunk = f_in.read(16)
                if not chunk:
                    break

                # Asegura que el chunk tenga una longitud múltiplo de 16
                if len(chunk)%16 != 0:
                    chunk += b' ' * (16-len(chunk)%16)

                ciphertext = cipher.encrypt(chunk)
                f_out.write(ciphertext)

    def remove_pkcs7_padding(data, prev_chunk):
        last_byte = data[-1]  # Obtiene el valor del último byte
        padding_length = last_byte

        if padding_length < 1 or padding_length > 16:
            # El relleno no es válido, se debe manejar el error adecuadamente
            raise ValueError("Padding no válido")

        # Verifica si el relleno es válido
        for i in range(-padding_length, -1):
            if data[i] != last_byte:
                raise ValueError("Padding no válido")

        # Elimina el relleno
        return data[:-padding_length]


    def decrypt_file(self, input_file, output_file):
        with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
            iv = f_in.read(16)  # Lee el IV del archivo cifrado

            cipher = AES.new(self.Expanded_KEY[0], AES.MODE_CBC, iv)

            prev_chunk = iv

            while True:
                chunk = f_in.read(16)
                if not chunk:
                    break

                decrypted_chunk = cipher.decrypt(chunk)
                f_out.write(self.remove_pkcs7_padding(decrypted_chunk, prev_chunk))
                prev_chunk = chunk
  
key = bytearray(00000000000000000000000000000000)
aes=AES(key,0x11B)