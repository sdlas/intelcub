from mttkinter import mtTkinter as tk
import tkinter.colorchooser
import pygame as py
import time
import _thread
import serial
import array
import cv2
from PIL import Image, ImageTk
import multiprocessing
import math
from background import background
from backbtn import backbtn #返回按钮
from title import title
import matplotlib.pyplot as plt
class heartpage():
    def __init__(self,mainclass,master,_winheight,_winwidth):
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.master = master
        self.mainclass = mainclass
        self.imagereadlist=[]
        self.topheight = 130 #顶部标题高度
        self.heartpage = tk.Canvas(self.master,bg="pink",width=self.winwidth,height=self.winheight,)
        self.heartpage.place(x=0,y=0)
        self.heartpage.configure(highlightthickness=0)
        self.startbtnwidth = 350
        self.working = False
        self.xmove = 250
        self.btnimage = ImageTk.PhotoImage(
            Image.open("srcimage/startm.jpg").resize(
                (int(self.startbtnwidth), int(self.startbtnwidth))))
        self.historyimage = ImageTk.PhotoImage(
            Image.open("srcimage/history.jpg").resize(
                (int(self.startbtnwidth), int(self.startbtnwidth))))
        self.waiting0 = ImageTk.PhotoImage(
            Image.open("srcimage/waiting0.jpg").resize(
                (int(self.startbtnwidth), int(self.startbtnwidth))))
        self.waiting1 = ImageTk.PhotoImage(
            Image.open("srcimage/waiting1.jpg").resize(
                (int(self.startbtnwidth), int(self.startbtnwidth))))
        self.waiting2 = ImageTk.PhotoImage(
            Image.open("srcimage/waiting2.jpg").resize(
                (int(self.startbtnwidth), int(self.startbtnwidth))))
        self.waiting3 = ImageTk.PhotoImage(
            Image.open("srcimage/waiting3.jpg").resize(
                (int(self.startbtnwidth), int(self.startbtnwidth))))
        self.waiting4 = ImageTk.PhotoImage(
            Image.open("srcimage/waiting4.jpg").resize(
                (int(self.startbtnwidth), int(self.startbtnwidth))))
        self.waiting5 = ImageTk.PhotoImage(
            Image.open("srcimage/waiting5.jpg").resize(
                (int(self.startbtnwidth), int(self.startbtnwidth))))
         #背景
        bg = background(self.heartpage,self.winheight,self.winwidth,"call")
        #返回按钮
        backbtn(self.heartpage,self.winheight,self.winwidth)
        #标题
        title(self.heartpage,self.winheight,self.winwidth,"心率测量")
        self.startbtn = tk.Button(self.heartpage,image = self.btnimage,width=self.startbtnwidth,height=self.startbtnwidth,command=self.start)
        self.startbtn.place(x=(self.winwidth-self.startbtnwidth)/2-self.xmove,y=(self.winheight-self.startbtnwidth)/2)
        self.hbtn = tk.Button(self.heartpage,image = self.historyimage,width=self.startbtnwidth,height=self.startbtnwidth,command=self.seehistory)
        self.hbtn.place(x=(self.winwidth-self.startbtnwidth)/2+self.xmove,y=(self.winheight-self.startbtnwidth)/2)
        bg.showimage()
    def start(self):
        if not self.working:
            _thread.start_new_thread(self.mainclass.bloodpressuretest,(self,"threadname",1))
            self.working = True
            _thread.start_new_thread(self.waitinggif,("threadname",1))
        else:
            pass
    def showresult(self,resultlist):
        self.working = False
        self.startbtn.config(image = self.btnimage)
        result(self.heartpage,self.winheight,self.winwidth,resultlist)
    def showbadresult(self):
        self.working = False
        self.startbtn.config(image = self.btnimage)
        result(self.heartpage,self.winheight,self.winwidth,-1)
    def waitinggif(self,threadname,x):
        flag = 0
        plus = True
        while self.working:
            if flag == 0:
                self.startbtn.config(image=self.waiting0)
            if flag == 1:
                self.startbtn.config(image=self.waiting1)
            if flag == 2:
                self.startbtn.config(image=self.waiting2)
            if flag == 3:
                self.startbtn.config(image=self.waiting3)
            if flag == 4:
                self.startbtn.config(image=self.waiting4)
            if flag == 5:
                self.startbtn.config(image=self.waiting5)
            if plus:
                flag = flag + 1
            else:
                flag = flag - 1
            if flag == 5:
                plus = False
            if flag == 0:
                plus = True
            time.sleep(0.2)
    def seehistory(self):
        if not self.working:
            history(self.heartpage,self.winheight,self.winwidth)
