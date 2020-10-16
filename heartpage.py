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
from backbtn import backbtn  # 返回按钮
from title import title
import matplotlib.pyplot as plt
from wordtovoice import wordtovoice  # 语音识别


class heartpage():
    def __init__(self, mainclass, master, _winheight, _winwidth):
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.master = master
        self.mainclass = mainclass
        self.imagereadlist = []
        self.topheight = 130  # 顶部标题高度
        self.heartpage = tk.Canvas(
            self.master, bg="pink", width=self.winwidth, height=self.winheight,)
        self.heartpage.place(x=0, y=0)
        self.heartpage.configure(highlightthickness=0)
        self.startbtnwidth = 200
        self.working = False
        self.inhistory = False
        self.xmove = 125
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
         # 背景
        bg = background(self.heartpage, self.winheight, self.winwidth, "call")
        # 返回按钮
        backbtn(self.mainclass, self.heartpage,
                self.winheight, self.winwidth, 7)
        # 标题
        title(self.heartpage, self.winheight, self.winwidth, "心率测量")
        self.startbtn = tk.Button(self.heartpage, image=self.btnimage,
                                  width=self.startbtnwidth, height=self.startbtnwidth, command=self.start)
        self.startbtn.place(x=(self.winwidth-self.startbtnwidth) /
                            2-self.xmove, y=(self.winheight-self.startbtnwidth)/2)
        self.hbtn = tk.Button(self.heartpage, image=self.historyimage,
                              width=self.startbtnwidth, height=self.startbtnwidth, command=self.seehistory)
        self.hbtn.place(x=(self.winwidth-self.startbtnwidth) /
                        2+self.xmove, y=(self.winheight-self.startbtnwidth)/2)
        bg.showimage()

    def start(self):
        if not self.working:
            wordtovoice(self.mainclass, "正在测量中，请耐心等待")
            _thread.start_new_thread(
                self.mainclass.bloodpressuretest, (self, "threadname", 1))
            self.working = True
            _thread.start_new_thread(self.waitinggif, ("threadname", 1))
        else:
            pass

    def showresult(self, resultlist):
        self.working = False
        self.startbtn.config(image=self.btnimage)
        result(self.mainclass, self.heartpage,
               self.winheight, self.winwidth, resultlist)

    def showbadresult(self):
        self.working = False
        self.startbtn.config(image=self.btnimage)
        result(self.mainclass, self.heartpage,
               self.winheight, self.winwidth, -1)

    def waitinggif(self, threadname, x):
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
            self.inhistory = True
            self.history = history(
                self.heartpage, self.winheight, self.winwidth)

    def back(self):
        self.mainclass.curfunid = -1
        self.heartpage.destroy()


class result():
    def __init__(self, mainclass, master, _winheight, _winwidth, resultlist):
        self.mainclass = mainclass
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.master = master
        self.resultlist = resultlist
        self.fontpadding = 60
        self.fontsize = 30
        if self.resultlist != -1:
            self.resultpage = tk.Canvas(
                self.master, bg="greenyellow", width=self.winwidth, height=self.winheight)
            self.resultpage.place(x=0, y=0)
            self.resultpage.create_text(self.winwidth/2, self.winheight/2-self.fontpadding *
                                        3/2, text="收缩压:"+str(self.resultlist[0]), font=("宋体", self.fontsize))
            self.resultpage.create_text(self.winwidth/2, self.winheight/2-self.fontpadding *
                                        1/2, text="舒张压:"+str(self.resultlist[1]), font=("宋体", self.fontsize))
            self.resultpage.create_text(self.winwidth/2, self.winheight/2+self.fontpadding *
                                        1/2, text="心率:"+str(self.resultlist[2]), font=("宋体", self.fontsize))
            self.resultpage.create_text(self.winwidth/2, self.winheight/2 +
                                        self.fontpadding*7/4, text="非常健康，一切指标良好", font=("宋体", self.fontsize+5))
            self.writein()
            wordtovoice(self.mainclass, "非常健康，一切指标良好")
            backbtn(self, self.resultpage, self.winheight, self.winwidth, 8)
        else:
            self.resultpage = tk.Canvas(
                self.master, bg="red", width=self.winwidth, height=self.winheight)
            self.resultpage.place(x=0, y=0)
            self.resultpage.create_text(
                self.winwidth/2, self.winheight/2, text="测量出错，请检查仪器是否佩戴正确", font=("宋体", self.fontsize+10))
            wordtovoice(self.mainclass, "测量出错，请检查仪器是否佩戴正确")
            backbtn(self, self.resultpage, self.winheight, self.winwidth, 8)

    def writein(self):
        with open('doc/heart.txt', 'a') as file_handle:   # .txt可以不自己新建,代码会自动新建
            file_handle.write(str(self.resultlist[0]))     # 写入
            file_handle.write('\n')         # 有时放在循环里面需要自动转行，不然会覆盖上一条数据
            file_handle.write(str(self.resultlist[1])) 
            file_handle.write('\n') 
            file_handle.write(str(self.resultlist[2])) 
            file_handle.write('\n') 
            file_handle.write("2020") 
            file_handle.write('\n')
            file_handle.write("10") 
            file_handle.write('\n')
            file_handle.write("11") 
            file_handle.write('\n')
