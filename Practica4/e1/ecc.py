# Imports
import hashlib

# Utils
def parsingToAsci(text):
    asciText = ''.join(format(ord(c),'x') for c in text)
    return asciText

# Functions
def execute():

    # It has been executed the command "cat 1.bin 2.bin 3.bin 4.bin > mensaje.bin" 

    # After that, we open the file and read the information
    message_file = open("mensaje.bin", "rb")
    message = message_file.read()
    
    # We construct the content of the preamble
    preamble = '20' * 64   
    text = "TLS 1.3, server CertificateVerify"
    asciText = parsingToAsci(text)
    preamble += asciText
    preamble += '00'

    #Cipher suite AES 256 SHA 384
    message384 = hashlib.sha384(message)
    message384 = message384.hexdigest()
    
    # Changing string to bytes and after that we compute the sha256
    m = hashlib.sha256(bytes.fromhex(preamble + message384))
    m = m.hexdigest()
    
    # We write the content in a new file in order to have the result for the signature verification
    mfile = open("m.txt", "w")
    mfile.flush()
    mfile.write(m)

    message_file.close()
    mfile.close()

    return

# Main
if __name__ == "__main__":
    execute()

