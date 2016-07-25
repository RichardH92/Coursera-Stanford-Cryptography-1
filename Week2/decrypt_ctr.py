#!/usr/bin/python

import sys
from Crypto.Cipher import AES

def strxor(a, b):
    if len(a) > len(b):
       return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
       return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

def split_ciphertext_into_blocks(ciphertext):
    num_blocks = len(ciphertext) / 16
    if len(ciphertext) % 16 != 0:
        num_blocks = num_blocks + 1

    ct_block_arr = []
    for i in range(0, num_blocks):
        ct_block_arr.append(ciphertext[i * 16:(i + 1) * 16])

    return ct_block_arr

def decrypt_ciphertext_blocks(ct_block_arr, iv, key):
    aes = AES.new(key, AES.MODE_ECB)
    pt_block_arr = []

    counter = int(iv.encode('hex'), 16)

    for i in range(0, len(ct_block_arr)):
        nonce = "%x" % (counter + i)

        encrypted_nonce = aes.encrypt(nonce.decode('hex'))
        decrypted_block = strxor(ct_block_arr[i], encrypted_nonce)
        pt_block_arr.append(decrypted_block)

    return pt_block_arr

key = sys.argv[1].decode('hex')
ciphertext_param = sys.argv[2].decode('hex')
iv = ciphertext_param[0:16]
ciphertext = ciphertext_param[16:len(ciphertext_param)]

ct_block_arr = split_ciphertext_into_blocks(ciphertext)
pt_block_arr = decrypt_ciphertext_blocks(ct_block_arr, iv, key)

plaintext = ""
for i in range(0, len(pt_block_arr)):
    plaintext = plaintext + pt_block_arr[i]

print plaintext
