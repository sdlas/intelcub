import tkinter as tk
import tkinter.colorchooser
import pygame as py
import time
import _thread
from tkinter import *
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
        # self.testimage = ImageTk.PhotoImage(Image.open("srcimage/firstson.jpg").resize(
        #     (int(self.avatarwidth), int(self.avatrheight))))
        # self.test = tk.Button(self.callpage,image=self.testimage,width=self.avatarwidth,height=self.avatrheight,command=self.back)
        # self.test.place(x=0,y=0)
        for n in range(0,len(self.childlist)):
            self.avatarimagelist.append(ImageTk.PhotoImage(self.goodimage(self.childlist[n])))
            self.avatarlabellist.append(tk.Button(self.callpage,width=self.avatarwidth,height=self.avatrheight,image=self.avatarimagelist[n],command = self.back))
            self.avatarlabellist[n].place(x=self.avatarpadding+(self.avatarwidth+self.avatarpadding)*n,y=200)
        bg.showimage()
    #返回合适比例的图片
    def goodimage(self,str):
        tempimage = Image.open("srcimage/"+str+".jpg")
        imgwidth = tempimage.size[0]
        imgheight = tempimage.size[1]
        imgscale = imgwidth/imgheight
        tempimage = tempimage.resize((int(self.avatarwidth),int(self.avatarwidth/imgscale)))
        return tempimage
    # #返回图片适合的放置位置
    # def rightpos(self,id):
    #     tempimage = Image.open("photos/"+self.imagelist[id])
    #     imgwidth = tempimage.size[0]
    #     imgheight = tempimage.size[1]
    #     imgscale = imgwidth/imgheight
    #     posx = 0 
    #     posy = 0
    #     if imgscale<self.canvasscale:
    #         #将高度设置到最大
    #         tempimage = tempimage.resize((int(self.canvasheight*imgscale),int(self.canvasheight)))
    #         posy = 0
    #         posx = (self.canvaswidth-self.canvasheight*imgscale)/2
    #     else:
    #         #将宽度设置到最大
    #         posy = (self.canvasheight-self.canvaswidth/imgscale)/2
    #         posx = 0
    #         tempimage = tempimage.resize((int(self.canvaswidth),int(self.canvaswidth/imgscale)))
    #     return posx,posy
    def back(self):
        pass