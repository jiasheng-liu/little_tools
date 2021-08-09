#! /bin/python3
#-*- utf-8 -*-

import sys
import os
import yaml
import ctypes as c

from scm_common import crc16_ccitt



class recordItemProperty:

    rditppt_flag = c.c_uint16(0)
    rditppt_type = c.c_uint8(0)
    rditppt_version = c.c_uint8(0)
    rditppt_crc = c.c_uint16(0)
    rditppt_ts = c.c_uint32(0)
    rditppt_lk = c.c_uint16(0)
    rditppt_lk_data = bytes()
    rditppt_length = c.c_uint16(0)
    rditppt_data = []

    rd_type_list = ["uint8", "uint16", "uint32", "char *", "BCD", "binary"]

    def __init__(self):
        self.rditppt_flag = c.c_uint16(0)
        self.rditppt_type = c.c_uint8(0)
        self.rditppt_version = c.c_uint8(0)
        self.rditppt_crc = c.c_uint16(0)
        self.rditppt_ts = c.c_uint32(0)
        self.rditppt_lk = c.c_uint16(0)
        self.rditppt_lk_data = bytes()
        self.rditppt_length = c.c_uint16(0)
        self.rditppt_data = []


    def get_property_length(self):
        self.rditppt_length += c.sizeof(self.rditppt_flag)
        self.rditppt_length += c.sizeof(self.rditppt_type)
        self.rditppt_length += c.sizeof(self.rditppt_version)
        self.rditppt_length += c.sizeof(self.rditppt_crc)
        self.rditppt_length += c.sizeof(self.rditppt_ts)
        self.rditppt_length += c.sizeof(self.rditppt_lk)
        self.rditppt_length += len(self.rditppt_lk_data)
        return self.rditppt_length


    # def set_property_type(self, ptype, bit_len=8, bitflag=False, bignum=0):
    def set_property_type(self, ptype) -> bool:
        """
        set type in property
        ptype: type field in property. manatory
        """
        idx = len(self.rd_type_list) + 1
        try:
            self.rd_type_list.index(ptype)
        except:
            print("no matched type, please check it again")
            return False
        self.rditppt_type = self.rd_type_list[idx]
        return True

    def set_property_flag(self, bitnum, bitvalue) -> bool:
        """
        bitnum: which bit. 0 means bit0, lowest bit
        bitvalue: 1 or 0
        """
        if ((bitnum >= c.sizeof(self.rditppt_flag) * 8) or (bitnum < 0)):
            print("wrong bit")
            return False
        if (bitvalue != 0 and bitvalue != 1):
            print("wrong bit value")
            return False
        if (bitvalue):
            self.rditppt_flag.value |= bitvalue << bitnum
        else:
            self.rditppt_flag.value &= ~bitvalue << bitnum
        return True


    def set_property_version(self, version) -> bool:
        if ((version >= 2 ** (c.sizeof(self.rditppt_version) * 8)) or (version < 0)):
            print("verion parameter is wrong")
            return False

        self.rditppt_version = version
        return True


    def set_property_ts(self):
        self.rditppt_ts = 0


    def calcu_property_crc(self, andSet=True) -> c.c_uint16:
        data = bytearray(self.rditppt_data)
        crc = crc16_ccitt(data)
        if (andSet):
            self.rditppt_crc = crc
        return crc & 0xFFFF


    def set_property_lk(self, lk) -> bool:
        if ((lk >= 2 ** (c.sizeof(self.rditppt_lk) * 8)) or (lk < 0)):
            print("wrong length of key path")
            return False
        self.rditppt_lk = lk
        return True


    def set_property_lk_data(self, data, length, withlength=False):
        if (length < 0 or data is None):
            print("wrong data or length")
            return False
        if (withlength):
            if (not self.set_property_lk(length)):
                print("failed to set lk")
                return False
        else:
            if (length != self.rditppt_lk):
                print("wrong length")
                return False
        
        self.rditppt_lk_data = bytearray(data)
        return True


    def format_property(self) -> bytearray:
        # rditppt_data
        self.rditppt_data.extend(list(int(self.rditppt_flag.value).to_bytes(c.sizeof(self.rditppt_flag), byteorder=now_byteorder)))
        self.rditppt_data.extend(list(int(self.rditppt_type.value).to_bytes(c.sizeof(self.rditppt_type), byteorder=now_byteorder)))
        self.rditppt_data.extend(list(int(self.rditppt_version.value).to_bytes(c.sizeof(self.rditppt_version), byteorder=now_byteorder)))
        self.rditppt_data.extend(list(int(self.rditppt_ts.value).to_bytes(c.sizeof(self.rditppt_ts), byteorder=now_byteorder)))
        self.rditppt_data.extend(list(int(self.rditppt_lk.value).to_bytes(c.sizeof(self.rditppt_lk), byteorder=now_byteorder)))
        self.rditppt_data.extend(list(bytearray(self.rditppt_lk_data, byteorder=now_byteorder)))
        if (self.calcu_property_crc() == 0):
            print("failed to caculte crc")
            return None
        self.rditppt_data.extend(list(int(self.rditppt_crc.value).to_bytes(c.sizeof(self.rditppt_crc), byteorder=now_byteorder)))
        return bytearray(self.rditppt_data)





class recordItem(recordItemProperty):


    rdit_hashcode = c.c_uint32(0)
    rdit_lp = c.c_uint16(0)
    rdit_lv = c.c_uint16(0)
    rdit_ppt = recordItemProperty()
    rdit_value = bytearray()
    key_path = bytearray()
    value = bytearray()


    def __init__(self, keypath, value):
        self.rdit_hashcode = c.c_uint32(0)
        self.rdit_lp = c.c_uint16(0)
        self.rdit_lv = c.c_uint16(0)
        self.rdit_ppt = recordItemProperty()
        self.rdit_value = bytearray()


    def set_record_hashcode(self):
        self.rdit_hashcode = "asdf"
    



