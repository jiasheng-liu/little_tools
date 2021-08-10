#! /bin/python3
#-*- utf-8 -*-

now_byteorder = "little"

def crc16_ccitt(data:bytes, poly=0x8408) -> int :
    """
    crc16_ccitt, polymode is 0x8408
    refer: https://gist.github.com/oysstu/68072c44c02879a2abf94ef350d1c7c6
    """
    # data = bytearray(data)
    crc = 0xFFFF
    for b in data:
        cur_byte = b & 0xFF
        for _ in range(0, 8):
            if (crc & 0x0001) ^ (cur_byte & 0x0001):
                crc ^= poly
            else:
                crc >>= 1
            cur_byte >>= 1
    crc = (~crc & 0xFFFF)
    crc = (crc << 8) | ((crc >> 8) & 0xFF)
    return crc & 0xFFFF


def hashcode(data: bytes) -> int:
    """
    refer to hashcode on java, this function will return 4 bytes hashcode
    hash() in zlib returns 8 bytes data as int in python3 is long. no long type in python3
    """
    seed = 31
    h = 0
    for c in data:
        h = int(seed * h) & 0xFFFFFFFF
        h = h + c
    return h


if __name__ == "__main__":
    data = bytes("hello world!", encoding='utf-8')
    crc = crc16_ccitt(data=data)
    print(crc)
    hc = hashcode(data=data)
    print(hc)

