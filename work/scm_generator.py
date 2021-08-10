#! /bin/python3
#-*- utf-8 -*-


import sys
import os
import yaml
import ctypes as c

from scm_common import crc16_ccitt, now_byteorder, hashcode
from scm_recordItem import scm_recordItem, scm_recordItemProperty
from scm_file import scm_file_header

def scm_generate_header(infile, outfile):
    """
    new a scm file header and create file
    """
    header = scm_file_header(in_file=infile, out_file=outfile)
    header.load_yaml()
    header.output_yaml()




def scm_generator():
    input_file = "./scm.yaml"
    output_file = "./scm.def"
    current_dir = os.path.dirname(__file__)
    input_file = os.path.join(current_dir, input_file)
    output_file = os.path.join(current_dir, output_file)

    scm_generate_header(infile=input_file, outfile=output_file)



if __name__ == "__main__":
    scm_generator()