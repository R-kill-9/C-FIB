import os
import subprocess
from glob import glob
from math import gcd, ceil, log2

import Crypto.PublicKey.RSA as rsa
import numpy as np
from Crypto.Util import number

from sqrt_long_division import sqrt_long_division

output_path = './outputs'
rw_input_path = './RSA_RW'
pseudo_input_path = './RSA_pseudo'
student = 'ricard.medina'


def decrypt_RW(rsa_key, encrypted_aes_key, encrypted_file):

    file_name = './RSA_RW/ricard.medina_pubkeyRSA_RW.pem'
    with open(file_name, 'rb') as file:
        someone_rsa_key = rsa.importKey(file.read())
        file.close()
    p = gcd(rsa_key.n, someone_rsa_key.n)

    if p != 1:
        q = rsa_key.n // p
        generate_key(p, q, rsa_key.e)
        decrypt_aes_key(encrypted_aes_key)
        decrypt_file(encrypted_file)





def calculate_k(n):
    return 2 ** (ceil(log2(n.bit_length())) - 1)


def split_n(n):
    k = int(calculate_k(n))
    binary_n = np.binary_repr(n, 2 * k)[::-1]
    lower_rs = binary_n[0:k // 2]
    l = binary_n[k // 2: (3 * k // 2)]
    upper_rs = binary_n[3 * k // 2:]
    # OJO!! Los bits estan invertidos, hay que revertilos antes de pasarlos a enteros
    return k, upper_rs, l, lower_rs


def get_rs_1024(upper_rs, lower_rs):
    # Si suponemos que no ha habido overflow
    rs = int((lower_rs + upper_rs)[::-1], 2)
    lmd = int((upper_rs + lower_rs)[::-1], 2)
    return rs, lmd


def get_rs_1024_overflow(upper_rs, lower_rs):
    # Si suponemos que ha habido overflow
    upper_rs = invert_bits(upper_rs)
    rs = int((lower_rs + upper_rs)[::-1], 2)
    lmd = int((upper_rs + lower_rs)[::-1], 2)
    return rs, lmd


def get_rs_1025(upper_rs, lower_rs):
    # Si suponemos que no ha habido overflow
    if upper_rs[0] == '0':
        upper_rs = invert_bits(upper_rs)
    else:
        upper_rs = '0' + upper_rs[1:]
    rs = int((lower_rs + upper_rs)[::-1], 2)
    lmd = int((upper_rs + lower_rs)[::-1], 2)
    return rs, lmd


def get_rs_1025_overflow(upper_rs, lower_rs):
    # Si suponemos que ha habido overflow
    upper_rs = upper_rs[0] + invert_bits(upper_rs[1:])
    rs = int((lower_rs + upper_rs)[::-1], 2)
    lmd = int((upper_rs + lower_rs)[::-1], 2)
    return rs, lmd


def invert_bits(upper_rs):
    u_rs = list(upper_rs)
    for idx, bit in enumerate(upper_rs):
        if bit == '0':
            u_rs[idx] = '1'
        else:
            u_rs[idx] = '0'
            break
    return ''.join(u_rs)


def calculate_r_s(rs, l, lmd):
    r = sqrt_long_division((-(lmd - l) + sqrt_long_division((lmd - l) ** 2 - 4 * (rs ** 2))) // 2)
    s = rs // r
    return r, s


def calculate_p_q(n, k, upper_rs, l, lower_rs):
    rs, lmd = get_rs_1024(upper_rs, lower_rs)
    p, q = get_p_q(k, int(l[::-1], 2), rs, lmd)
    if n == p * q:
        return p, q

    rs, lmd = get_rs_1024_overflow(upper_rs, lower_rs)
    p, q = get_p_q(k, int('1' + l[::-1], 2), rs, lmd)
    if n == p * q:
        return p, q

    rs, lmd = get_rs_1025(upper_rs, lower_rs)
    p, q = get_p_q(k, int('1' + l[::-1], 2), rs, lmd)
    if n == p * q:
        return p, q

    rs, lmd = get_rs_1025_overflow(upper_rs, lower_rs)
    p, q = get_p_q(k, int('10' + l[::-1], 2), rs, lmd)
    if n == p * q:
        return p, q

    return -1, -1


def get_p_q(k, l_int, rs, lmd):
    try:
        r, s = calculate_r_s(rs, l_int, lmd)
        p = int(np.binary_repr(r, k // 2) + np.binary_repr(s, k // 2), 2)
        q = int(np.binary_repr(s, k // 2) + np.binary_repr(r, k // 2), 2)
        return p, q
    except ValueError:
        return -1, -1


def generate_key(p, q, e):
    new_rsa_key = rsa.construct((p * q, e, number.inverse(e, (p - 1) * (q - 1)), p, q))
    private_rsa_key = new_rsa_key.export_key()

    filename = f'{student}_privkeyRSA_RW.pem'
    with open(os.path.join(output_path, filename), 'wb') as file:
        print("generando privkeyRSA_RW.pem")
        file.write(private_rsa_key)
        file.close()


def decrypt_aes_key(key_path):
    key_filename = f'{student}_privkeyRSA_RW.pem'
    filename = f'{student}_RSA_RW_decrypted.key'
    subprocess.run(['openssl', 'pkeyutl', '-decrypt',
                    '-in', key_path,
                    '-out', os.path.join(output_path, filename),
                    '-inkey', os.path.join(output_path, key_filename)])
    print("generado archivo aes")


def decrypt_file(file_path):
    filename = f'{student}_RW_decrypted_file.png'
    key_filename = f'{student}_RSA_RW_decrypted.key'
    print("generado archivo rw")
    subprocess.run(['openssl', 'enc', '-d', '-aes-128-cbc', '-pbkdf2',
                    '-kfile', os.path.join(output_path, key_filename),
                    '-in', file_path,
                    '-out', os.path.join(output_path, filename)])
    


class Parte2:
    @staticmethod
    def execute_part1():
        with open(os.path.join(rw_input_path, f'{student}_pubkeyRSA_RW.pem'), 'rb') as file:
            my_rsa_key = rsa.importKey(file.read())
            file.close()

        print('Decryption starts')
        decrypt_RW(my_rsa_key, os.path.join(rw_input_path, f'{student}_RSA_RW.enc'),
                   os.path.join(rw_input_path, f'{student}_AES_RW.enc'))
        print('End')



if __name__ == '__main__':
    Parte2.execute_part1()
