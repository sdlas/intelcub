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
        self.fontsize = 30
        self.topheight = 130
        self.canvaswidth = 220
        self.canvasheight =100
        self.sidepaddingx = 200
        self.toppaddingy = 100
        self.xpadding = (self.winwidth - self.canvaswidth*4-self.sidepaddingx*2)/3
        self.ypadding = 80
        self.q = 30
        self.tipscanvaswidth = 700
        self.tipscanvasheight = 250
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
        self.numlist =["20.0℃","50.0%","12ug/m3","10ug/m3"]
        self.canvaslist = []
        self.numcanvaslist =[]
        for i in range(0,len(self.namelist)):
            self.canvaslist.append(tk.Canvas(self.envpage,bg="yellowgreen",width=self.canvaswidth,height=self.canvasheight))
            self.numcanvaslist.append(tk.Canvas(self.envpage,bg="white",width=self.canvaswidth,height=self.canvasheight))
            self.canvaslist[i].place(x=self.movex[i%2*2],y=self.movey[int(i/2)])
            self.numcanvaslist[i].place(x=self.movex[i%2*2+1],y=self.movey[int(i/2)])
            self.canvaslist[i].create_text(self.canvaswidth/2,self.canvasheight/2,text=self.namelist[i],font=("宋体",self.fontsize))
            self.numcanvaslist[i].create_text(self.canvaswidth/2,self.canvasheight/2,text=self.numlist[i],font=("宋体",self.fontsize))
        self.tipscanvas = tk.Canvas(self.envpage,width=self.tipscanvaswidth,height=self.tipscanvasheight,bg="pink")
        self.tipscanvas.place(x=self.winwidth-self.tipscanvaswidth,y=self.winheight-self.tipscanvasheight)
        _thread.start_new_thread(self.fresh,("threadname",1))
        bg.showimage()
    def fresh(self,threadname,x):
        #打开串口，波特率9600，无校验，停止位1，数据位8，连接超时2秒
        ser=serial.Serial("COM5", 9600, parity='N', stopbits=1, bytesize=8, timeout=5)
        # ser=serial.Serial("/dev/ttyUSB0", 9600, parity='N', stopbits=1, bytesize=8, timeout=5)
        while(1):
            string = ser.read(32).hex()
            pm25 = self.toten(string[12:16])
            if pm25<75:
                self.canvaslist[2].config(bg="greenyellow")
            elif pm25>75 and pm25<115:
                self.canvaslist[2].config(bg="yellow")
            else:
                self.canvaslist[2].config(bg="red")
            pm10 = self.toten(string[16:20])
            tem = self.toten(string[48:52])/10
            humdity = self.toten(string[52:56])/10
            for i in range(0,4):
                self.numcanvaslist[i].delete("all")
            self.numcanvaslist[0].create_text(self.canvaswidth/2,self.canvasheight/2,text=str(tem)+"℃",font=("宋体",self.fontsize))
            self.numcanvaslist[1].create_text(self.canvaswidth/2,self.canvasheight/2,text=str(humdity)+"%",font=("宋体",self.fontsize))
            self.numcanvaslist[2].create_text(self.canvaswidth/2,self.canvasheight/2,text=str(pm25)+"ug/m3",font=("宋体",self.fontsize))
            self.numcanvaslist[3].create_text(self.canvaswidth/2,self.canvasheight/2,text=str(pm10)+"ug/m3",font=("宋体",self.fontsize))
            time.sleep(2)
    def toten(self,string):
        sum = 0
        for i in range(0,4):
            sum = sum + self.toint(string[i])*math.pow(16,int(3-i))
        return sum
    def toint(self,string):
        if string == "a":
            return 10
        if string == "b":
            return 11
        if string == "c":
            return 12
        if string == "d":
            return 13
        if string == "e":
            return 14
        if string == "f":
            return 15
        else:
            return int(string)
    def back(self):
        self.envpage.destroy()