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
class playclockpage():
    def __init__(self,matser,_winheight,_winwidth):
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.master = matser
        self.comwidth = 150
        self.comheight = 100
        self.clockimg = ImageTk.PhotoImage(Image.open("srcimage/playclock.jpg").resize((int(self.winwidth),int(self.winheight)))) 
        self.confirmimg = ImageTk.PhotoImage(Image.open("srcimage/confirm.jpg").resize((int(self.comwidth),int(self.comheight)))) 
        self.playclockpage = tk.Canvas(self.master,bg="pink",height = self.winheight ,width =self.winwidth)
        self.playclockpage.place(x=0,y=0)
        #背景
        bg = background(self.playclockpage,self.winheight,self.winwidth,"clock")
        #返回按钮
        backbtn(self.playclockpage,self.winheight,self.winwidth)
        #标题
        bg.backgroundcanvas.create_image(0,0,anchor="nw",image=self.clockimg)
        self.combtn = tk.Button(self.playclockpage,image=self.confirmimg,width=self.comwidth,height=self.comheight,command=self.back)
        self.combtn.place(x=(self.winwidth-self.comwidth)/2,y=750)
        self.playmusic()
    def playmusic(self):
        filepath = "record.wav"
        py.mixer.init()
        # 加载音乐
        py.mixer.music.load(filepath)
        py.mixer.music.play(loops=-1, start=0.0)
        time.sleep(300)
        py.mixer.music.stop()
    def back(self):
        py.mixer.music.stop()
        self.playclockpage.destroy()