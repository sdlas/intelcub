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
class callpage():
    def __init__(self,matser,_winheight,_winwidth):
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.master = matser
        self.callpage = tk.Frame(self.master,bg="pink",height = self.winheight ,width =self.winwidth)
        self.callpage.place(x=0,y=0)
        #背景
        bg = background(self.callpage,self.winheight,self.winwidth,"call")
        #返回按钮
        backbtn(self.callpage,self.winheight,self.winwidth)
        #标题
        title(self.callpage,self.winheight,self.winwidth,"打电话给家人")
        self.childlist = ["firstson","secondson","thirdson"]
        self.avatarimagelist = [] #头像放置
        self.avatarlabellist = []
        #头像高度
        self.avatarpadding = 200
        self.avatarwidth = (self.winwidth - (len(self.childlist)+1)*self.avatarpadding)/len(self.childlist)
        self.avatrheight = self.avatarwidth/0.618
        self.iconwidth = 100
        self.iconpadding = 50
        self.callbtnwidth = 250
        self.callbtnheight = 150
        self.callnumberimg = ImageTk.PhotoImage(Image.open("srcimage/callnumber.jpg").resize((int(self.callbtnwidth),int(self.callbtnheight))))  
        for n in range(0,len(self.childlist)):
            self.avatarimagelist.append(ImageTk.PhotoImage(self.goodimage(self.childlist[n])))
            self.avatarlabellist.append(tk.Button(self.callpage,width=self.avatarwidth,height=self.avatrheight,image=self.avatarimagelist[n],command = self.back))
            self.avatarlabellist[n].place(x=self.avatarpadding+(self.avatarwidth+self.avatarpadding)*n,y=200)
        self.callbtn = tk.Button(self.callpage,width = self.callbtnwidth,height = self.callbtnheight,image=self.callnumberimg,command=self.call)
        self.callbtn.place(x=self.winwidth-self.callbtnwidth,y=0)
        bg.showimage()
    #返回合适比例的图片
    def goodimage(self,str):
        tempimage = Image.open("srcimage/"+str+".jpg")
        imgwidth = tempimage.size[0]
        imgheight = tempimage.size[1]
        imgscale = imgwidth/imgheight
        tempimage = tempimage.resize((int(self.avatarwidth),int(self.avatarwidth/imgscale)))
        return tempimage
    def back(self):
        pass
    def call(self):
        callnumber(self.master,self.winheight,self.winwidth)
class callnumber():
    def __init__(self,master,_winheight,_winwidth):
        self.master = master
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.number = ""
        self.callnumberpage = tk.Canvas(self.master,width = self.winwidth,height=self.winheight,bg="pink")
        self.callnumberpage.place(x=0,y=0)
        bg = background(self.callnumberpage,self.winheight,self.winwidth,"call")
        title(self.callnumberpage,self.winheight,self.winwidth,"拨号")
        backbtn(self.callnumberpage,self.winwidth,self.winheight)
        self.numberbtnwidth = 120
        self.numberbtnheight = 80
        self.numberbtnpadding = 20
        self.numbercanvaswidth = 600
        self.numbercanvasheight = 100
        self.topheight = 130
        self.movex = [
            self.winwidth/2-self.numberbtnwidth*3/2-self.numberbtnpadding,
            self.winwidth/2-self.numberbtnwidth/2,
            self.winwidth/2+self.numberbtnwidth/2+self.numberbtnpadding
        ]
        self.movey = [
            self.topheight + 50,
            self.topheight + 100 + self.numbercanvasheight + self.numberbtnpadding,
            self.topheight + 100 + (self.numbercanvasheight + self.numberbtnpadding)*2,
            self.topheight + 100 + (self.numbercanvasheight + self.numberbtnpadding)*3,
            self.topheight + 100 + (self.numbercanvasheight + self.numberbtnpadding)*4,
        ]
        self.numbercanvas  = tk.Canvas(self.callnumberpage,width=self.numbercanvaswidth,height=self.numbercanvasheight)
        self.numbercanvas.place(x=(self.winwidth-self.numbercanvaswidth)/2,y=self.movey[0])
        self.btnlist = []
        self.btnvalue = [1,2,3,4,5,6,7,8,9,0,11,10]
        self.imagenamelist =["1.jpg","2.jpg","3.jpg","4.jpg","5.jpg","6.jpg","7.jpg","8.jpg","9.jpg","0.jpg","del.jpg","call.jpg"]
        self.imagelist = []
        for i in range(0,len(self.imagenamelist)):
            self.imagelist.append(
                ImageTk.PhotoImage(
                    Image.open("srcimage/"+self.imagenamelist[i]).resize(
                        (int(self.numberbtnwidth), int(self.numberbtnheight)))))
        for i in range(0,len(self.btnvalue)):
            self.btnlist.append(tk.Button(self.callnumberpage,image=self.imagelist[i],width=self.numberbtnwidth,height=self.numberbtnheight,command=self.returnfun(i)))
            self.btnlist[i].place(x=self.movex[i%3],y=self.movey[int(i/3)+1])
        bg.showimage()
    def returnfun(self,x):
        return lambda:self.input(x)
    def input(self,x):
        if x < 10:
            if len(self.number)<11:
                self.number = self.number + str(self.btnvalue[x])
        else:
            if x==10:
                if len(self.number)>0:
                    self.number =self.number[:-1]
            else:
                self.callphone()
        self.numbercanvas.delete("all")
        self.numbercanvas.create_text(self.numbercanvaswidth/2,self.numbercanvasheight/2,text=self.number,font=("宋体",40))
    def callphone(self):
        pass

