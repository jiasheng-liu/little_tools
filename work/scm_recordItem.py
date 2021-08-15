#! /bin/python3
#-*- utf-8 -*-

import sys
import os
import yaml
import ctypes as c

from scm_common import crc16_ccitt, now_byteorder, hashcode



class scm_recordItemProperty:

    rditppt_flag = c.c_uint16(0)
    rditppt_type = c.c_uint8(0)
    rditppt_version = c.c_uint8(0)
    rditppt_ts = c.c_uint32(0)
    rditppt_lk = c.c_uint16(0)
    rditppt_lk_data = bytes()
    rditppt_length = c.c_uint16(0)
    rditppt_data = []

    rd_type_list = ["uint8", "uint16", "uint32", "string", "BCD", "binary"]
    rditppt_key_list = ["flag", "type", "version"]

    def __init__(self):
        self.rditppt_flag = c.c_uint16(0)
        self.rditppt_type = c.c_uint8(0)
        self.rditppt_version = c.c_uint8(0)
        self.rditppt_ts = c.c_uint32(0)
        self.rditppt_lk = c.c_uint16(0)
        self.rditppt_lk_data = bytes()
        self.rditppt_length = c.c_uint16(0)
        self.rditppt_data = []


    def get_property_length(self):
        self.rditppt_length.value = 0
        self.rditppt_length.value += c.sizeof(self.rditppt_flag)
        self.rditppt_length.value += c.sizeof(self.rditppt_type)
        self.rditppt_length.value += c.sizeof(self.rditppt_version)
        self.rditppt_length.value += c.sizeof(self.rditppt_ts)
        self.rditppt_length.value += c.sizeof(self.rditppt_lk)
        self.rditppt_length.value += self.rditppt_lk.value
        return self.rditppt_length.value


    # def set_property_type(self, ptype, bit_len=8, bitflag=False, bignum=0):
    def set_property_type(self, ptype) -> bool:
        """
        set type in property
        ptype: type field in property. manatory
        """
        idx = len(self.rd_type_list) + 1
        try:
            idx = self.rd_type_list.index(ptype)
            if (idx == len(self.rd_type_list) + 1):
                return False
        except:
            print("no matched type, please check it again")
            return False
        self.rditppt_type.value = idx
        return True


    def set_property_flag(self, bitnum=-1, bitvalue=-1, value=-1) -> bool:
        """
        bitnum: which bit. 0 means bit0, lowest bit
        bitvalue: 1 or 0
        """
        if ((bitnum >= c.sizeof(self.rditppt_flag) * 8) or (bitnum < 0 and bitnum != -1)):
            print("wrong bit")
            return False
        if ((bitvalue != 0 and bitvalue != 1) and ( bitvalue != -1 and bitnum == -1)):
            print("wrong bit value")
            return False
        if (bitvalue != -1 and bitnum != -1):
            if (bitvalue):
                self.rditppt_flag.value |= 1 << bitnum
            else:
                self.rditppt_flag.value &= ~(1 << bitnum)
        else:
            if (value == -1):
                print("wrong value")
                return False
            self.rditppt_flag.value = value

        return True


    def set_property_version(self, version) -> bool:
        if ((version >= 2 ** (c.sizeof(self.rditppt_version) * 8)) or (version < 0)):
            print("verion parameter is wrong")
            return False

        self.rditppt_version.value = version
        return True


    def set_property_ts(self):
        self.rditppt_ts.value = 0


    # def calcu_property_crc(self, andSet=True) -> c.c_uint16:
    #     data = bytearray(self.rditppt_data)
    #     crc = crc16_ccitt(data)
    #     if (andSet):
    #         self.rditppt_crc.value = crc
    #     return crc & 0xFFFF


    def set_property_lk(self, lk) -> bool:
        if ((lk >= 2 ** (c.sizeof(self.rditppt_lk) * 8)) or (lk < 0)):
            print("wrong length of key path")
            return False
        self.rditppt_lk.value = lk
        return True


    def set_property_lk_data(self, data, length, withlength=False):
        if (length < 0 or data is None):
            print("wrong data or length")
            return False
        if (length != len(data)):       # should same with dat
            return False

        self.rditppt_lk_data = bytearray()
        if (isinstance(data, str)):
            data = bytes(data+"\0", encoding='utf-8')
        self.rditppt_lk_data = bytes(data)

        if (length != len(data) - 1):   # with an end char
            return False
        else:
            length = len(data)

        if (withlength):
            if (not self.set_property_lk(length)):
                print("failed to set lk")
                return False
        else:
            if (length != self.rditppt_lk.value):
                print("wrong length")
                return False
        return True


    def format_property(self) -> bytearray:
        # rditppt_data
        self.rditppt_data.clear()

        self.rditppt_data.extend(list(int(self.rditppt_flag.value).to_bytes(c.sizeof(self.rditppt_flag), byteorder=now_byteorder)))
        self.rditppt_data.extend(list(int(self.rditppt_type.value).to_bytes(c.sizeof(self.rditppt_type), byteorder=now_byteorder)))
        self.rditppt_data.extend(list(int(self.rditppt_version.value).to_bytes(c.sizeof(self.rditppt_version), byteorder=now_byteorder)))
        self.rditppt_data.extend(list(int(self.rditppt_ts.value).to_bytes(c.sizeof(self.rditppt_ts), byteorder=now_byteorder)))
        self.rditppt_data.extend(list(int(self.rditppt_lk.value).to_bytes(c.sizeof(self.rditppt_lk), byteorder=now_byteorder)))
        self.rditppt_data.extend(list(self.rditppt_lk_data))

        # if (self.calcu_property_crc() == 0):
        #     print("failed to caculte crc")
        #     return None
        # self.rditppt_data.extend(list(int(self.rditppt_crc.value).to_bytes(c.sizeof(self.rditppt_crc), byteorder=now_byteorder)))
        return bytearray(self.rditppt_data)





