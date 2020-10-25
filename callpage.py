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
    def __init__(self,mainclass,matser,_winheight,_winwidth):
        self.mainclass = mainclass
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.master = matser
        self.calling = False
        self.callpage = tk.Frame(self.master,bg="pink",height = self.winheight ,width =self.winwidth)
        self.callpage.place(x=0,y=0)
        #背景
        bg = background(self.callpage,self.winheight,self.winwidth,"call")
        #返回按钮
        backbtn(self.mainclass,self.callpage,self.winheight,self.winwidth,5)
        #标题
        title(self.callpage,self.winheight,self.winwidth,"打电话给家人")
        self.childlist = ["firstson","secondson","thirdson"]
        self.avatarimagelist = [] #头像放置
        self.avatarlabellist = []
        self.numberlist = ["15060356168","18792858682","13024999392"]
        #头像高度
        self.avatarpadding = 60
        self.avatarwidth = (self.winwidth - (len(self.childlist)+1)*self.avatarpadding)/len(self.childlist)
        self.avatrheight = self.avatarwidth/0.7
        self.iconwidth = 100
        self.iconpadding = 50
        self.callbtnwidth = 125
        self.callbtnheight = 75
        self.callnumberimg = ImageTk.PhotoImage(Image.open("srcimage/callnumber.jpg").resize((int(self.callbtnwidth),int(self.callbtnheight))))  
        for n in range(0,len(self.childlist)):
            self.avatarimagelist.append(ImageTk.PhotoImage(self.goodimage(self.childlist[n])))
            self.avatarlabellist.append(tk.Button(self.callpage,width=self.avatarwidth,height=self.avatrheight,image=self.avatarimagelist[n],command = self.returnfun(n)))
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
        self.mainclass.curfunid = -1
        self.callpage.destroy()
    def call(self):
        callnumber(self.master,self.winheight,self.winwidth)
    def callfamily(self,x):
        self.calling = True
        callingpage(self,self.callpage,self.winheight,self.winwidth,x)
        ser = serial.Serial("/dev/ttyS0",
                            115200,
                            parity='N',
                            stopbits=1,
                            bytesize=8,
                            timeout=2)

        #拨打电话
        string = 'ATD'+self.numberlist[x]+';\n'
        # ser.write('ATD' + num + ';\n'.encode())
        ser.write(string.encode())

        #讀取返回字符串長度並打印
        serlen = ser.inWaiting()
        print(ser.read(serlen))
    def returnfun(self,x):
        return lambda:self.callfamily(x)
    def offphone(self):
        ser = serial.Serial("/dev/ttyS0",
                            115200,
                            parity='N',
                            stopbits=1,
                            bytesize=8,
                            timeout=2)
        ser.write('ATH;\n'.encode())

class callingpage():
    def __init__(self,mainclass,master,_winheight,_winwidth,x):
        self.master = master
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.id = x
        self.mainclass = mainclass
        self.callingpage = tk.Canvas(self.master,bg="white",width=self.winwidth,height = self.winheight)
        self.callingpage.place(x=0,y=0)
        self.avatarheight = self.winheight
        self.avatarwidth = self.avatarheight*0.7
        self.childlist = ["firstson","secondson","thirdson"]
        self.childimage = ImageTk.PhotoImage(Image.open("srcimage/"+self.childlist[self.id]+".jpg").resize((int(self.avatarwidth),int(self.avatarheight)))) 
        self.callingpage.create_image((self.winwidth-self.avatarwidth)/2,0,anchor="nw",image=self.childimage)
        self.comwidth = 210
        self.comheight = 100
        self.hangout = ImageTk.PhotoImage(Image.open("srcimage/offphone.jpg").resize((int(self.comwidth),int(self.comheight)))) 
        self.combtn = tk.Button(self.callingpage,image = self.hangout,width=self.comwidth,height=self.comheight,command=self.offphone)
        self.combtn.place(x=(self.winwidth-self.comwidth)/2,y=self.winheight*6/8)
    def offphone(self):
        self.mainclass.offphone()
        self.mainclass.calling = False
        self.callingpage.destroy()
class callnumber():
    def __init__(self,master,_winheight,_winwidth):
        self.master = master
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.number = ""
        self.callnumberpage = tk.Canvas(self.master,width = self.winwidth,height=self.winheight,bg="pink")
        self.callnumberpage.place(x=0,y=0)
        self.calling = False #是否正在打电话
        bg = background(self.callnumberpage,self.winheight,self.winwidth,"call")
        title(self.callnumberpage,self.winheight,self.winwidth,"拨号")
        backbtn(self,self.callnumberpage,self.winwidth,self.winheight,10)
        self.numberbtnwidth = 60
        self.numberbtnheight = 40
        self.numberbtnpadding = 10
        self.numbercanvaswidth = 320
        self.numbercanvasheight = 50
        self.topheight = 100
        self.movex = [
            self.winwidth/2-self.numberbtnwidth*3/2-self.numberbtnpadding,
            self.winwidth/2-self.numberbtnwidth/2,
            self.winwidth/2+self.numberbtnwidth/2+self.numberbtnpadding
        ]
        self.movey = [
            self.topheight + 25,
            self.topheight + 60 + self.numbercanvasheight + self.numberbtnpadding,
            self.topheight + 60 + (self.numbercanvasheight + self.numberbtnpadding)*2,
            self.topheight + 60 + (self.numbercanvasheight + self.numberbtnpadding)*3,
            self.topheight + 60 + (self.numbercanvasheight + self.numberbtnpadding)*4,
        ]
        self.numbercanvas  = tk.Canvas(self.callnumberpage,width=self.numbercanvaswidth,height=self.numbercanvasheight,bg="grey")
        self.numbercanvas.place(x=(self.winwidth-self.numbercanvaswidth)/2,y=self.movey[0])
        self.btnlist = []
        self.btnvalue = [1,2,3,4,5,6,7,8,9,0,11,10]
        self.imagenamelist =["1.jpg","2.jpg","3.jpg","4.jpg","5.jpg","6.jpg","7.jpg","8.jpg","9.jpg","0.jpg","del.jpg","call.jpg"]
        self.imagelist = []
        self.offphoneimg = ImageTk.PhotoImage(
            Image.open("srcimage/offphone.jpg").resize(
                (int(self.numberbtnwidth), int(self.numberbtnheight))))
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
                if self.calling:
                    self.offphone()
                else:
                    self.callphone()
        self.numbercanvas.delete("all")
        self.numbercanvas.create_text(self.numbercanvaswidth/2,self.numbercanvasheight/2,text=self.number,font=("宋体",30))
    def callphone(self):
        ser = serial.Serial("/dev/ttyS0",
                            115200,
                            parity='N',
                            stopbits=1,
                            bytesize=8,
                            timeout=2)

        #拨打电话
        # ser.write('ATD' + num + ';\n'.encode())
        string = 'ATD'+str(self.number)+';\n'
        self.calling = True
        self.btnlist[-1].config(image=self.offphoneimg)
        ser.write(string.encode())

        #讀取返回字符串長度並打印
        serlen = ser.inWaiting()
        print(ser.read(serlen))
        
        #ser.write('AT+CLIP=1;\n'.encode())#开启来电显示功能
        #ser.write('ATA;\n'.encode())#接听来电
    def offphone(self):
        self.calling = False
        self.btnlist[-1].config(image=self.imagelist[-1])
        ser = serial.Serial("/dev/ttyS0",
                            115200,
                            parity='N',
                            stopbits=1,
                            bytesize=8,
                            timeout=2)
        ser.write('ATH;\n'.encode())

