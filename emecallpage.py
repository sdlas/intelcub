import tkinter as tk
import tkinter.colorchooser
import pygame as py
import time
import _thread
import serial
import cv2
from PIL import Image, ImageTk
import multiprocessing
import math
from backbtn import backbtn
from title import title
from background import background
class emecallpage():
    def __init__(self,mainclass,matser,_winheight,_winwidth):
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.master = matser
        self.mainclass = mainclass
        self.working = True
        self.comwidth = 210
        self.comheight = 100
        self.clockimg = ImageTk.PhotoImage(Image.open("srcimage/emecalling.jpg").resize((int(self.winwidth),int(self.winheight)))) 
        self.confirmimg = ImageTk.PhotoImage(Image.open("srcimage/stopeme.jpg").resize((int(self.comwidth),int(self.comheight)))) 
        self.emecallpage = tk.Canvas(self.master,height = self.winheight ,width =self.winwidth)
        self.emecallpage.place(x=0,y=0)
        #背景
        bg = background(self.emecallpage,self.winheight,self.winwidth,"clock")
        #标题
        bg.backgroundcanvas.create_image(0,0,anchor="nw",image=self.clockimg)
        self.combtn = tk.Button(self.emecallpage,image=self.confirmimg,width=self.comwidth,height=self.comheight,command=self.back)
        self.combtn.place(x=(self.winwidth-self.comwidth)/2,y=self.winheight*6/7)
        _thread.start_new_thread(self.playmusic,("threadname",1))
    def playmusic(self,threadname,x):
        filepath = "alarming.mp3"
        py.mixer.init()
        # 加载音乐
        py.mixer.music.load(filepath)
        py.mixer.music.play(loops=-1, start=0.0)
        time.sleep(300)
        py.mixer.music.stop()
    def back(self):
        py.mixer.music.stop()
        self.mainclass.fallflag = False
        self.mainclass.voicerecing = True
        with open('flag.txt','w') as file_handle:   # .txt可以不自己新建,代码会自动新建
            file_handle.write("0")
        self.emecallpage.destroy()