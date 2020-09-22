import os
os.system("./hello.sh")
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
from videopage import videopage  #视频播放界面
from photopage import photopage  #相册界面
from musicpage import musicpage  #音乐界面
from callpage import callpage  #拨打电话界面
from hearto2page import hearto2page #血氧浓度检测
from heartpage import heartpage #心率测量
winwidth = 0
winheight = 0


#桌面
class basedesk():
    def __init__(self, master):
        self.root = master
        self.root.config()
        self.root.title('Base page')
        self.root.geometry(str(winwidth) + 'x' + str(winheight))

        initface(self.root)


#初始界面
class initface():
    def __init__(self, master):
        self.master = master
        #基准界面initface
        self.initface = tk.Canvas(self.master,
                                  bg="white",
                                  width=winwidth,
                                  height=winheight)
        self.initface.pack()
        self.initface.configure(highlightthickness=0)
        #常量定义
        self.closebtnwidth = 70  #关闭按钮的大小
        self.Bigbtnwidth = winwidth / 3  #中央大按钮的大小
        self.btnwidth = winheight / 4  #普通按钮的大小
        self.padding1 = 40  #普通按钮之间的间隔
        self.midlength = winwidth * 9 / 24
        self.sidelength = winwidth * 15 / 48
        self.tomid = 50
        self.Amovex = winwidth / 3 - self.padding1 - self.btnwidth - self.tomid
        self.Bmovey = winheight / 4
        self.Cmovex = winwidth * 2 / 3 + self.padding1 + self.tomid
        self.midmove = 60  #中间层按钮偏移量
        self.heartratelist = [80,90,69,110,102,79] #心跳速度列表
        self.oxygenlist = [89,90,98,96,87,92] #血氧浓度列表
        #偏移量
        self.move = [
            [self.Amovex, self.Bmovey - self.btnwidth / 2 - self.padding1 / 2],
            [
                self.Amovex - self.midmove,
                self.Bmovey + self.btnwidth / 2 + self.padding1 / 2
            ],
            [
                self.Amovex,
                self.Bmovey + self.btnwidth * 3 / 2 + self.padding1 * 3 / 2
            ], [winwidth / 3, 0], [winwidth / 3, self.Bmovey],
            [self.sidelength, winheight * 5 / 6],
            [self.Cmovex, self.Bmovey - self.btnwidth / 2 - self.padding1 / 2],
            [
                self.Cmovex + self.midmove,
                self.Bmovey + self.btnwidth / 2 + self.padding1 / 2
            ],
            [
                self.Cmovex,
                self.Bmovey + self.btnwidth * 3 / 2 + self.padding1 * 3 / 2
            ]
        ]
        #读取图片
        self.titleimage = ImageTk.PhotoImage(
            Image.open("srcimage/title.jpg").resize(
                (int(winwidth / 3), int(winheight / 6))))
        self.backgroundimage = ImageTk.PhotoImage(
            Image.open("srcimage/background.jpg").resize(
                (int(winwidth), int(winheight))))
        self.bookimage = ImageTk.PhotoImage(
            Image.open("srcimage/photos.jpg").resize(
                (int(self.btnwidth), int(self.btnwidth))))
        self.movieimage = ImageTk.PhotoImage(
            Image.open("srcimage/video.jpg").resize(
                (int(self.btnwidth), int(self.btnwidth))))
        self.musicimage = ImageTk.PhotoImage(
            Image.open("srcimage/music.jpg").resize(
                (int(self.btnwidth), int(self.btnwidth))))
        self.studyimage = ImageTk.PhotoImage(
            Image.open("srcimage/emecall.jpg").resize(
                (int(self.btnwidth), int(self.btnwidth))))
        self.gameimage = ImageTk.PhotoImage(
            Image.open("srcimage/phone.jpg").resize(
                (int(self.btnwidth), int(self.btnwidth))))
        self.hearto2image = ImageTk.PhotoImage(
            Image.open("srcimage/hearto2.jpg").resize(
                (int(self.btnwidth), int(self.btnwidth))))
        self.workimage = ImageTk.PhotoImage(
            Image.open("srcimage/looking.jpg").resize(
                (int(self.Bigbtnwidth), int(self.Bigbtnwidth))))
        self.closeimage = ImageTk.PhotoImage(
            Image.open("srcimage/close.jpg").resize(
                (int(self.closebtnwidth), int(self.closebtnwidth))))
        # 右边的三个按钮
        self.buttonA_1 = tk.Button(self.initface,
                                   image=self.bookimage,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="ridge",
                                   command=self.gotophoto,
                                   bd=0)
        self.buttonA_1.place(x=self.move[0][0], y=self.move[0][1])
        self.buttonA_2 = tk.Button(self.initface,
                                   image=self.movieimage,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="ridge",
                                   command=self.gotovideo,
                                   bd=0)
        self.buttonA_2.place(x=self.move[1][0], y=self.move[1][1])
        self.buttonA_3 = tk.Button(self.initface,
                                   image=self.musicimage,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="ridge",
                                   command=self.gotomusic,
                                   bd=0)
        self.buttonA_3.place(x=self.move[2][0], y=self.move[2][1])
        # 交大的校徽
        self.titleCanvas = tk.Canvas(self.initface,
                                     width=self.Bigbtnwidth,
                                     height=winheight / 6)
        self.titleCanvas.place(x=self.move[3][0], y=self.move[3][1])
        self.titleCanvas.create_image(0, 0, anchor='nw', image=self.titleimage)
        self.titleCanvas.configure(highlightthickness=0)
        # 中间的按钮
        self.buttonB = tk.Button(self.initface,
                                 image=self.workimage,
                                 height=int(winheight / 2),
                                 width=int(winwidth / 3),
                                 relief="ridge")
        self.buttonB.place(x=self.move[4][0], y=self.move[4][1])
        # 左边的三个按钮
        self.buttonC_1 = tk.Button(self.initface,
                                   image=self.studyimage,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="ridge",
                                   command=self.emecall,
                                   bd=0)
        self.buttonC_1.place(x=self.move[6][0], y=self.move[6][1])
        self.buttonC_2 = tk.Button(self.initface,
                                   image=self.gameimage,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="ridge",
                                   command=self.callfamily,
                                   bd=0)
        self.buttonC_2.place(x=self.move[7][0], y=self.move[7][1])
        self.buttonC_3 = tk.Button(self.initface,
                                   image=self.hearto2image,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="ridge",
                                   bd=0,
                                   command = self.gotoheartpage)
        self.buttonC_3.place(x=self.move[8][0], y=self.move[8][1])
        #关闭按钮
        self.closebtn = tk.Button(self.initface,
                                  image=self.closeimage,
                                  width=self.closebtnwidth,
                                  height=self.closebtnwidth,
                                  bd=0,
                                  command=self.destroypage)
        self.closebtn.place(x=winwidth - self.closebtnwidth, y=0)
        self.hearto2page = [] 
        #刷新显示图片
        self.showtitle()
        

    def gotovideo(self):
        #self.initface.destroy()
        videopage(self.master, winheight, winwidth)

    def gotophoto(self):
        #self.initface.destroy()
        photopage(self.master, winheight, winwidth)

    def gotomusic(self):
        musicpage(self.master, winheight, winwidth)
    def gotohearto2(self):
        self.hearto2page.append(hearto2page(self,self.master,winheight,winwidth))
    #心率
    def gotoheartpage(self):
        heartpage(self,self.master, winheight, winwidth)
    #紧急呼救
    def emecall(self, event):
        #打开串口，波特率115200，无校验，停止位1，数据位8，连接超时2秒
        ser = serial.Serial("/dev/ttyS0",
                            115200,
                            parity='N',
                            stopbits=1,
                            bytesize=8,
                            timeout=2)

        #拨打电话
        ser.write('ATD' + num + ';\n'.encode())

        #讀取返回字符串長度並打印
        serlen = ser.inWaiting()
        print(ser.read(serlen))

    def callfamily(self):
        callpage(self.master, winheight, winwidth)

    def showtitle(self):
        def video_loop():
            try:
                while True:
                    self.initface.create_image(0,
                                               0,
                                               anchor='nw',
                                               image=self.backgroundimage)
                    self.titleCanvas.create_image(0,
                                                  0,
                                                  anchor='nw',
                                                  image=self.titleimage)

                    self.master.update_idletasks()  #最重要的更新是靠这两句来实现
                    self.master.update()
            except:
                pass

        video_loop()
        #self.face1.mainloop()
    #测血压
    def bloodpressuretest(self,callclass,theadname,name):
        #打开串口，波特率9600，无校验，停止位1，数据位8，连接超时2秒
        ser=serial.Serial("/dev/ttyUSB2", 9600, parity='N', stopbits=1, bytesize=8, timeout=5)

        #开始测量
        ser.write('AT+ST:1\r\n'.encode())
        time.sleep(15)
        #等待测量完成后读取数据，取最后U1开头即可
        flag = False
        for item in ser.readlines():
            string = bytes.decode(item)
            if string[1] == "1":
                #此时输出数据有效
                flag = True
                result = self.resolvestr2(string[3:])
                break
        if not flag:
            result="false"
            callclass.showbadresult()
        else:
            callclass.showresult(result)
    #关闭当前界面
    def destroypage(self):
        self.master.destroy()
    #开启多线程
    def startnewthread(self):
        _thread.start_new_thread(self.printnum,("threadname",1))
        _thread.start_new_thread(self.drawline,("threadname2",1))
    #读取数据，刷新显示
    def printnum(self,str,x):
        while(1):
            #獲取字符串長度
            serlen = ser.inWaiting()
            #打印字符串
            string = bytes.decode(ser.read(serlen))
            arr = self.resolvestr(string)
            if arr[0]!=-1:
                self.heartratelist.append(arr[0])
                self.oxygenlist.append(arr[1])
            else:
                if len(self.heartratelist)>0:
                    self.heartratelist.append(self.heartratelist[-1])
                    self.oxygenlist.append(self.oxygenlist[-1])
            #程序延時1s
            time.sleep(1)
    def drawline(self,str,x):
        while(1):
            self.hearto2page[0].drawline()
            time.sleep(1)
    #将字符串处理成可用数据
    def resolvestr(self,_str):
        array = _str.split(',')
        arrayr = []
        for item in array:
            try:
                item = int(item)
            except:
                item = -1
            arrayr.append(item)
        return arrayr
    def resolvestr2(self,_str):
        array = _str.split(',')
        arrayr = []
        for item in array:
            try:
                item = int(item)
            except:
                pass
            arrayr.append(item)
        return arrayr

def start(threadname,x):
    os.system("./hello.sh")
if __name__ == '__main__':
    #_thread.start_new_thread(start,("threadname",1))
    root = tk.Tk()
    #全屏应用
    root.attributes("-fullscreen", True)
    # 串口初始化
    #ser=serial.Serial('COM6',115200,parity='N',stopbits=1,bytesize=8,timeout=10)
    #获取宽高
    winwidth = root.winfo_screenwidth()
    winheight = root.winfo_screenheight()
    basedesk(root)
    root.mainloop()

# root = tk.Tk()

# img_png = tkinter.PhotoImage(file = 'banana.gif')
# label_img = tkinter.Label(root, image = img_png)
# label_img.pack()
# root.mainloop()