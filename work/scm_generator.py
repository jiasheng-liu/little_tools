#! /bin/python3
#-*- utf-8 -*-


from zlib import crc32
import sys
import os
import yaml
import ctypes as c


class SCMFile(c.BigEndianStructure):

    __input_yaml = "./scm.yaml"
    __out_file = "./scm.def"
    __current_dir = os.path.dirname(__file__)
    __file_data = {}

    __header_key = "scm"
    __header_data = {}

    __header_buffer = []
    __header_magic_word = c.c_uint32(0x55AA1199)
    __header_crc = c.c_uint32(0x3344EEFF)
    __header_shrink_hold = c.c_uint32(0x00001000)
    __header_version = c.c_uint8(0x01)
    __header_flag = c.c_uint8(0x00)
    __header_rfu = c.c_uint16(0x0101)
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


    def format_header(self, header=None):
        # if ( header is None or (not isinstance(dict, header)) or len(header) == 0):
        #     print("wrong parameter")
        #     header=self.__header_data

        # if (header.get(self.__header_key) is not None):
        #     header = header[self.__header_key]

        self.__header_buffer.append(self.__header_magic_word)
        self.__header_buffer.append(self.__header_crc)
        self.__header_buffer.append(self.__header_shrink_hold)
        self.__header_buffer.append(self.__header_version)
        self.__header_buffer.append(self.__header_flag)
        self.__header_buffer.append(self.__header_rfu)
        self.__header_crc = crc32(bytes(self.__header_buffer[2:]))
        self.__header_buffer[1] =  self.__header_crc

        print(str(self.__header_buffer))
        with open("temp.def", 'wb') as f:
            for value in self.__header_buffer:
                # print(type(value).size())
                # print(value.value)
                num = int(value.value)
                print(c.sizeof(value))
                f.write(num.to_bytes(c.sizeof(value), byteorder="big"))
                # f.write(value.to_bytes(4, byteorder='little'))
                # print(type(value))
                # if (type(value) == "ctype.c_uint"):
                # str(value).encode('hex')[::-1]
                # f.write(value)
        f.close()



    def convert(self):
        pass



def generate():
    data = SCMFile(in_file="scm.yaml")
    data.load_yaml()
    data.output_yaml()
    data.format_header()

if __name__ == "__main__":
    generate()




