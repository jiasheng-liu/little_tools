#! /bin/python3
#-*- utf-8 -*-


import sys
import os
import yaml
import ctypes as c

from scm_common import crc16_ccitt, now_byteorder, hashcode
from scm_recordItem import scm_recordItem, scm_recordItemProperty
from scm_file import scm_file_header



magic_word = "scm"


def scm_generate_header(infile, outfile):
    """
    new a scm file header and create file
    """
    header = scm_file_header(in_file=infile, out_file=outfile)
    header.load_yaml()
    header.convert_element_from_yaml()
    header.format_header()
    header.write_header()
    header.output_yaml()


def scm_generate_new_record(outfile, cmd:str, data:dict):
    """
    append a new record from infile to outfile. 
    outfile must exist
    """
    if (not os.path.exists(outfile)):
        exit(-1)

    if (not isinstance(data, dict)):
        exit(-2)
    key_list = data.keys()
    key_path = ""

    print(key_list)
    for key in key_list:
        value_dict = data[key]
        key_path = ""
        key_path = '/'.join([cmd, key])
        value_type = ""

        if (isinstance(value_dict, dict)):
            value = value_dict['value']
            for key1 in value_dict.keys():
                if (key1 in record.rditppt_key_list):
                    if (key1 == "flag"): # flag
                        record.set_property_flag(value=value_dict["flag"])
                    elif (key1 == "version"):
                        record.set_property_version(version=value_dict["version"])
                    elif (key1 == "type"):
                        record.set_property_type(ptype=value_dict['type'])
                        value_type = value_dict["type"]
                    elif (key1 == "value"):
                        pass
                    else:
                        print("key1=" +str(key1))
        else:
            value = value_dict

        if (isinstance(value, str) and (value_type != "string")):
            if (value.isdigit()):
                value = int.from_bytes(bytes(value, encoding="utf-8"), byteorder=sys.byteorder)

        record = scm_recordItem(keypath=key_path)

        if (isinstance(value, str) or isinstance(value, bytes) or isinstance(value, bytearray)):
            record.set_record_lv(ptype=type(value), length=len(value))
        else:
            record.set_record_lv(ptype=type(value), length=0)

        record.set_record_value(data=value)

        file_data = bytearray()
        file_data = record.format_record()
        record.write_record(outfile, file_data)

        # record.delet

    print("done")





def scm_generator():
    input_file = "./scm.yaml"
    output_file = "./scm.def"
    current_dir = os.path.dirname(__file__)
    input_file = os.path.join(current_dir, input_file)
    output_file = os.path.join(current_dir, output_file)

    if (not os.path.exists(input_file)):
        exit(-1)

    scm_generate_header(infile=input_file, outfile=output_file)

    with open(input_file, 'r') as f:
        yaml_data = yaml.safe_load(f)
    f.close()

    yaml_key_list = list(yaml_data.keys())
    print(type(yaml_key_list))
    yaml_key_list.remove(magic_word)
    for key in yaml_key_list:
        scm_generate_new_record(outfile=output_file, cmd=key, data=yaml_data[key])



if __name__ == "__main__":
    scm_generator()