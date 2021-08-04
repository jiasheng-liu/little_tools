#!python3


#=======================
# imports
#=======================
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
import pynmea2

import logging
import os
from PIL import Image, ImageTk

# logging config
logging.basicConfig(level=logging.DEBUG)

# GUI part
# create instance
win = tk.Tk()

# Add a title
win.title("nmea decoder v0.01")
win.resizable(0,0)      # disable to re-size windows

scroll_w = 45
scroll_h = 5


ttk.Label(win, text="input nmea sentence").grid(column=0, row=1)

# nmea input window
nmea_win = scrolledtext.ScrolledText(win, width=scroll_w, height=scroll_h, wrap=tk.WORD)
nmea_win.grid(column=0, row=2, columnspan=3, sticky=tk.EW)

Position_frame = tk.LabelFrame(win, text="position")
Position_frame.grid(column=0, row=10, columnspan=3, sticky=tk.EW, padx=5)
# output window frame: latitude
Lantitude_frame = tk.LabelFrame(Position_frame, text="latitude")
Lantitude_frame.grid(column=0, row=10, columnspan=1, sticky=tk.W, padx=5)
latitude_d = tk.StringVar()
lat_dms_d = tk.StringVar()
lat_dms_m = tk.StringVar()
lat_dms_s = tk.StringVar()
lat_semisphere = tk.StringVar()

# output window: format in degree, unit is degree
tk.Label(Lantitude_frame, text="degree").grid(column=0, row=1)
lat_degree_win = tk.Entry(Lantitude_frame, width=int(scroll_w/3), state='readonly', textvariable=latitude_d)
lat_degree_win.grid(column=0,row=2, columnspan=2, padx=5)

# output window: which semisphere
tk.Label(Lantitude_frame, text="semisphere").grid(column=2, row=1)
tk.Entry(Lantitude_frame, width=int(scroll_w/10), state='readonly', textvariable=lat_semisphere).grid(column=2, row=2, padx=3)

# output window: format in degree,minutes,seconds
tk.Label(Lantitude_frame, text="d").grid(column=0, row=3)
tk.Entry(Lantitude_frame, width=int(scroll_w/10), state='readonly', textvariable=lat_dms_d).grid(column=0, row=4, ipadx=3)
tk.Label(Lantitude_frame, text="m").grid(column=1, row=3)
tk.Entry(Lantitude_frame, width=int(scroll_w/10), state='readonly', textvariable=lat_dms_m).grid(column=1, row=4, ipadx=3)
tk.Label(Lantitude_frame, text="s").grid(column=2, row=3)
tk.Entry(Lantitude_frame, width=int(scroll_w/7), state='readonly', textvariable=lat_dms_s).grid(column=2, row=4, ipadx=2)

# output window frame: longitude
Longitude_frame = tk.LabelFrame(Position_frame, text="longitude")
Longitude_frame.grid(column=2, row=10, columnspan=1,sticky=tk.E, padx=5)
longitude_d = tk.StringVar()
lon_dms_d = tk.StringVar()
lon_dms_m = tk.StringVar()
lon_dms_s = tk.StringVar()
lon_semisphere = tk.StringVar()

# output window: format in degree, unit is degree
tk.Label(Longitude_frame, text="degree").grid(column=0,row=1)
lon_degree_win = tk.Entry(Longitude_frame, width=int(scroll_w/3), state='readonly', textvariable=longitude_d)
lon_degree_win.grid(column=0,row=2, columnspan=2, padx=5)

# output window: format in degree,minutes,seconds
tk.Label(Longitude_frame, text="d").grid(column=0, row=3)
tk.Entry(Longitude_frame, width=int(scroll_w/10), state='readonly', textvariable=lon_dms_d).grid(column=0, row=4, ipadx=3)
tk.Label(Longitude_frame, text="m").grid(column=1, row=3)
tk.Entry(Longitude_frame, width=int(scroll_w/10), state='readonly', textvariable=lon_dms_m).grid(column=1, row=4, ipadx=3)
tk.Label(Longitude_frame, text="s").grid(column=2, row=3)
tk.Entry(Longitude_frame, width=int(scroll_w/7), state='readonly', textvariable=lon_dms_s).grid(column=2, row=4, ipadx=3)

# output window: which semisphere
tk.Label(Longitude_frame, text="semisphere").grid(column=2, row=1)
tk.Entry(Longitude_frame, width=int(scroll_w/10), state='readonly', textvariable=lon_semisphere).grid(column=2, row=2, ipadx=3)

