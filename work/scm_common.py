#! /bin/python3
#-*- utf-8 -*-


"""
some links: 
    crc: 
        https://crccalc.com/
        https://gist.github.com/aurelj/270bb8af82f65fa645c1
        https://gist.github.com/oysstu/68072c44c02879a2abf94ef350d1c7c6



"""



now_byteorder = "big"

def crc16_ccitt(data:bytes, poly=0x8408) -> int :

    crc = 0xFFFF
    for b in data:
        b = b & 0xFF
        crc ^= b
        for _ in range(0, 8):
            if (crc & 0x0001):
                crc = (crc >> 1) ^ poly
            else:
                crc = crc >> 1

    return crc & 0xFFFF


def hashcode(data: bytes, init_hash=0) -> int:
    """
    refer to hashcode on java, this function will return 4 bytes hashcode
    hash() in zlib returns 8 bytes data as int in python3 is long. no long type in python3
    """
    # seed = 31
    # h = 0
    # for c in data:
    #     h = int(seed * h) & 0xFFFFFFFF
    #     h = h + c
    # return h
    from ctypes import c_uint32
    hash_code = c_uint32(init_hash)
    for d in data:
        hash_code.value += d
        hash_code.value += (hash_code.value << 10)
        hash_code.value ^= (hash_code.value >> 6)
    hash_code.value += (hash_code.value << 3)
    hash_code.value ^= (hash_code.value >> 11)
    hash_code.value += (hash_code.value << 15)
    return hash_code.value





if __name__ == "__main__":
    data = bytes("cmee", encoding='utf-8')
    # data = bytes("123456789", encoding='utf-8')
    crc = crc16_ccitt(data=data)
    print(hex(crc))
    print(crc)
    hc = hashcode(data=data, endchar=True)
    print(hex(hc))

    # data1=bytes("cmee", encoding='utf-8')
    # hc1 = hashcode(data=data1)
    # print(hc1)

    # data1=bytes("cscs", encoding='utf-8')
    # hc1 = hashcode(data=data1)
    # print(hc1)


    # data = bytes([0x53, 0x43, 0x4D, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0A, 0x01, 0x00, 0x00, 0x00, 0x00])
    # data = bytes([0x73, 0x63, 0x6D, 0x00, 0x00, 0x00, 0x00, 0x0A, 0x01, 0x00, 0x00, 0x00, 0x00])
    # data = bytes("SCM\0\0\0\0\0\n\1\0\0\0\0\0", encoding='utf-8')
    # print(data)
    # crc = crc16_ccitt(data=data)
    # print(crc)
    # print(hex(crc))
    # hc = hashcode(data=data)
    # print(hc)

