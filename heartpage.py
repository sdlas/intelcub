from mttkinter import mtTkinter as tk
import tkinter.colorchooser
import pygame as py
import time
import _thread
from tkinter import *
import serial
import array
import cv2
from PIL import Image, ImageTk
import multiprocessing
import math
from background import background
from backbtn import backbtn #返回按钮
from title import title
class heartpage():
    def __init__(self,mainclass,master,_winheight,_winwidth):
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.master = master
        self.mainclass = mainclass
        self.imagereadlist=[]
        self.topheight = 130 #顶部标题高度
        self.heartpage = tk.Canvas(self.master,bg="pink",width=self.winwidth,height=self.winheight)
        self.heartpage.place(x=0,y=0)
        self.heartpage.configure(highlightthickness=0)
        self.startbtnwidth = 350
        self.working = False
        self.btnimage = ImageTk.PhotoImage(
            Image.open("srcimage/startm.jpg").resize(
                (int(self.startbtnwidth), int(self.startbtnwidth))))
        self.waitingimage = ImageTk.PhotoImage(
            Image.open("srcimage/waiting.jpg").resize(
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
        self.startbtn.place(x=(self.winwidth-self.startbtnwidth)/2,y=(self.winheight-self.startbtnwidth)/2)
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