def update_result_pic(res=''):
    if len(images_folder) == 0:
        return

    if (res in images_name):
        image_path = os.path.join(images_folder, images_name[res])
    else:
        return

    image = Image.open(image_path)
    img = ImageTk.PhotoImage(image)
    image_label.configure(image=img)
    image_label.image = img

# decode button handler
def decode_callback():
    nmea = nmea_win.get('1.0', 'end-1c')
    logging.debug(type(nmea_win))
    logging.debug(len(nmea))
    if (len(nmea)):
        try:
            data = pynmea2.parse(nmea)
            longitude_d.set(str("%05f" %abs(data.longitude)))
            lon_dms_d.set(str("%3d" %abs(data.longitude)))
            lon_dms_m.set(str("%02d" %data.longitude_minutes))
            lon_dms_s.set(str("%05.3f" %data.longitude_seconds))
            lon_semisphere.set(str(data.lon_dir))
            logging.debug(longitude_d)
            latitude_d.set(str("%05f" %abs(data.latitude)))
            lat_dms_d.set(str("%02d" %abs(data.latitude)))
            lat_dms_m.set(str("%02d" %data.latitude_minutes))
            lat_dms_s.set(str("%05.3f" %data.latitude_seconds))
            lat_semisphere.set(str(data.lat_dir))

            if (data.sentence_type == 'RMC'):
                days = data.datetime.day
                hours = data.datetime.hour
                minutes = data.datetime.minute
                month = data.datetime.month
                year = data.datetime.year
                seconds = data.datetime.second
                date_str.set(str("%02d-%02d-%02d" %(year, month, days)))
                time_str.set(str("%02d:%02d:%02d" %(hours, minutes, seconds)))

                logging.debug("%d-%d-%d, %d:%d:%d" %(year, month, days, hours, minutes, seconds))

            else:
                date_str.set("")
                time_str.set("")

            buttem_msg.configure(foreground="GREEN", font=('', 9, 'bold'))
            button_message.set("success in translating")
            update_result_pic('success')
        except:
            # messagebox.showwarning(title="Warnning", message="Error occurred during translating")
            # button_message.set("Error occurred during translating")
            buttem_msg.configure(foreground="RED", font=('', 9, 'bold'))
            button_message.set("Error occurred during translating")
            update_result_pic('fail')
    else:
        buttem_msg.configure(foreground="RED", font=('', 9, 'bold'))
        button_message.set("Please input a nmea sentence")
        update_result_pic('fail')
    win.update()


# add a button
button_decode = tk.Button(win, text="decode", command=decode_callback)
button_decode.grid(column=0, row=9)
button_message = tk.StringVar()
tk.Label(win, text="result").grid(column=1, row=9)
buttem_msg = tk.Entry(win,width=int(scroll_w*2/3), state='readonly', textvariable=button_message, background="RED")
buttem_msg.grid(column=2, row=9, padx=5)


# add date time
date_time_frame = tk.LabelFrame(win, text="date&time")
date_time_frame.grid(column=0, row=11, columnspan=4, sticky=tk.W, padx=5)
date_str = tk.StringVar()
tk.Label(date_time_frame, text='date').grid(column=0, row=0, padx=3)
tk.Entry(date_time_frame, width=int(scroll_w/3), state="readonly", textvariable=date_str).grid(column=1, row=0, padx=3, columnspan=1)

time_str = tk.StringVar()
tk.Label(date_time_frame, text='time').grid(column=2, row=0, padx=10)
tk.Entry(date_time_frame, width=int(scroll_w/3), state="readonly", textvariable=time_str).grid(column=3, row=0, padx=3, columnspan=1)

# tk.Label(win, text="(ꈍᴗꈍ)", font=( , '12', )).grid(column=2, row=11, sticky=tk.E, padx=5)
# insert photo
images_name = {"start":"smile_s.png","success":"bling_s.png", "fail":"sad_s.png"}
images_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
if not os.path.exists(images_folder):
    images_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")
    if not os.path.exists(images_folder):
        images_folder = ""

if len(images_folder):
    image_path = os.path.join(images_folder, images_name['start'])

    image = Image.open(image_path)
    img = ImageTk.PhotoImage(image)
    image_label = tk.Label(win, image=img)
    image_label.grid(column=2, row=11, sticky=tk.E, padx=5)

#=======================
# Start GUI
#=======================
win.mainloop()


