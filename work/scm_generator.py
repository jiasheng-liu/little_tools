#! /bin/python3
#-*- utf-8 -*-


import sys
import os
import yaml
import ctypes as c

from scm_common import crc16_ccitt



class SCMFile:

    __input_yaml = "./scm.yaml"
    __out_file = "./scm.def"
    __current_dir = os.path.dirname(__file__)
    __file_data = {}

    __header_key = "scm"
    __header_data = {}

    __header_buffer = []
    __header_magic_word = c.c_uint32(0x55AA1199)
    __header_crc = c.c_uint16(0)
    __header_shrink_hold = c.c_uint32(0x00001000)
    __header_version = c.c_uint8(0x01)
    __header_flag = c.c_uint8(0x00)
    __header_rfu = c.c_uint32(0)
    __content=""

    def __init__(self, in_file="", out_file=""):
        if (in_file is not ""):
            self.__input_yaml = os.path.join(self.__current_dir, in_file)
        else:
            self.__input_yaml = os.path.join(self.__current_dir, self.__input_yaml)
        if (out_file is not ""):
            self.__out_file = os.path.join(self.__current_dir, out_file)
        else:
            self.__out_file = os.path.join(self.__current_dir, self.__out_file)


    def load_yaml(self, in_file=""):
        yaml_file = in_file
        if (in_file is ""):
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

            if (self.__file_data.get(self.__header_key) is not None):
                self.__header_data = self.__file_data[self.__header_key]
            else:
                raise KeyError
        
        except KeyError:
            print("key error, no %s" % self.__header_key)
            exit(-1)

        except:
            print("failed to open yaml file")
            exit(-1)



    def output_yaml(self):
        print(self.__file_data)


    def convert_element(self, type="", value=""):
        pass


    def format_header(self):
        self.__header_buffer.extend(list(int(self.__header_magic_word.value).to_bytes(c.sizeof(self.__header_magic_word), byteorder=now_byteorder)))
        self.__header_buffer.extend(list(int(self.__header_shrink_hold.value).to_bytes(c.sizeof(self.__header_shrink_hold), byteorder=now_byteorder)))
        self.__header_buffer.extend(list(int(self.__header_version.value).to_bytes(c.sizeof(self.__header_version), byteorder=now_byteorder)))
        self.__header_buffer.extend(list(int(self.__header_flag.value).to_bytes(c.sizeof(self.__header_flag), byteorder=now_byteorder)))
        self.__header_buffer.extend(list(int(self.__header_rfu.value).to_bytes(c.sizeof(self.__header_rfu), byteorder=now_byteorder)))

        self.__header_crc.value = crc16_ccitt(bytearray(self.__header_buffer))
        self.__header_buffer.extend(list(int(self.__header_crc.value).to_bytes(c.sizeof(self.__header_crc), byteorder=now_byteorder)))

        print(str(self.__header_buffer))
        with open("temp.def", 'wb') as f:
            array_asdf = bytearray(self.__header_buffer)
            f.write(array_asdf)
        f.close()



class recordItem:

    def __init__(self):
        pass






def generate():
    data = SCMFile(in_file="scm.yaml")
    data.load_yaml()
    data.output_yaml()
    data.format_header()

if __name__ == "__main__":
    generate()




