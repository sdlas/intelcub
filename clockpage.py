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
class clockpage():
    def __init__(self,mainclass,matser,_winheight,_winwidth):
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.master = matser
        self.mainclass = mainclass
        self.clockpage = tk.Frame(self.master,bg="pink",height = self.winheight ,width =self.winwidth)
        self.clockpage.place(x=0,y=0)
        self.mainclass.tasklist = []
        self.f = open("doc/clockplan.txt")
        line = self.f.readline()
        while line:
            if int(line) != 0:
                templist = []
                line = self.f.readline().replace("\n", "")
                line = list(line.split(","))
                line = self.transint(line)
                templist.append(line)
                line = self.f.readline().replace("\n", "")
                if int(line) == 0:
                    line = False
                else:
                    line = True
                templist.append(line)
                line = self.f.readline().replace("\n","")
                line = list(line.split(","))
                line = self.transint(line)
                templist.append(line)
                self.mainclass.tasklist.append(templist)
                line = self.f.readline()
            else:
                self.mainclass.tasklist.append([int(line)])
                line = self.f.readline()
        self.f.close()
        self.taskstrlist = self.translist(self.mainclass.tasklist)
        self.topheight = 130 #顶部标题高度
        self.ypadding = 10
        self.xpadding = 20
        self.taskheight =(self.winheight - self.topheight - 8*self.ypadding)/3
        self.taskwidth = (self.winwidth - 6*self.xpadding)/2
        self.btnwidth = 50
        self.btnheight = 50
        self.btnpadding = 10
        self.btnlist = []
        self.detelebtnlist = []
        self.canvaslist = []
        self.addimage = ImageTk.PhotoImage(
            Image.open("srcimage/add.jpg").resize(
                (int(self.taskwidth), int(self.taskheight))))
        self.editimage = ImageTk.PhotoImage(
            Image.open("srcimage/edit.jpg").resize(
                (int(self.btnwidth), int(self.btnheight))))
        self.closeimage = ImageTk.PhotoImage(
            Image.open("srcimage/close.jpg").resize(
                (int(self.btnwidth), int(self.btnheight))))
        #背景
        bg = background(self.clockpage,self.winheight,self.winwidth,"call")
        #返回按钮
        backbtn(self.clockpage,self.winheight,self.winwidth)
        #标题
        title(self.clockpage,self.winheight,self.winwidth,"定时服药提醒")
        self.refresh()
        bg.showimage()
    def returntime(self,num):
        if len(str(num)) == 1:
            return "0"+str(num)
        else:
            return str(num)
    def returnfun(self,i):
        return lambda:self.setting(i)
    def returndetfun(self,i):
        return lambda:self.detting(i)
    def setting(self,x):
        editclock(self,self.clockpage,self.winheight,self.winwidth,x,self.mainclass.tasklist[x])
    def detting(self,x):
        self.mainclass.tasklist[x]=[0]
        self.refresh()
    def translist(self,l):
        resultlist = []
        for i in range(0,len(l)):
            tempstr = 0
            if l[i][0] !=0:
                templist = l[i]
                repeatstr = 0
                if templist[1]:
                    repeatstr = "重复"
                else:
                    repeatstr = "一次"
                daystrarr = ["周一","周二","周三","周四","周五","周六","周日"]
                daystr = ""
                if len(templist[2]) == 7:
                    daystr = "每天"
                else:
                    if len(templist[2])<3:
                        for item in templist[2]:
                            daystr = daystr + "、"+daystrarr[item]
                    else:
                        for i in range(0,3):
                            daystr = daystr + "、"+daystrarr[i]
                        daystr = daystr + ". . ." 
                    daystr = daystr[1:]
                tempstr = self.returntime(templist[0][0])+":"+self.returntime(templist[0][1])+"  "+repeatstr + "  "+ daystr
            resultlist.append(tempstr)
        return resultlist
    def setlist(self,x,message):
        self.mainclass.tasklist[x] = message
        self.refresh()
    def refresh(self):
        self.taskstrlist = self.translist(self.mainclass.tasklist)
        for i in range(0,len(self.canvaslist)):
            self.canvaslist[i].destroy()
        self.btnlist = []
        self.detelebtnlist = []
        self.canvaslist = []
        for i in range(0,len(self.mainclass.tasklist)):
            self.canvaslist.append(tk.Canvas(self.clockpage,width=self.taskwidth,height=self.taskheight,highlightthickness=0))
            self.canvaslist[i].place(x=self.xpadding*((i%2)*2+1) +(i%2)*self.taskwidth,y=self.topheight+self.taskheight*int(i/2)+self.ypadding*((int(i/2))*2+1))
            if self.mainclass.tasklist[i][0] != 0:
                self.canvaslist[i].create_text(self.taskwidth/2,self.taskheight/2,text=self.taskstrlist[i],font=("宋体",30))
                self.btnlist.append(tk.Button(self.canvaslist[i],image=self.editimage,width=self.btnwidth,height=self.btnheight,command=self.returnfun(i)))
                self.detelebtnlist.append(tk.Button(self.canvaslist[i],image=self.closeimage,width=self.btnwidth,height=self.btnheight,command=self.returndetfun(i)))
                self.btnlist[i].place(x=self.taskwidth-self.btnwidth-self.btnpadding,y=self.btnpadding)
                self.detelebtnlist[i].place(x=self.btnpadding,y=self.btnpadding)
            else:
                self.btnlist.append(tk.Button(self.canvaslist[i],image=self.addimage,width=self.taskwidth,height=self.taskheight,command=self.returnfun(i)))
                self.detelebtnlist.append(tk.Button(self.canvaslist[i],image=self.closeimage,width=self.btnwidth,height=self.btnheight,command=self.returndetfun(i)))
                self.btnlist[i].place(x=0,y=0)

    def transint(self,lists):
        temp = []
        for item in lists:
            temp.append(int(item))
        return temp