class result():
    def __init__(self,master,_winheight,_winwidth,resultlist):
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.master = master
        self.resultlist = resultlist
        self.fontpadding = 60
        self.fontsize = 30
        if self.resultlist!=-1:
            self.resultpage = tk.Canvas(self.master,bg="greenyellow",width = self.winwidth,height = self.winheight)
            self.resultpage.place(x=0,y=0)
            self.resultpage.create_text(self.winwidth/2,self.winheight/2-self.fontpadding*3/2,text="高压:"+str(self.resultlist[0]),font=("宋体",self.fontsize))
            self.resultpage.create_text(self.winwidth/2,self.winheight/2-self.fontpadding*1/2,text="低压:"+str(self.resultlist[1]),font=("宋体",self.fontsize))
            self.resultpage.create_text(self.winwidth/2,self.winheight/2+self.fontpadding*1/2,text="心率:"+str(self.resultlist[2]),font=("宋体",self.fontsize))
            self.resultpage.create_text(self.winwidth/2,self.winheight/2+self.fontpadding*7/4,text="非常健康，一切良好",font=("宋体",self.fontsize+5))
            backbtn(self.resultpage,self.winheight,self.winwidth)
        else:
            self.resultpage = tk.Canvas(self.master,bg="red",width = self.winwidth,height = self.winheight)
            self.resultpage.place(x=0,y=0)
            self.resultpage.create_text(self.winwidth/2,self.winheight/2,text="测量出错，请检查仪器是否佩戴正确",font=("宋体",self.fontsize+10))
            backbtn(self.resultpage,self.winheight,self.winwidth)
