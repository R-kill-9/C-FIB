import hashlib


def Asci(text):
    return ''.join(format(ord(char),'x') for char in text)


def main():

    original_message = open("mensaje.bin", "rb")
    message = original_message.read()
    original_message.close()

    preamble = '20' * 64   
    text = "TLS 1.3, server CertificateVerify"
    asci_text = Asci(text)
    preamble += asci_text
    preamble += '00'
    message_384 = hashlib.sha384(message)
    message_384 = message_384.hexdigest()
    
    m = hashlib.sha256(bytes.fromhex(preamble + message_384))
    m = m.hexdigest()
    
    mfile = open("result.txt", "w")
    mfile.flush()
    mfile.write(m)
    mfile.close()

    return

if __name__ == "__main__":
    main()

