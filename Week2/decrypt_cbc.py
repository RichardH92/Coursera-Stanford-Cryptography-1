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

    ct_block_arr = []
    for i in range(0, num_blocks):
        ct_block_arr.append(ciphertext[i * 16:(i + 1) * 16])

    return ct_block_arr

def decrypt_ciphertext_blocks(ct_block_arr):
    aes_decryptor = AES.new(key, AES.MODE_ECB)

    pt_block_arr = []
    decrypted_block = aes_decryptor.decrypt(ct_block_arr[0])
    pt_block_arr.append(strxor(decrypted_block, iv))
    for i in range(1, len(ct_block_arr)):
        decrypted_block = aes_decryptor.decrypt(ct_block_arr[i])
        pt_block_arr.append(strxor(decrypted_block, ct_block_arr[i - 1]))

    return pt_block_arr

def remove_padding(pt_block_arr):
    pad_block = pt_block_arr[len(pt_block_arr) - 1]
    pad_length = ord(pad_block[15])

    if pad_length == 16:
        pt_block_arr.pop()
    else:
        pt_block_arr[len(pt_block_arr) - 1] = pad_block[0:(16 - pad_length)]

    return pt_block_arr


key = sys.argv[1].decode('hex')
ciphertext_param = sys.argv[2].decode('hex')
iv = ciphertext_param[0:16]
ciphertext = ciphertext_param[16:len(ciphertext_param)]

ct_block_arr = split_ciphertext_into_blocks(ciphertext)
pt_block_arr = decrypt_ciphertext_blocks(ct_block_arr)
pt_block_arr = remove_padding(pt_block_arr)

plaintext = ""
for i in range(0, len(pt_block_arr)):
    plaintext = plaintext + pt_block_arr[i]

print plaintext