class history():
    def __init__(self,master,_winheight,_winwidth):
        self.master = master
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.history = tk.Canvas(self.master,bg="pink",width=self.winwidth,height=self.winheight)
        self.history.place(x=0,y=0)
        self.linewidth = 5 #线宽
        self.pointradius = 6
        #背景
        bg = background(self.history,self.winheight,self.winwidth,"call")
        #返回按钮
        backbtn(self.history,self.winheight,self.winwidth)
        self.paddingl = 200 #水平的间隙
        self.paddingv = 60 #竖直方向的间隙 
        self.matwidth = self.winwidth-self.paddingl*2
        self.matheight = self.winheight-self.paddingv*2
        self.perx = self.matwidth/100
        self.pery = self.matheight/100
        self.matcanvas = tk.Canvas(self.history,bg="white",width=self.matwidth,height=self.matheight)
        self.matcanvas.place(x=self.paddingl,y=self.paddingv)
        self.opointx = 10*self.perx
        self.opointy = 90*self.pery
        self.yheight = 80*self.pery
        self.xwidth = 80*self.perx
        self.highpressurelist = []
        self.pressurescale = [90,150]
        self.lowpressurelist = []
        self.pressurelist = []
        self.datelist = []
        self.f = open("doc/heart.txt")
        line = self.f.readline().replace("\n", "")
        while line:
            self.highpressurelist.append(int(line))
            line = self.f.readline().replace("\n", "")
            self.pressurelist.append(int(line))
            line = self.f.readline().replace("\n", "")
            self.lowpressurelist.append(int(line))
            line = self.f.readline().replace("\n", "")
            templist = []
            templist.append(int(line))
            line = self.f.readline().replace("\n", "")
            templist.append(int(line))
            line = self.f.readline().replace("\n", "")
            templist.append(int(line))
            self.datelist.append(templist)
            line = self.f.readline().replace("\n", "")
        print(self.highpressurelist,self.lowpressurelist,self.pressurelist,self.datelist)
        self.pressurelength = self.pressurescale[1] - self.pressurescale[0]
        self.datevalue = []
        self.scalelist = []
        self.datescale = [self.turnvalue(self.datelist[0]),self.turnvalue(self.datelist[-1])]
        self.xlist =[]
        for i in range(0,len(self.datelist)):
            self.datevalue.append(self.turnvalue(self.datelist[i]))
            self.scalelist.append((self.datevalue[i]-self.datescale[0])/(self.datescale[1]-self.datescale[0]))
            self.xlist.append(self.opointx+self.perx*70*self.scalelist[i])
        self.drawline()
        bg.showimage()
    #将日期转化为值
    def turnvalue(self,date):
        return (date[1]-1)*30 + date[2]
    #绘制坐标轴
    def drawaxis(self):
        # x轴
        self.matcanvas.create_line(self.opointx,self.opointy,self.matwidth - self.opointx,self.opointy,fill='black')
        # y轴
        self.matcanvas.create_line(self.opointx, self.opointy,self.opointx,self.matheight-self.opointy,fill='black')
        self.matcanvas.create_text(self.opointx-25,self.opointy-10,text=str(self.pressurescale[0]),font=("宋体",20))
        self.matcanvas.create_text(self.opointx-25,self.matheight-self.opointy,text=str(self.pressurescale[1]),font=("宋体",20))
        for i in range(0,len(self.pressurelist)):
            self.matcanvas.create_text(self.xlist[i],self.opointy+30,text=str(self.datelist[i][0])+"年"+str(self.datelist[i][1])+"月"+str(self.datelist[i][2])+"日",font=("宋体",15))
    #给定低压，返回绘制y
    def lowpressurey(self,num):
        tempnum = (num - self.pressurescale[0])/self.pressurelength*self.yheight #y坐标值
        return self.turncanvasy(tempnum)
    #给定高压，返回绘制y
    def highpressurey(self,num):
        tempnum = (num - self.pressurescale[0])/self.pressurelength*self.yheight #y坐标值
        return self.turncanvasy(tempnum)
    #血压
    def pressurey(self,num):
        tempnum = (num - self.pressurescale[0])/self.pressurelength*self.yheight #y坐标值
        return self.turncanvasy(tempnum)
    #给定y值，返回在canvas中应该的y值
    def turncanvasy(self,num):
        return self.opointy - num
    #根据列表中已有的点，绘制图像
    def drawline(self):
        for n in range(0,len(self.pressurelist)):
            if n>0:
                self.matcanvas.create_line(self.xlist[n-1],self.highpressurey(self.highpressurelist[n-1]),self.xlist[n],self.highpressurey(self.highpressurelist[n]),fill='red',width=self.linewidth)
                self.matcanvas.create_oval(self.xlist[n-1]-self.pointradius,self.highpressurey(self.highpressurelist[n-1])-self.pointradius,self.xlist[n-1]+self.pointradius,self.highpressurey(self.highpressurelist[n-1])+self.pointradius,fill="red",width=0)
                self.matcanvas.create_line(self.xlist[n-1],self.lowpressurey(self.lowpressurelist[n-1]),self.xlist[n],self.lowpressurey(self.lowpressurelist[n]),fill='yellow',width=self.linewidth)
                self.matcanvas.create_oval(self.xlist[n-1]-self.pointradius,self.lowpressurey(self.lowpressurelist[n-1])-self.pointradius,self.xlist[n-1]+self.pointradius,self.lowpressurey(self.lowpressurelist[n-1])+self.pointradius,fill="yellow",width=0)
                self.matcanvas.create_line(self.xlist[n-1],self.pressurey(self.pressurelist[n-1]),self.xlist[n],self.pressurey(self.pressurelist[n]),fill='blue',width=self.linewidth)
                self.matcanvas.create_oval(self.xlist[n-1]-self.pointradius,self.pressurey(self.pressurelist[n-1])-self.pointradius,self.xlist[n-1]+self.pointradius,self.pressurey(self.pressurelist[n-1])+self.pointradius,fill="blue",width=0)
        self.matcanvas.create_oval(self.xlist[-1]-self.pointradius,self.highpressurey(self.highpressurelist[-1])-self.pointradius,self.xlist[-1]+self.pointradius,self.highpressurey(self.highpressurelist[-1])+self.pointradius,fill="red",width=0)   
        self.matcanvas.create_oval(self.xlist[-1]-self.pointradius,self.lowpressurey(self.lowpressurelist[-1])-self.pointradius,self.xlist[-1]+self.pointradius,self.lowpressurey(self.lowpressurelist[-1])+self.pointradius,fill="yellow",width=0) 
        self.matcanvas.create_oval(self.xlist[-1]-self.pointradius,self.pressurey(self.pressurelist[-1])-self.pointradius,self.xlist[-1]+self.pointradius,self.pressurey(self.pressurelist[-1])+self.pointradius,fill="blue",width=0)
        self.drawaxis()       