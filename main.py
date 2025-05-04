import datetime    
import webbrowser
import interface
import tkinter     
from tkinter import *
import numpy as np  
import cv2 as cv    
import pyautogui
from tkinter import filedialog

status = ""

# Find the time for name
def find_time():
    x = datetime.datetime.now()
    date_for_name = (x.strftime("%d") + "-" + x.strftime("%m") + "-" + x.strftime("%Y") + "-" + x.strftime("%H") + "-" +
                     x.strftime("%M") + "-" + x.strftime("%S"))
    return date_for_name

def edit_checks(clicked):
    if clicked == "mp4":
        if interface.mp4_format.get() == False:
            interface.avi_format.set(True)
        else:
            interface.avi_format.set(False)
    elif clicked == "avi":
        if interface.avi_format.get() == False:
            interface.mp4_format.set(True)
        else:
            interface.mp4_format.set(False)

def result_format():
    return ".mp4" if interface.mp4_format.get() else ".avi"

def result_format2():
    return "MP4V" if result_format() == ".mp4" else "XVID"

interface.video_format.add_checkbutton(label=".mp4", onvalue=1, offvalue=0, variable=interface.mp4_format,
                                       command=lambda: edit_checks("mp4"))
interface.video_format.add_checkbutton(label=".avi", onvalue=1, offvalue=0, variable=interface.avi_format,
                                       command=lambda: edit_checks("avi"))

interface.about.add_command(label="TG | @Dante_Clever")
interface.about.add_command(label="Website | Alpha Role Play ",
                            command=lambda: webbrowser.open("https://alpharp.ir/"))

def open_file():
    global ok
    directory = filedialog.askdirectory()
    ok = directory + "\\"

open_img = PhotoImage(file=f"assets/open.png")
big = Button(image=open_img, command=open_file, borderwidth=0, highlightthickness=0, relief="flat").place(x=2, y=2)

def create_vid():
    global out
    global ok
    screen_size = pyautogui.size()
    fourcc = cv.VideoWriter_fourcc(*result_format2())
    
    # FPS is fixed at 20
    fps = 20
    out = cv.VideoWriter(ok + find_time() + result_format(), fourcc, fps, screen_size)

def record():
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    out.write(frame)

def toggle_record(event):
    if status == "playing":
        status_playing("end")  # Stop recording
    else:
        start_record()  # Start recording

def start_record():
    if status in ("end"):
        create_vid()
    status_playing("playing")

def status_playing(yeter):
    global status
    status = yeter
    if status == "stopped":
        interface.pause["state"] = "disabled"
        interface.start["state"] = "normal"
        interface.canvas.itemconfig(interface.info, text="نگه داشته شد و در صورت ادامه شروع را بزنيد ")
    elif status == "playing":
        interface.pause["state"] = "normal"
        interface.end["state"] = "normal"
        interface.start["state"] = "disabled"
        interface.canvas.itemconfig(interface.info, text="درحال ظبط")
    elif status == "end":
        interface.canvas.itemconfig(interface.info, text="ذخیره شد ")
        interface.pause["state"] = "disabled"
        interface.end["state"] = "disabled"
        interface.start["state"] = "normal"
        interface.root.quit()  # Close the application

# Quality Selection
def set_quality(quality):
    global resolution
    resolution = quality
    interface.quality_label.config(text=f"Quality: {quality}")

interface.start.config(command=lambda: start_record())
interface.end.config(command=lambda: status_playing("end"))
interface.pause.config(command=lambda: status_playing("stopped"))

# FPS scale disabled for user
#interface.fps_scale = Scale(interface.root, from_=1, to=60, bg="#2B29AF", fg="Black", orient=HORIZONTAL, borderwidth=0, highlightthickness=0, relief="flat")
#interface.fps_scale.set(20)  # Set default FPS to 20
#interface.fps_scale.config(state='disabled')  # Disable user interaction
#interface.fps_scale.place(x=540, y=366)  

# Add quality selection buttons
interface.quality_label = Label(interface.root, text="Select Quality", bg="#2B29AF", fg="White")
interface.quality_label.place(x=540, y=420)

quality_options = ["240p", "480p", "720p", "1080p"]
quality_var = StringVar(value=quality_options[0])  # Default to 240p

for quality in quality_options:
    button = Button(interface.root, text=quality, command=lambda q=quality: set_quality(q))
    button.place(x=540, y=450 + (quality_options.index(quality) * 30))

interface.root.bind("<F10>", toggle_record)

interface.running = True
while interface.running:
    interface.root.update()
    interface.start.place(x=318, y=230, width=172, height=58)
    interface.pause.place(x=118, y=230, width=172, height=58)
    interface.end.place(x=518, y=230, width=172, height=58)
    interface.root.config(menu=interface.menubar)

    if status == "playing":
        record()
    elif status == "stopped":
        pass
    elif status == "end":
        out.release()
