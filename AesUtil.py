import base64
from Crypto.Cipher import AES
from base64 import encodebytes
from binascii import b2a_hex, a2b_hex


def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
          add = 16 - (len(text.encode('utf-8')) % 16)
    else:
         add = 0
    text = text + ('\0' * add)

    return text.encode('utf-8')


def encrypt(text):
    key = 'greewqnmlgbdctmd'
    key = key.encode('utf-8')

    encodeStr = base64.b64encode(text.encode('utf-8'))

    text = add_to_16(str(encodeStr, 'utf-8'))
    # text = str(encodeStr,'utf-8')

    cryptos = AES.new(key, AES.MODE_ECB)
    cipher_text = cryptos.encrypt(text)

    return b2a_hex(cipher_text)


def decrypt(text):
    key = 'greewqnmlgbdctmd'
    key = key.encode('utf-8')
    cryptor = AES.new(key, AES.MODE_ECB)
    plain_text = cryptor.decrypt(a2b_hex(text))
    # return plain_text.rstrip('\0')
    deStr = bytes.decode(plain_text).rstrip('\0') #byte
    deStr = base64.b64decode(deStr) # base64
    return deStr
