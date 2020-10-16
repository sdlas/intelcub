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
from wordtovoice import wordtovoice #语音识别
class envpage():
    def __init__(self,mainclass,matser,_winheight,_winwidth):
        self.mainclass = mainclass
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.master = matser
        self.envpage = tk.Frame(self.master,bg="pink",height = self.winheight ,width =self.winwidth)
        self.envpage.place(x=0,y=0)
        #背景
        bg = background(self.envpage,self.winheight,self.winwidth,"call")
        #返回按钮
        backbtn(self.mainclass,self.envpage,self.winheight,self.winwidth,3)
        #标题
        title(self.envpage,self.winheight,self.winwidth,"环境监测")
        self.fontsize = 20
        self.topheight = 130
        self.canvaswidth = 150
        self.canvasheight =50
        self.sidepaddingx = 60
        self.toppaddingy = 50
        self.xpadding = (self.winwidth - self.canvaswidth*4-self.sidepaddingx*2)/3
        self.ypadding = 80
        self.q = 30
        self.tipscanvaswidth = 350
        self.tipscanvasheight = 180
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
        self.infoimg = ImageTk.PhotoImage(Image.open("srcimage/info.jpg").resize((int(self.tipscanvaswidth),int(self.tipscanvasheight)))) 
        for i in range(0,len(self.namelist)):
            self.canvaslist.append(tk.Canvas(self.envpage,bg="yellowgreen",width=self.canvaswidth,height=self.canvasheight))
            self.numcanvaslist.append(tk.Canvas(self.envpage,bg="white",width=self.canvaswidth,height=self.canvasheight))
            self.canvaslist[i].place(x=self.movex[i%2*2],y=self.movey[int(i/2)])
            self.numcanvaslist[i].place(x=self.movex[i%2*2+1],y=self.movey[int(i/2)])
            self.canvaslist[i].create_text(self.canvaswidth/2,self.canvasheight/2,text=self.namelist[i],font=("宋体",self.fontsize))
            self.numcanvaslist[i].create_text(self.canvaswidth/2,self.canvasheight/2,text=self.numlist[i],font=("宋体",self.fontsize))
        self.tipscanvas = tk.Canvas(self.envpage,width=self.tipscanvaswidth,height=self.tipscanvasheight)
        self.tipscanvas.create_image(0,0,anchor="nw",image=self.infoimg)
        self.tipscanvas.place(x=self.winwidth-self.tipscanvaswidth,y=self.winheight-self.tipscanvasheight)
        _thread.start_new_thread(self.fresh,("threadname",1))
        self.played = False
        bg.showimage()
    def fresh(self,threadname,x):
        #打开串口，波特率9600，无校验，停止位1，数据位8，连接超时2秒
        ser=serial.Serial("/dev/ttyUSB1", 9600, parity='N', stopbits=1, bytesize=8, timeout=5)
        # ser=serial.Serial("/dev/ttyUSB0", 9600, parity='N', stopbits=1, bytesize=8, timeout=5)
        while(1):
            string = ser.read(32).hex()
            pm25 = self.toten(string[12:16])
            pm10 = self.toten(string[16:20])
            tem = self.toten(string[48:52])/10
            humdity = self.toten(string[52:56])/10
            if pm25<75:
                self.canvaslist[2].config(bg="greenyellow")
            elif pm25>75 and pm25<220:
                self.canvaslist[2].config(bg="yellow")
            else:
                self.canvaslist[2].config(bg="red")
            for i in range(0,4):
                self.numcanvaslist[i].delete("all")
            if tem<20:
                self.canvaslist[0].config(bg="yellow")
            elif tem>20 and tem<27:
                self.canvaslist[0].config(bg="greenyellow")
            else:
                self.canvaslist[0].config(bg="red")
            if humdity<30:
                self.canvaslist[1].config(bg="yellow")
            elif humdity>30 and humdity<70:
                self.canvaslist[1].config(bg="greenyellow")
            else:
                self.canvaslist[1].config(bg="red")
            if pm10<50:
                self.canvaslist[3].config(bg="greenyellow")
            elif pm10<300:
                self.canvaslist[3].config(bg="yellow")
            else:
                self.canvaslist[3].config(bg="red")



            self.numcanvaslist[0].create_text(self.canvaswidth/2,self.canvasheight/2,text=str(tem)+"℃",font=("宋体",self.fontsize))
            self.numcanvaslist[1].create_text(self.canvaswidth/2,self.canvasheight/2,text=str(humdity)+"%",font=("宋体",self.fontsize))
            self.numcanvaslist[2].create_text(self.canvaswidth/2,self.canvasheight/2,text=str(pm25)+"ug/m3",font=("宋体",self.fontsize))
            self.numcanvaslist[3].create_text(self.canvaswidth/2,self.canvasheight/2,text=str(pm10)+"ug/m3",font=("宋体",self.fontsize))
            if not self.played:
                tems = ""
                hums = ""
                pm25s = ""
                if pm25<75:
                    pm25s = "空气质量良好"
                elif pm25>75 and pm25<220:
                    pm25s = "空气轻度污染"
                else:
                    pm25s = "空气重度污染"
                if tem<20:
                    tems = "温度较低注意保暖"
                elif tem>20 and tem<27:
                    tems = "温度适宜"
                else:
                    tems = "温度较高注意防寒"
                if humdity<30:
                    hums = "空气较干燥"
                elif humdity>30 and humdity<70:
                    hums = "湿度适宜"
                else:
                    hums ="空气较潮湿"
                string = tems + hums +pm25s
                wordtovoice(self.mainclass,string)
                self.played = True
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
        self.mainclass.curfunid = -1
        self.envpage.destroy()