class editclock():
    def __init__(self,mainclass,master,_winheight,_winwidth,id,message):
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.id = id
        self.message = message
        self.mainclass = mainclass
        self.master = master
        self.hour = 8 # 时
        self.min = 0 # 分
        self.repeatflag = True #是否重复
        self.plusbtnwidth = 50
        self.paddingy = 200 #各垂直部分之间的间距
        self.topy = self.winheight/4
        self.sidex = 80
        self.paddingx = 30 #各水平方向的间距
        self.movey = [self.topy,self.topy+self.paddingy,self.topy+self.paddingy*2]
        self.labelwidth = 50
        self.boxwidth = int((self.winwidth-self.paddingx*7-self.sidex*2)/8)
        self.closepadding = 30
        #重复尺寸
        self.titlebtnwidth = 120
        self.titlebtnheight = 80
        self.btnwidth = 120
        self.btnheight = 60
        self.cfbtnwidth = 120
        self.cfbtnheight = 80
        self.movex = [
            [
                self.sidex,
                self.sidex + self.boxwidth + self.paddingx,
                self.sidex + (self.boxwidth + self.paddingx)*2,
                self.sidex + (self.boxwidth + self.paddingx)*3,
                self.sidex + (self.boxwidth + self.paddingx)*4,
                self.sidex + (self.boxwidth + self.paddingx)*5,
                self.sidex + (self.boxwidth + self.paddingx)*6,
                self.sidex + (self.boxwidth + self.paddingx)*7,
            ],
            [
                self.sidex,
                self.sidex + self.boxwidth + self.paddingx,
                self.sidex + (self.boxwidth + self.paddingx)*2,
                self.sidex + (self.boxwidth + self.paddingx)*3,
                self.sidex + (self.boxwidth + self.paddingx)*4,
                self.sidex + (self.boxwidth + self.paddingx)*5,
                self.sidex + (self.boxwidth + self.paddingx)*6,
                self.sidex + (self.boxwidth + self.paddingx)*7,
            ]
        ]
        self.dayimagelist = []
        self.dayimagenamelist = ["day1.jpg","day2.jpg","day3.jpg","day4.jpg","day5.jpg","day6.jpg","day7.jpg"]
        self.dayableimagelist = []
        self.dayableimagenamelist = ["day1able.jpg","day2able.jpg","day3able.jpg","day4able.jpg","day5able.jpg","day6able.jpg","day7able.jpg"]
        self.dayableflag = []
        for item in self.dayimagenamelist:
            self.dayimagelist.append(
                ImageTk.PhotoImage(
                    Image.open("srcimage/"+item).resize(
                        (int(self.btnwidth), int(self.btnheight))))
            )
            self.dayableflag.append(False)
        for item in self.dayableimagenamelist:
            self.dayableimagelist.append(
                ImageTk.PhotoImage(
                    Image.open("srcimage/"+item).resize(
                        (int(self.btnwidth), int(self.btnheight))))
            )
        
        if self.message[0]!=0:
            self.hour = self.message[0][0]
            self.min = self.message[0][1]
            self.repeatflag = self.message[1]
            for i in range(0,len(self.message[2])):
                self.dayableflag[self.message[2][i]] = True
        else:
            for i in range(0,len(self.dayableflag)):
                self.dayableflag[i] = True

        self.addimage = ImageTk.PhotoImage(
            Image.open("srcimage/addicon.jpg").resize(
                (int(self.plusbtnwidth), int(self.plusbtnwidth))))
        self.minusimage = ImageTk.PhotoImage(
            Image.open("srcimage/minus.jpg").resize(
                (int(self.plusbtnwidth), int(self.plusbtnwidth))))
        self.repeatimage = ImageTk.PhotoImage(
            Image.open("srcimage/repeat.jpg").resize(
                (int(self.titlebtnwidth), int(self.titlebtnheight))))
        self.neverimage = ImageTk.PhotoImage(
            Image.open("srcimage/never.jpg").resize(
                (int(self.titlebtnwidth), int(self.titlebtnheight))))
        self.confirmimage = ImageTk.PhotoImage(
            Image.open("srcimage/confirm.jpg").resize(
                (int(self.cfbtnwidth), int(self.cfbtnheight))))
        self.editpage = tk.Canvas(self.master,bg="pink",width=self.winwidth,height=self.winheight)
        self.editpage.place(x=0,y=0)
        #时间设置
        self.hourCanvas = tk.Canvas(self.editpage,width=self.boxwidth,height=self.boxwidth)
        self.hournumCanvas = tk.Canvas(self.editpage,width=self.boxwidth,height=self.boxwidth)
        self.addhourbtn = tk.Button(self.editpage,image=self.addimage,width=self.plusbtnwidth,height=self.plusbtnwidth,command=self.addhour)
        self.addhourbtn.place(x=self.movex[0][0]+(self.boxwidth-self.plusbtnwidth)/2+self.closepadding,y=self.movey[0]+(self.boxwidth-self.plusbtnwidth)/2)
        self.hournumCanvas.place(x=int(self.movex[0][1]),y=int(self.movey[0]))
        self.hournumCanvas.create_text(self.boxwidth/2,self.boxwidth/2,text=self.returntime(self.hour),font=("宋体",50))
        self.minushourbtn = tk.Button(self.editpage,image=self.minusimage,width=self.plusbtnwidth,height=self.plusbtnwidth,command=self.minushour)
        self.minushourbtn.place(x=self.movex[0][2]+(self.boxwidth-self.plusbtnwidth)/2-self.closepadding,y=self.movey[0]+(self.boxwidth-self.plusbtnwidth)/2)
        self.hourCanvas.place(x=int(self.movex[0][3]),y=int(self.movey[0]))
        self.hourCanvas.create_text(self.boxwidth/2,self.boxwidth/2,text="时",font=("宋体",50))

        self.addminbtn = tk.Button(self.editpage,image=self.addimage,width=self.plusbtnwidth,height=self.plusbtnwidth,command=self.addmin)
        self.addminbtn.place(x=self.movex[0][4]+(self.boxwidth-self.plusbtnwidth)/2+self.closepadding,y=self.movey[0]+(self.boxwidth-self.plusbtnwidth)/2)
        self.minnumCanvas = tk.Canvas(self.editpage,width=self.boxwidth,height=self.boxwidth)
        self.minnumCanvas.create_text(self.boxwidth/2,self.boxwidth/2,text=self.returntime(self.min),font=("宋体",50))
        self.minnumCanvas.place(x=int(self.movex[0][5]),y=int(self.movey[0]))
        self.minusminbtn = tk.Button(self.editpage,image=self.minusimage,width=self.plusbtnwidth,height=self.plusbtnwidth,command=self.minusmin)
        self.minusminbtn.place(x=self.movex[0][6]+(self.boxwidth-self.plusbtnwidth)/2-self.closepadding,y=self.movey[0]+(self.boxwidth-self.plusbtnwidth)/2)
        self.minCanvas = tk.Canvas(self.editpage,width=self.boxwidth,height=self.boxwidth)
        self.minCanvas.create_text(self.boxwidth/2,self.boxwidth/2,text="分",font=("宋体",50))
        self.minCanvas.place(x=int(self.movex[0][7]),y=int(self.movey[0]))

        #重复设置
        if self.repeatflag:
            self.btntitle = tk.Button(self.editpage,image=self.repeatimage,width=self.titlebtnwidth,height=self.titlebtnheight,command=self.chooserepeat)
        else:
            self.btntitle = tk.Button(self.editpage,image=self.neverimage,width=self.titlebtnwidth,height=self.titlebtnheight,command=self.chooserepeat)
        self.btntitle.place(x=self.movex[1][0]+(self.boxwidth-self.titlebtnwidth)/2,y=self.movey[1]+(self.boxwidth-self.titlebtnheight)/2)
        self.btnlist = []
        for i in range(0,len(self.dayimagenamelist)):
            if self.dayableflag[i]:
                self.btnlist.append(tk.Button(self.editpage,image=self.dayableimagelist[i],width=self.btnwidth,height=self.btnheight,command=self.returnfun(i)))
            else:
                self.btnlist.append(tk.Button(self.editpage,image=self.dayimagelist[i],width=self.btnwidth,height=self.btnheight,command=self.returnfun(i)))
            self.btnlist[i].place(x=self.movex[1][i+1]+(self.boxwidth-self.btnwidth)/2,y=self.movey[1]+(self.boxwidth-self.btnheight)/2)
        #确定按钮
        self.cfbtn = tk.Button(self.editpage,image=self.confirmimage,width=self.cfbtnwidth,height=self.cfbtnheight,command=self.confirm)
        self.cfbtn.place(x=(self.winwidth-self.cfbtnwidth)/2,y=self.movey[2])
    #对日期加减运算
    def addhour(self):
        self.hour = (self.hour + 1)%24
        self.refresh()
    def minushour(self):
        self.hour = (self.hour - 1)%24
        self.refresh()
        
    def addmin(self): 
        if (self.min+10)>=60:
            self.hour =(self.hour + 1)%24
        self.min = (self.min + 10)%60
        self.refresh()
    def minusmin(self):
        if (self.min-10)<0:
            self.hour =(self.hour - 1)%24
        self.min = (self.min - 10)%60
        self.refresh()
    def refresh(self):
        self.hournumCanvas.delete("all")
        self.hournumCanvas.create_text(self.boxwidth/2,self.boxwidth/2,text=self.returntime(self.hour),font=("宋体",50))
        self.minnumCanvas.delete("all")
        self.minnumCanvas.create_text(self.boxwidth/2,self.boxwidth/2,text=self.returntime(self.min),font=("宋体",50))
    #日期点击函数
    def choose(self,x):
        self.dayableflag[x] = not self.dayableflag[x]
        self.refreshrepeat()
    def returnfun(self,x):
        return lambda:self.choose(x)
    def refreshrepeat(self):
        for i in range(0,len(self.dayableflag)):
            if self.dayableflag[i]:
                self.btnlist[i].config(image=self.dayableimagelist[i])
            else:
                self.btnlist[i].config(image=self.dayimagelist[i])
    #重复点击
    def chooserepeat(self):
        self.repeatflag = not self.repeatflag
        if self.repeatflag:
            self.btntitle.config(image=self.repeatimage)
        else:
            self.btntitle.config(image=self.neverimage)
    def returntime(self,num):
        if len(str(num)) == 1:
            return "0"+str(num)
        else:
            return str(num)
    #确认
    def confirm(self):
        resultlist = []
        timelist = []
        daylist = []
        timelist.append(self.hour)
        timelist.append(self.min)
        for i in range(0,len(self.dayableflag)):
            if self.dayableflag[i]:
                daylist.append(i)
        repflag = self.repeatflag
        resultlist.append(timelist)
        resultlist.append(repflag)
        resultlist.append(daylist)
        self.mainclass.setlist(self.id,resultlist)
        self.mainclass.mainclass.pushinclock()
        self.editpage.destroy()