class scm_recordItem(scm_recordItemProperty):

    # key_path = ""
    value = {}
    buffer = []


    def __init__(self, keypath: str) -> None:
        self.rdit_crc = c.c_uint16(0)
        self.rdit_hashcode = c.c_uint32(0)
        self.rdit_lp = c.c_uint16(0)
        self.rdit_lv = c.c_uint16(0)
        self.rdit_ppt = scm_recordItemProperty()
        self.rdit_value = bytearray()
        # key_path = bytearray(keypath, encoding='utf-8')
        self.set_property_lk_data(data=keypath, length=len(keypath), withlength=True)


    def calc_record_hashcode(self, key_path):
        print("key_path=%s, len=%d" % (key_path, len(key_path)))
        self.rdit_hashcode.value = hashcode(key_path)


    def calcu_record_crc(self, buffer, andSet=True) -> c.c_uint16:
        data = bytearray(buffer)
        crc = crc16_ccitt(data)
        if (andSet):
            self.rdit_crc.value = crc
        return crc & 0xFFFF


    def set_record_lp(self):
        self.rdit_lp.value = self.get_property_length()


    def set_record_lv(self, ptype, length =0 ) -> bool:
        if (ptype == str or ptype == bytes or ptype == bytearray):
            if ((length < 0) or (length >= 2 ** (c.sizeof(self.rdit_lv) * 8))):
                print("wrong length")
                return False
            self.rdit_lv.value = length
        elif (ptype == int):
            if (self.rd_type_list[self.rditppt_type.value] == "uint8"):
                self.rdit_lv.value = 1
            elif (self.rd_type_list[self.rditppt_type.value] == "uint16"):
                self.rdit_lv.value = 2
            elif (self.rd_type_list[self.rditppt_type.value] == "uint32"):
                self.rdit_lv.value = 4
            else:
                print("should not come here")
                return False
        return True


    def set_record_property(self) -> bool:
        return True


    def set_record_value(self, data) -> bool:
        self.rdit_value = data
        return True


    def format_record(self) -> bytearray:
        self.rdit_lp.value = self.get_property_length()
        self.set_record_property()
        self.set_record_lp()
        self.calc_record_hashcode(self.rditppt_lk_data)
        print(self.rdit_hashcode.value)
        self.buffer.clear()
        if (isinstance(self.rdit_value, str)):
            self.buffer.extend(list(bytearray(self.rdit_value, encoding="utf-8")))
        elif (isinstance(self.rdit_value, int)):
            self.buffer.extend(list(int(self.rdit_value).to_bytes(self.rdit_lv.value, byteorder=now_byteorder)))
        else:
            print("ffff")
            exit(-1)
        self.buffer.extend(list(self.format_property()))
        self.buffer.extend(list(int(self.rdit_lv.value).to_bytes(c.sizeof(self.rdit_lv), byteorder=now_byteorder)))
        self.buffer.extend(list(int(self.rdit_lp.value).to_bytes(c.sizeof(self.rdit_lp), byteorder=now_byteorder)))
        self.buffer.extend(list(int(self.rdit_hashcode.value).to_bytes(c.sizeof(self.rdit_hashcode), byteorder=now_byteorder)))

        self.calcu_record_crc(buffer=self.buffer, andSet=True)
        self.buffer.extend(list(int(self.rdit_crc.value).to_bytes(c.sizeof(self.rdit_crc), byteorder=now_byteorder)))
        return bytearray(self.buffer)


    def write_record(self, file: str, data):
        with open(file, 'ab') as f:
            f.write(data)
        f.close()

