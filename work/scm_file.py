#! /bin/python3
#-*- utf-8 -*-


import sys
import os
import yaml
import ctypes as c

from scm_common import crc16_ccitt, now_byteorder, hashcode



class scm_file_header:

    __input_yaml = ""
    __out_file = ""
    __current_dir = os.path.dirname(__file__)
    __file_data = {}

    __header_key = "SCM"
    __header_data = {}

    __header_buffer = []
    __header_magic_word = c.c_uint32(0)
    __header_crc = c.c_uint16(0)
    __header_shrink_hold = c.c_uint16(0)
    __header_version = c.c_uint8(0)
    __header_flag = c.c_uint8(0)
    __header_rfu = bytes(6)
    __content=""


    key_scm_ver = "filever"

    def __init__(self, in_file, out_file):
        self.__input_yaml = in_file
        self.__out_file = out_file


    def get_header_length(self) -> int:
        length = 0
        length += c.sizeof(self.__header_magic_word)
        length += c.sizeof(self.__header_shrink_hold)
        length += c.sizeof(self.__header_version)
        length += c.sizeof(self.__header_flag)
        length += c.sizeof(self.__header_rfu)
        length += c.sizeof(self.__header_crc)
        return length


    def load_yaml(self) -> dict:
        yaml_file = self.__input_yaml
        try:
            with open(yaml_file, 'r') as stream:
                try:
                    self.__file_data = yaml.safe_load(stream)
                except:
                    print("failed to load yaml file")
                    exit(-1)
                finally:
                    stream.close()

            if (self.__file_data.get(self.__header_key.lower()) is not None):
                self.__header_data = self.__file_data[self.__header_key.lower()]
            else:
                raise KeyError
        
        except KeyError:
            print("key error, no %s" % self.__header_key.lower())
            exit(-1)

        except:
            print("failed to open yaml file")
            exit(-1)
        return self.__header_data



    def output_yaml(self):
        print(self.__file_data)



    def set_header_key(self, key: str):
        self.__header_key = key.lower()


    def set_header_magic_word(self, word:int = 0):
        if (word == 0):
            self.__header_magic_word.value = int.from_bytes(bytes(self.__header_key.upper(), encoding="utf-8"), byteorder=sys.byteorder)
        else:
            self.__header_magic_word.value = word


    def set_header_shrink_hold(self, hold: int) -> bool:
        if ((hold < 0) or (hold >= 2 ** (c.sizeof(self.__header_shrink_hold) * 8))):
            print("wrong hold param")
            return False
        self.__header_shrink_hold.value = hold
        return True


    def set_header_version(self, version: int) -> bool:
        if ((version < 0) or (version >= 2 ** (c.sizeof(self.__header_version) * 8))):
            print("wrong version")
            return False
        self.__header_version.value = version
        return True


    def set_header_flag(self, bitnum: int, bitvalue: int) -> bool:
        if ((bitnum < 0) or (bitnum > 2 ** (c.sizeof(self.__header_flag) * 8))):
            print("wrong bit num")
            return False
        if (bitvalue != 0 and bitvalue != 1):
            print("wrong bit value")
            return False
        if (bitvalue):
            self.__header_flag.value |= 1 << bitnum
        else:
            self.__header_flag.value &=~(1 << bitnum)
        return True


    def convert_element_from_yaml(self):
        if (self.key_scm_ver in self.__header_data.keys()):
            self.set_header_version(version=self.__header_data[self.key_scm_ver])
        value = int.from_bytes(bytes(self.__header_key.upper(), encoding="utf-8"), byteorder=sys.byteorder)
        self.set_header_magic_word(word=value)
        self.set_header_shrink_hold(hold=2048)


    def format_header(self):
        self.__header_buffer.extend(list(int(self.__header_magic_word.value).to_bytes(c.sizeof(self.__header_magic_word), byteorder=now_byteorder)))
        self.__header_buffer.extend(list(int(self.__header_shrink_hold.value).to_bytes(c.sizeof(self.__header_shrink_hold), byteorder=now_byteorder)))
        self.__header_buffer.extend(list(int(self.__header_version.value).to_bytes(c.sizeof(self.__header_version), byteorder=now_byteorder)))
        self.__header_buffer.extend(list(int(self.__header_flag.value).to_bytes(c.sizeof(self.__header_flag), byteorder=now_byteorder)))
        self.__header_buffer.extend(list(self.__header_rfu))

        self.__header_crc.value = crc16_ccitt(bytearray(self.__header_buffer))
        self.__header_buffer.extend(list(int(self.__header_crc.value).to_bytes(c.sizeof(self.__header_crc), byteorder=now_byteorder)))

        print(str(self.__header_buffer))


    def write_header(self):
        with open(self.__out_file, 'wb') as f:
            array_asdf = bytearray(self.__header_buffer)
            f.write(array_asdf)
        f.close()


