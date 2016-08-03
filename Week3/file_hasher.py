#!/usr/bin/python

import sys
import os
import mmap
from Crypto.Hash import SHA256

def hash_file(file):
    fin = open(file, "rb")
    mm = mmap.mmap(fin.fileno(), 0, access=mmap.ACCESS_READ)
    return hash_bytes(mm)

def hash_bytes(bytes_to_hash):
    num_blocks, fin_block_size = divmod(len(bytes_to_hash), BLOCK_SIZE)

    start = len(bytes_to_hash) - fin_block_size
    end = len(bytes_to_hash)

    curr_hash = bytes()

    while start >= 0:
        hasher = SHA256.new()
        hasher.update(bytes_to_hash[start:end] + curr_hash)
        curr_hash = hasher.digest()

        end = start
        start -= BLOCK_SIZE

    return curr_hash

BLOCK_SIZE = 1024
file = sys.argv[1]
print hash_file(file).encode('hex')
