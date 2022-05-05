from msilib.schema import Billboard
import pandas as pd
import tkinter as tk
import time
from vpython import *
from tkinter import filedialog
import math

root = tk.Tk()
root.withdraw()

xArrow = arrow(axis=vector(1,0,0), length=10, color=color.red, shaftwidth=.2)
yArrow = arrow(axis=vector(0,1,0), length=10, color=color.green, shaftwidth=.2)
zArrow = arrow(axis=vector(0,0,1), length=10, color=color.blue, shaftwidth=.2)
    
rocket = cylinder(length=12, pos=vector(0, 1, 0), width=1.5, height=1.5)
rocket.rotate(axis=vector(0,0,1), angle=math.pi/2)

tvc = cylinder(length=16, pos=vector(0,1,0), width=.5, height=.5)
tvc.rotate(axis=vector(0,0,1), angle=-math.pi/2)

L = label(pos=rocket.pos,
    text='Mode: ', xoffset=70,
    yoffset=50, space=30,
    height=16, border=4,
    font='sans')

def set_angle(yaw, pitch, tvc_x, tvc_y):
    x = 10*math.cos(yaw)*math.cos(pitch)
    y = 10*math.sin(yaw)*math.cos(pitch)
    z = 10*math.sin(pitch)
    rocket.axis = vector(x, y, z)
    rocket.rotate(angle=math.pi/2, axis=vector(0,0,1))

    tvc_pitch = pitch - (tvc_x - pi/2)
    tvc_yaw = yaw - (tvc_y - pi/2)

    tx = 10*math.cos(tvc_yaw)*math.cos(tvc_pitch)
    ty = 10*math.sin(tvc_yaw)*math.cos(tvc_pitch)
    tz = 10*math.sin(-tvc_pitch)
    tvc.axis = vector(tx, ty, tz)
    tvc.rotate(angle=-math.pi/2, axis=vector(0,0,1))

file_path = filedialog.askopenfilename()

df = pd.read_csv(file_path)

sleep(5)

lastFrame = df.iloc[0]
df = df.iloc[1: , :]

for index, row in df.iterrows():
    time.sleep(row['current_time']-lastFrame['current_time'])

    L.text = "Mode: " + str(row['mode'])
    set_angle(row['euler[x]'], row['euler[y]'], (math.pi/180)*row['servo_u[x]'], (math.pi/180)*row['servo_u[y]'])
    lastFrame = row