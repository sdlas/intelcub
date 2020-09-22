from mttkinter import mtTkinter as tk
import tkinter.colorchooser
import pygame as py
import time
import _thread
from tkinter import *
import cv2
from PIL import Image, ImageTk
import multiprocessing
import math
from backbtn import backbtn
from title import title
from background import background
import matplotlib.pyplot as plt

class hearto2page():
    def __init__(self,mainclass,matser,_winheight,_winwidth):
        self.mainclass = mainclass
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.master = matser
        self.hearto2page = tk.Frame(self.master,bg="pink",height = self.winheight ,width =self.winwidth)
        self.hearto2page.place(x=0,y=0)
        self.heartratescale = [0,150] #心跳速度范围
        self.heartratelength = self.heartratescale[1]-self.heartratescale[0]
        self.oxygenscale = [0,150] #血氧浓度范围
        self.oxygenlength = self.oxygenscale[1] - self.oxygenscale[0]
        #背景
        bg = background(self.hearto2page,self.winheight,self.winwidth,"call")
        #返回按钮
        backbtn(self.hearto2page,self.winheight,self.winwidth)
        #标题
        self.testbtn = tk.Button(self.hearto2page,bitmap="error",width=100,height=100,command = self.testbtn)
        self.testbtn.place(x=0,y=0)
        title(self.hearto2page,self.winheight,self.winwidth,"健康检测")
        self.paddingl = 200 #水平的间隙
        self.paddingv = 60 #竖直方向的间隙 
        self.matwidth = self.winwidth-self.paddingl*2
        self.matheight = self.winheight-self.paddingv*2
        self.perx = self.matwidth/100
        self.pery = self.matheight/100
        self.matcanvas = tk.Canvas(self.hearto2page,bg="white",width=self.matwidth,height=self.matheight)
        self.matcanvas.place(x=self.paddingl,y=self.paddingv)
        self.opointx = 10*self.perx
        self.opointy = 90*self.pery
        self.yheight = 80*self.pery
        self.xwidth = 80*self.perx
        self.drawaxis()#绘制坐标轴
        # 40,130
        # 85,100
        #bg.showimage()
        #self.updatecan()
        plt.ion()
        plt.figure(1)
    def testbtn(self):
        self.mainclass.startnewthread()
    def back(self):
        pass
    #绘制坐标轴
    def drawaxis(self):
        # x轴
        self.matcanvas.create_line(self.opointx,self.opointy,self.matwidth - self.opointx,self.opointy,fill='black')
        # y轴
        self.matcanvas.create_line(self.opointx, self.opointy,self.opointx,self.matheight-self.opointy,fill='black')
    #给定心跳速度，返回绘制y
    def hearty(self,num):
        tempnum = (num - self.heartratescale[0])/self.heartratelength*self.yheight #y坐标值
        return self.turncanvasy(tempnum)
    #给定血氧浓度，返回绘制y
    def oxygeny(self,num):
        tempnum = (num - self.oxygenscale[0])/self.oxygenlength*self.yheight #y坐标值
        return self.turncanvasy(tempnum)
    #给定y值，返回在canvas中应该的y值
    def turncanvasy(self,num):
        return self.opointy - num
    #根据列表中已有的点，绘制图像
    def drawline(self):
        print(self.mainclass.heartratelist)
        plt.plot(list(range(0,len(self.mainclass.heartratelist))),self.mainclass.heartratelist,c='r',ls='-', marker='o', mec='b',mfc='w')  ## 保存历史数据
        plt.plot(list(range(0,len(self.mainclass.oxygenlist))),self.mainclass.oxygenlist,c='y',ls='-', marker='o', mec='b',mfc='w')
        #plt.plot(t, np.sin(t), 'o')
        plt.pause(0.1)
        # #绘制心率图像
        # self.matcanvas.delete('all')
        # for n in range(0,len(self.mainclass.heartratelist)):
        #     if n>0:
        #         self.matcanvas.create_line(self.opointx+(n-1)*self.perx*8,self.hearty(self.mainclass.heartratelist[n-1]),self.opointx+n*self.perx*8,self.hearty(self.mainclass.heartratelist[n]),fill='red')
        # #绘制血氧图像
        # for n in range(0,len(self.mainclass.oxygenlist)):
        #     if n>0:
        #         self.matcanvas.create_line(self.opointx+(n-1)*self.perx*8,self.oxygeny(self.mainclass.oxygenlist[n-1]),self.opointx+n*self.perx*8,self.oxygeny(self.mainclass.oxygenlist[n]),fill='yellow')
        # self.drawaxis()       
    def wow(self):
        print("wow")