class history():
    def __init__(self,master,_winheight,_winwidth):
        self.master = master
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.history = tk.Canvas(self.master,bg="pink",width=self.winwidth,height=self.winheight)
        self.history.place(x=0,y=0)
        self.linewidth = 5 #线宽
        self.pointradius = 6
        # 背景
        bg = background(self.history,self.winheight,self.winwidth,"call")
        # 返回按钮
        bb = backbtn(self,self.history,self.winheight,self.winwidth,9)
        bb.backbtn.place(x=bb.backbtnpadding,y=10)
        self.paddingl = 60 #水平的间隙
        self.paddingv = 50 #竖直方向的间隙 
        self.matwidth = self.winwidth-self.paddingl*2
        self.matheight = self.winheight-self.paddingv*2
        self.perx = self.matwidth/100
        self.pery = self.matheight/100
        self.matcanvas = tk.Canvas(self.history,bg="white",width=self.matwidth,height=self.matheight)
        self.matcanvas.place(x=self.paddingl,y=self.paddingv+40)
        self.opointx = 10*self.perx
        self.opointy = 90*self.pery
        self.yheight = 80*self.pery
        self.xwidth = 80*self.perx
        self.highpressurelist = []
        self.highpressurescale = [90,170]
        self.lowpressurescale = [50,110]
        self.heartscale = [40,130]
        self.safescalelist =[
            [self.highpressurescale[0],140],
            [self.lowpressurescale[0],90],
            [60,100]
        ]
        self.lowpressurelist = []
        self.pressurelist = []
        self.datelist = []
        self.switchbtnwidth = 80
        self.switchbtnheight = 50
        self.curid = 0 #当前选择的模块
        self.btnpadding = 10
        self.switchimagenamelist = ["highpressure.jpg","lowpressure.jpg","heartrate.jpg"]
        self.switchimageablenamelist = ["highpressureable.jpg","lowpressureable.jpg","heartrateable.jpg"]
        self.switchimagelist = []
        self.switchimageablelist = []
        for i in range(0,len(self.switchimagenamelist)):
            self.switchimagelist.append(ImageTk.PhotoImage(Image.open("srcimage/"+self.switchimagenamelist[i]).resize((int(self.switchbtnwidth), int(self.switchbtnheight)))))
            self.switchimageablelist.append(ImageTk.PhotoImage(Image.open("srcimage/"+self.switchimageablenamelist[i]).resize((int(self.switchbtnwidth), int(self.switchbtnheight)))))
        self.menubtnlist = []
        for i in range(0,len(self.switchimagenamelist)):
            self.menubtnlist.append(tk.Button(self.matcanvas,image=self.switchimageablelist[i],width=self.switchbtnwidth,height=self.switchbtnheight,command=self.returnfun(i)))
            self.menubtnlist[i].place(x=self.btnpadding+(self.btnpadding+self.switchbtnwidth)*i,y=self.btnpadding)
        self.f = open("doc/heart.txt")
        line = self.f.readline().replace("\n", "")
        count = 0
        while line and count<5:
            count = count+1
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
            if len(self.datelist)>0:
                for i in range(0,3):
                    if templist[i]!=self.datelist[-1][i]:
                        self.datelist.append(templist)
            else:
                self.datelist.append(templist)
            line = self.f.readline().replace("\n", "")
        self.highpressurelength = self.highpressurescale[1] - self.highpressurescale[0]
        self.lowpressurelength = self.lowpressurescale[1] - self.lowpressurescale[0]
        self.heartlength = self.heartscale[1]-self.heartscale[0]
        self.datevalue = []
        self.scalelist = []
        self.datescale = [self.turnvalue(self.datelist[0]),self.turnvalue(self.datelist[-1])]
        self.xlist =[]
        for i in range(0,len(self.datelist)):
            self.datevalue.append(self.turnvalue(self.datelist[i]))
            self.scalelist.append((self.datevalue[i]-self.datescale[0])/(self.datescale[1]-self.datescale[0]))
            self.xlist.append(self.opointx+self.perx*70*self.scalelist[i])
        self.changecanvas(self.curid)
        bg.showimage()
    # 将日期转化为值
    def turnvalue(self,date):
        return (date[1]-1)*30 + date[2]
    # 绘制坐标轴
    def drawaxis(self,x):
        # x轴
        self.matcanvas.create_line(self.opointx,self.opointy,self.matwidth - self.opointx,self.opointy,fill='black')
        # y轴
        self.matcanvas.create_line(self.opointx, self.opointy,self.opointx,self.matheight-self.opointy,fill='black')
        if x==0:
            self.matcanvas.create_text(self.opointx-30,self.opointy-10,text=str(self.highpressurescale[0])+"mmHg",font=("宋体",10))
            self.matcanvas.create_text(self.opointx-30,self.matheight-self.opointy+22,text=str(self.highpressurescale[1])+"mmHg",font=("宋体",10))
            self.matcanvas.create_rectangle(self.opointx,self.highpressurey(self.safescalelist[0][1]),self.opointx+80*self.perx,self.highpressurey(self.safescalelist[0][0]),fill="yellowgreen",width=0)
            self.matcanvas.create_text(self.opointx+self.perx*40,(self.highpressurey(self.safescalelist[0][1])+self.highpressurey(self.safescalelist[0][0]))/2,text="健康范围",font=("宋体",40))
        if x==1:
            self.matcanvas.create_text(self.opointx-30,self.opointy-10,text=str(self.lowpressurescale[0])+"mmHg",font=("宋体",10))
            self.matcanvas.create_text(self.opointx-30,self.matheight-self.opointy+22,text=str(self.lowpressurescale[1])+"mmHg",font=("宋体",10))
            self.matcanvas.create_rectangle(self.opointx,self.lowpressurey(self.safescalelist[1][1]),self.opointx+80*self.perx,self.lowpressurey(self.safescalelist[1][0]),fill="yellowgreen",width=0)
            self.matcanvas.create_text(self.opointx+self.perx*40,(self.lowpressurey(self.safescalelist[1][1])+self.lowpressurey(self.safescalelist[1][0]))/2,text="健康范围",font=("宋体",40))
        if x==2:
            self.matcanvas.create_text(self.opointx-30,self.opointy-10,text=str(self.heartscale[0])+"次/分钟",font=("宋体",10))
            self.matcanvas.create_text(self.opointx-30,self.matheight-self.opointy+22,text=str(self.heartscale[1])+"次/分钟",font=("宋体",10))
            self.matcanvas.create_rectangle(self.opointx,self.pressurey(self.safescalelist[2][1]),self.opointx+80*self.perx,self.pressurey(self.safescalelist[2][0]),fill="yellowgreen",width=0)
            self.matcanvas.create_text(self.opointx+self.perx*40,(self.pressurey(self.safescalelist[2][1])+self.pressurey(self.safescalelist[2][0]))/2,text="健康范围",font=("宋体",40))
        for i in range(0,len(self.pressurelist)):
            self.matcanvas.create_text(self.xlist[i],self.opointy+25,text=str(self.datelist[i][1])+"月"+str(self.datelist[i][2])+"日",font=("宋体",10))
    # 给定低压，返回绘制y
    def lowpressurey(self,num):
        tempnum = (num - self.lowpressurescale[0])/self.lowpressurelength*self.yheight #y坐标值
        return self.turncanvasy(tempnum)
    # 给定高压，返回绘制y
    def highpressurey(self,num):
        tempnum = (num - self.highpressurescale[0])/self.highpressurelength*self.yheight #y坐标值
        return self.turncanvasy(tempnum)
    # 血压
    def pressurey(self,num):
        tempnum = (num - self.heartscale[0])/self.heartlength*self.yheight #y坐标值
        return self.turncanvasy(tempnum)
    # 给定y值，返回在canvas中应该的y值
    def turncanvasy(self,num):
        return self.opointy - num  
    # 返回函数
    def returnfun(self,x):
        return lambda:self.changecanvas(x)
    def changecanvas(self,x):
        self.curid = x
        self.matcanvas.delete("all")
        self.drawaxis(x)    
        if x==0:
            for n in range(0,len(self.pressurelist)):
                if n>0:
                    self.matcanvas.create_line(self.xlist[n-1],self.highpressurey(self.highpressurelist[n-1]),self.xlist[n],self.highpressurey(self.highpressurelist[n]),fill='red',width=self.linewidth)
                    self.matcanvas.create_oval(self.xlist[n-1]-self.pointradius,self.highpressurey(self.highpressurelist[n-1])-self.pointradius,self.xlist[n-1]+self.pointradius,self.highpressurey(self.highpressurelist[n-1])+self.pointradius,fill="red",width=0)            
            self.matcanvas.create_oval(self.xlist[-1]-self.pointradius,self.highpressurey(self.highpressurelist[-1])-self.pointradius,self.xlist[-1]+self.pointradius,self.highpressurey(self.highpressurelist[-1])+self.pointradius,fill="red",width=0)   
        if x==1:
            for n in range(0,len(self.pressurelist)):
                if n>0:
                    self.matcanvas.create_line(self.xlist[n-1],self.lowpressurey(self.lowpressurelist[n-1]),self.xlist[n],self.lowpressurey(self.lowpressurelist[n]),fill='yellow',width=self.linewidth)
                    self.matcanvas.create_oval(self.xlist[n-1]-self.pointradius,self.lowpressurey(self.lowpressurelist[n-1])-self.pointradius,self.xlist[n-1]+self.pointradius,self.lowpressurey(self.lowpressurelist[n-1])+self.pointradius,fill="yellow",width=0)
            self.matcanvas.create_oval(self.xlist[-1]-self.pointradius,self.lowpressurey(self.lowpressurelist[-1])-self.pointradius,self.xlist[-1]+self.pointradius,self.lowpressurey(self.lowpressurelist[-1])+self.pointradius,fill="yellow",width=0) 
        if x==2:
            for n in range(0,len(self.pressurelist)):
                if n>0:
                    self.matcanvas.create_line(self.xlist[n-1],self.pressurey(self.pressurelist[n-1]),self.xlist[n],self.pressurey(self.pressurelist[n]),fill='blue',width=self.linewidth)
                    self.matcanvas.create_oval(self.xlist[n-1]-self.pointradius,self.pressurey(self.pressurelist[n-1])-self.pointradius,self.xlist[n-1]+self.pointradius,self.pressurey(self.pressurelist[n-1])+self.pointradius,fill="blue",width=0)
            self.matcanvas.create_oval(self.xlist[-1]-self.pointradius,self.pressurey(self.pressurelist[-1])-self.pointradius,self.xlist[-1]+self.pointradius,self.pressurey(self.pressurelist[-1])+self.pointradius,fill="blue",width=0)
        self.refresh()      
    def refresh(self):
        for i in range(0,len(self.menubtnlist)):
            if i==self.curid:
                self.menubtnlist[i].config(image=self.switchimageablelist[i])
            else:
                self.menubtnlist[i].config(image=self.switchimagelist[i])
