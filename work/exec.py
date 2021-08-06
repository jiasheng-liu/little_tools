#! /bin/python3
#-*- utf-8 -*-

"""
Header( 8 bytes in total for example ): storage version (1 byte) 
List of parameters as Data (VLT: value, property, length_v(2B), length_p(2B), tag(4B))
; tag is put at the end, as parser is expected to read data from back.

For each parameter

tag:  tag=hash(keypath)
length_p: length of property
length_v: length of value
property: flags(2B, no use so far), type(1B), version (1B), crc (4B, counting from ts), ts(4B, time stamp), length of key path (1B), key path
value: value
"""



""" some code block
from zlib import crc32

data = "hello world"
checksum = crc32(data.encode('utf-8'))
print(type(checksum))
print("checksum=%d" % checksum)

"""


""" hash code
import sys
import os

class record(object):

    data = ""
    def __init__(self, string):
        data = string
        print(data)

    def hashCode(self, string):
        seed = 31
        h = 0
        for c in string:
            h = int(seed * h) & 0xFFFFFFFF
            h = h + ord(c)
        return h
    
"""



import sys
import numpy as np


sys_is_le = sys.byteorder == 'little'
print(sys_is_le)
print(sys.byteorder)

int32 = np.int32(1)
print(int32)

# a = np.dtype.newbyteorder(np.uint32, '>')
dt = np.dtype(np.int32)
a = dt.newbyteorder('>')
# print(sys.byteorder)
print (a)
print(int32)


