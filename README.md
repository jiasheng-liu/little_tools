# little_tools

this project will collect some scripts and tools developed by ourselves for our work

## NMEA Decoder

The first tool is NMEA decoder to decode NMEA sentence in GNSS. We can input the NMEA sentence in the "input window", and click "decode" button. Then it will get the location infor from the NMEA sentence and display them in the "latitude" and "longitude"

this script is based on python3, uses python GUI frame (tkinter, python internal lib) and nmea decoder lib (pynmea2, github repo: `https://github.com/Knio/pynmea2`)

The **nmea_decoder.exe** is an executive program which can run on Windows directly even if there is no pynmea2 in your python environment.
