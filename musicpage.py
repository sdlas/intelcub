import tkinter as tk
import tkinter.colorchooser
import pygame as py
import time
import _thread
from tkinter import *
import cv2
from PIL import Image, ImageTk
import multiprocessing
import os.path
import glob
from backbtn import backbtn #返回按钮
from title import title
from background import background
winheight = 0
winwidth = 0


class musicpage():
    def __init__(self, master, _winheight, _winwidth):

        #获取本地音乐文件
        self.extensionlist = ['mp3', 'flac']
        self.musiclist = []
        for extension in self.extensionlist:
            file_list = glob.glob('music/*.' + extension)  #返回一个列表
            for item in file_list:
                self.musiclist.append(item[6:])

        #尺寸变量
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.photopadding = self.winwidth / 128
        self.photoleftpadding = 500
        self.photowidth = self.winwidth - self.photopadding * 2 - self.photoleftpadding
        self.photoheight = 70
        self.photomovex = (self.winwidth - self.photowidth) / 2
        self.master = master
        self.musicreadlist = []
        self.topheight = 130  #顶部标题高度
        self.backbtnheight = self.topheight / 2
        self.backbtnwidth = self.backbtnheight
        self.backbtnpadding = self.topheight / 4  #顶部按钮的间距
        self.pausebtnwidth = 40
        self.pausebtnmovey = (self.photoheight - self.pausebtnwidth) / 2
        self.pausebtnmovex = self.photowidth - 30 - self.pausebtnwidth
        self.curid = -1
        self.pausemusicflag = False  #是否有音乐暂停
        self.pausemusicid = -1  #暂停的音乐id
        #读取图片
        self.backimg = ImageTk.PhotoImage(
            Image.open("srcimage/toleft.jpg").resize(
                (int(self.backbtnwidth), int(self.backbtnheight))))
        self.pauseimg = ImageTk.PhotoImage(
            Image.open("srcimage/pause.jpg").resize(
                (int(self.pausebtnwidth), int(self.pausebtnwidth))))
        self.playimg = ImageTk.PhotoImage(
            Image.open("srcimage/play.jpg").resize(
                (int(self.pausebtnwidth), int(self.pausebtnwidth))))
        self.musicpage = tk.Canvas(self.master,
                                     bg="pink",
                                     width=self.winwidth,
                                     height=self.winheight)
        self.musicpage.place(x=0, y=0)
        self.musicpage.configure(highlightthickness=0)
         #背景
        bg = background(self.musicpage,self.winheight,self.winwidth,"call")
        #返回按钮
        backbtn(self.musicpage,self.winheight,self.winwidth)
        #标题
        title(self.musicpage,self.winheight,self.winwidth,"播放音乐")
        self.Canvaslist = []
        self.pausebtnlist = []
        #图片缩略图放置
        for n in range(0, len(self.musiclist)):
            self.Canvaslist.append(
                tk.Canvas(self.musicpage,
                          bg="white",
                          width=int(self.photowidth),
                          height=int(self.photoheight)))
            self.Canvaslist[n].place(
                x=self.photomovex,
                y=n * (self.photoheight + self.photopadding) + self.topheight)
            self.Canvaslist[n].create_text(self.photowidth / 2,
                                           self.photoheight / 2,
                                           text=self.resolvestr(self.musiclist[n])[0],
                                           font=("黑体", 25))
            self.pausebtnlist.append(
                tk.Button(self.Canvaslist[n],
                          image=self.playimg,
                          width=self.pausebtnwidth,
                          height=self.pausebtnwidth,
                          command=self.returnfun(n)))
            self.pausebtnlist[n].place(x=self.pausebtnmovex,
                                       y=self.pausebtnmovey)
        bg.showimage()
    def back(self):
        try:
            py.mixer.music.stop()
        except:
            pass
        self.musicpage.destroy()
        #self.vbar.destory()

    #选中要播放的音乐
    def choosemusic(self, x):
        if x == self.curid:
            #暂停正在播放的歌曲
            self.curid = -1
            self.pausebtnlist[x].config(image=self.playimg)
            self.pausemusic(x)
            return
        self.curid = x
        for n in range(0, len(self.pausebtnlist)):
            #
            if n != self.curid:
                self.pausebtnlist[n].config(image=self.playimg)
            else:
                self.pausebtnlist[n].config(image=self.pauseimg)
                if self.pausemusicflag and self.pausemusicid == self.curid:
                    self.unpausemusic()
                else:
                    _thread.start_new_thread(self.playmusic, ("Thread", x))

    #返回函数
    def returnfun(self, x):
        return lambda: self.choosemusic(x)

    #播放音乐
    def playmusic(self, threadname, x):
        #切换歌曲要恢复设置
        self.pausemusicflag = False
        self.pausemusicid = -1
        filepath = "music/" + self.musiclist[x]
        py.mixer.init()
        # 加载音乐
        py.mixer.music.load(filepath)
        py.mixer.music.play(loops=-1, start=0.0)
        #播放时长，没有此设置，音乐不会播放，会一次性加载完
        time.sleep(300)
        py.mixer.music.stop()
        #播放完后根据循环方式选择播放方式播放歌曲\

    #暂停音乐
    def pausemusic(self, x):
        self.pausemusicid = x
        self.pausemusicflag = True
        py.mixer.music.pause()

    #恢复播放
    def unpausemusic(self):
        self.pausemusicflag = False
        py.mixer.music.unpause()
    #将字符串处理成可用数据
    def resolvestr(self,_str):
        array = _str.split('.')
        arrayr = []
        for item in array:
            arrayr.append(item)
        return arrayr
    