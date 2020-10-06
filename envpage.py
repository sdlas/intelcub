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
class envpage():
    def __init__(self,matser,_winheight,_winwidth):
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.master = matser
        self.envpage = tk.Frame(self.master,bg="pink",height = self.winheight ,width =self.winwidth)
        self.envpage.place(x=0,y=0)
        #背景
        bg = background(self.envpage,self.winheight,self.winwidth,"call")
        #返回按钮
        backbtn(self.envpage,self.winheight,self.winwidth)
        #标题
        title(self.envpage,self.winheight,self.winwidth,"环境监测")
        self.topheight = 130
        self.canvaswidth = 220
        self.canvasheight =100
        self.sidepaddingx = 200
        self.toppaddingy = 100
        self.xpadding = (self.winwidth - self.canvaswidth*4-self.sidepaddingx*2)/3
        self.ypadding = 80
        self.q = 30
        self.movex=[
            self.sidepaddingx+self.q,
            self.sidepaddingx + self.canvaswidth + self.xpadding-self.q,
            self.sidepaddingx + (self.canvaswidth + self.xpadding)*2+self.q,
            self.sidepaddingx + (self.canvaswidth + self.xpadding)*3-self.q,
        ]
        self.movey=[
            self.topheight+self.toppaddingy,
            self.topheight+self.toppaddingy+self.canvasheight+self.ypadding
        ]
        self.namelist =["温度：","湿度：","PM2.5：","PM10.0："]
        self.numlist =["1000","202","12","15"]
        self.canvaslist = []
        self.numcanvaslist =[]
        for i in range(0,len(self.namelist)):
            self.canvaslist.append(tk.Canvas(self.envpage,bg="white",width=self.canvaswidth,height=self.canvasheight))
            self.numcanvaslist.append(tk.Canvas(self.envpage,bg="white",width=self.canvaswidth,height=self.canvasheight))
            self.canvaslist[i].place(x=self.movex[i%2*2],y=self.movey[int(i/2)])
            self.numcanvaslist[i].place(x=self.movex[i%2*2+1],y=self.movey[int(i/2)])
            self.canvaslist[i].create_text(self.canvaswidth/2,self.canvasheight/2,text=self.namelist[i],font=("宋体",40))
            self.numcanvaslist[i].create_text(self.canvaswidth/2,self.canvasheight/2,text=self.numlist[i],font=("宋体",40))
        bg.showimage()