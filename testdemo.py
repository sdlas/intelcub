import os
from mttkinter import mtTkinter as tk
import tkinter.colorchooser
import pygame as py
import numpy as np
import time
import _thread
from aip import AipSpeech
import serial
import array
import cv2
from PIL import Image, ImageTk
import multiprocessing
import math
from datetime import datetime
from videopage import videopage  #视频播放界面
from photopage import photopage  #相册界面
from musicpage import musicpage  #音乐界面
from callpage import callpage  #拨打电话界面
from hearto2page import hearto2page #血氧浓度检测
from heartpage import heartpage #心率测量
from clockpage import clockpage #定时服药
from envpage import envpage #环境监测
from playclockpage import playclockpage #闹钟播放
import sounddevice as sd
winwidth = 0
winheight = 0
app_id = "22734117"
api_key = "dGN7IjSC9ZbeaEb9wpumWF8I"
secret_key = "7wDCfXsZ8blwwa2peLOwVOHIoZuOyHUm"

client = AipSpeech(app_id, api_key, secret_key)
length = 2
duration = 50  # seconds
#今天会闹钟的时间
clocktime = []
#桌面
class basedesk():
    def __init__(self, master):
        self.root = master
        self.root.config()
        self.root.title('Base page')
        self.root.geometry(str(winwidth) + 'x' + str(winheight))
        initface(self.root)
        #littleface(self.root)


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
        self.btnwidth = winheight / 5  #普通按钮的大小
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
        self.twomove = 100
        self.playclockwidth = winwidth
        self.playclockheight = winheight
        self.littlewidth = 340
        self.littleheight = self.littlewidth*winheight/winwidth
        self.smiling = True
        self.small = False
        self.emojiid = 0
        self.playclocking = False
        #偏移量
        self.move = [
            [
                [self.Amovex-self.twomove/2, self.Bmovey - self.btnwidth / 2 - self.padding1 / 2],
                [
                    self.Amovex - self.midmove-self.twomove,
                    self.Bmovey + self.btnwidth / 2 + self.padding1 / 2
                ],
                [
                    self.Amovex -self.midmove+self.btnwidth+60-self.twomove,
                    self.Bmovey + self.btnwidth / 2 + self.padding1 / 2
                ],
                [
                    self.Amovex-self.twomove/2,
                    self.Bmovey + self.btnwidth * 3 / 2 + self.padding1 * 3 / 2
                ]
            ],
            [
                [winwidth / 3, 0], 
                [winwidth / 3, self.Bmovey],
                [winwidth / 3, self.Bmovey+self.Bigbtnwidth-90],
            ],
            [
                
                [self.Cmovex+self.twomove/2, self.Bmovey - self.btnwidth / 2 - self.padding1 / 2],
                [
                    self.Cmovex + self.midmove-self.twomove,
                    self.Bmovey + self.btnwidth / 2 + self.padding1 / 2
                ],
                [
                    self.Cmovex + self.midmove+self.btnwidth-self.twomove+60,
                    self.Bmovey + self.btnwidth / 2 + self.padding1 / 2
                ],
                [
                    self.Cmovex+self.twomove/2,
                    self.Bmovey + self.btnwidth * 3 / 2 + self.padding1 * 3 / 2
                ]
            ]
        ]
        self.child = []
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
        self.clockimage = ImageTk.PhotoImage(
            Image.open("srcimage/clock.jpg").resize(
                (int(self.btnwidth), int(self.btnwidth))))
        self.environmentimage = ImageTk.PhotoImage(
            Image.open("srcimage/environment.jpg").resize(
                (int(self.btnwidth), int(self.btnwidth))))

        self.workimage = ImageTk.PhotoImage(
            Image.open("srcimage/looking.jpg").resize(
                (int(self.Bigbtnwidth), int(self.Bigbtnwidth))))
        self.faceback = ImageTk.PhotoImage(
            Image.open("srcimage/faceback.jpg").resize(
                (int(self.Bigbtnwidth), int(self.Bigbtnwidth))))
        self.working0 = ImageTk.PhotoImage(
            Image.open("srcimage/working0.jpg").resize(
                (int(self.Bigbtnwidth), int(self.Bigbtnwidth))))
        self.working1 = ImageTk.PhotoImage(
            Image.open("srcimage/working1.jpg").resize(
                (int(self.Bigbtnwidth), int(self.Bigbtnwidth))))
        self.working2 = ImageTk.PhotoImage(
            Image.open("srcimage/working2.jpg").resize(
                (int(self.Bigbtnwidth), int(self.Bigbtnwidth))))
        self.working3 = ImageTk.PhotoImage(
            Image.open("srcimage/working3.jpg").resize(
                (int(self.Bigbtnwidth), int(self.Bigbtnwidth))))
        self.working4 = ImageTk.PhotoImage(
            Image.open("srcimage/working4.jpg").resize(
                (int(self.Bigbtnwidth), int(self.Bigbtnwidth))))
        self.working5 = ImageTk.PhotoImage(
            Image.open("srcimage/working5.jpg").resize(
                (int(self.Bigbtnwidth), int(self.Bigbtnwidth))))
        self.closeimage = ImageTk.PhotoImage(
            Image.open("srcimage/close.jpg").resize(
                (int(self.closebtnwidth), int(self.closebtnwidth))))
        self.playclockimage = ImageTk.PhotoImage(
            Image.open("srcimage/playclock.jpg").resize(
                (int(self.playclockwidth), int(self.playclockheight))))
        
        self.lsmile0 = ImageTk.PhotoImage(
            Image.open("srcimage/smile0.jpg").resize(
                (int(self.littlewidth), int(self.littleheight))))
        self.lsmile1 = ImageTk.PhotoImage(
            Image.open("srcimage/smile1.jpg").resize(
                (int(self.littlewidth), int(self.littleheight))))
        self.lsmile2 = ImageTk.PhotoImage(
            Image.open("srcimage/smile2.jpg").resize(
                (int(self.littlewidth), int(self.littleheight))))
        self.lsmile3 = ImageTk.PhotoImage(
            Image.open("srcimage/smile3.jpg").resize(
                (int(self.littlewidth), int(self.littleheight))))
        self.lhappy = ImageTk.PhotoImage(
            Image.open("srcimage/happy.jpg").resize(
                (int(self.littlewidth), int(self.littleheight))))
        self.ldislike = ImageTk.PhotoImage(
            Image.open("srcimage/dislike.jpg").resize(
                (int(self.littlewidth), int(self.littleheight))))
        # 右边的三个按钮
        self.buttonA_1 = tk.Button(self.initface,
                                   image=self.bookimage,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="ridge",
                                   command=self.gotophoto,
                                   bd=0,highlightthickness=0,
                                   highlightcolor="white")
        self.buttonA_1.place(x=self.move[0][0][0], y=self.move[0][0][1])
        self.buttonA_2 = tk.Button(self.initface,
                                   image=self.movieimage,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="ridge",
                                   command=self.gotovideo,
                                   bd=0,highlightthickness=0)
        self.buttonA_2.place(x=self.move[0][1][0], y=self.move[0][1][1])
        self.buttonA_3 = tk.Button(self.initface,
                                   image=self.musicimage,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="ridge",
                                   command=self.gotomusic,
                                   bd=0,highlightthickness=0)
        self.buttonA_3.place(x=self.move[0][2][0], y=self.move[0][2][1])
        self.buttonA_4 = tk.Button(self.initface,
                                   image=self.environmentimage,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="ridge",
                                   command=self.gotoenvpage,
                                   bd=0,highlightthickness=0)
        self.buttonA_4.place(x=self.move[0][3][0], y=self.move[0][3][1])
        # 交大的校徽
        self.titleCanvas = tk.Canvas(self.initface,
                                     width=self.Bigbtnwidth,
                                     height=winheight / 6)
        self.titleCanvas.place(x=self.move[1][0][0], y=self.move[1][0][1])
        self.titleCanvas.create_image(0, 0, anchor='nw', image=self.titleimage)
        self.titleCanvas.configure(highlightthickness=0)
        # 中间的按钮
        self.buttonB = tk.Button(self.initface,
                                 image=self.faceback,
                                 height=int(winheight / 2),
                                 width=int(winwidth / 3),
                                 relief="ridge",
                                 bd=0,highlightthickness=0)
        self.buttonB.place(x=self.move[1][1][0], y=self.move[1][1][1])
        #下面的文字
        self.wordcanvas = tk.Canvas(self.initface,bg="white",width=winwidth/3,height=200,highlightthickness=0)
        self.wordcanvas.place(x=self.move[1][2][0],y=self.move[1][2][1])
        self.wordcanvas.create_text(winwidth/6,100,text="知心小雨为您服务",font=("宋体",30))
        # 左边的三个按钮
        self.buttonC_1 = tk.Button(self.initface,
                                   image=self.studyimage,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="ridge",
                                   command=self.emecall,
                                   bd=0,highlightthickness=0)
        self.buttonC_1.place(x=self.move[2][0][0], y=self.move[2][0][1])
        self.buttonC_2 = tk.Button(self.initface,
                                   image=self.gameimage,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="ridge",
                                   command=self.callfamily,
                                   bd=0,highlightthickness=0)
        self.buttonC_2.place(x=self.move[2][1][0], y=self.move[2][1][1])
        self.buttonC_3 = tk.Button(self.initface,
                                   image=self.clockimage,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="ridge",
                                   bd=0,highlightthickness=0,
                                   command = self.gotoclockpage)
        self.buttonC_3.place(x=self.move[2][2][0], y=self.move[2][2][1])
        self.buttonC_4 = tk.Button(self.initface,
                                   image=self.hearto2image,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="ridge",
                                   bd=0,highlightthickness=0,
                                   command = self.gotoheartpage)
        self.buttonC_4.place(x=self.move[2][3][0], y=self.move[2][3][1])
        #关闭按钮
        self.closebtn = tk.Button(self.initface,
                                  image=self.closeimage,
                                  width=self.closebtnwidth,
                                  height=self.closebtnwidth,
                                  bd=0,
                                  command=self.destroypage)
        self.closebtn.place(x=winwidth - self.closebtnwidth, y=0)
        self.facepage = tk.Canvas(self.master,width = self.littlewidth,height=self.littleheight,highlightthickness=0)
        self.facepage.place(x=(winwidth-self.littlewidth)/2,y=(winheight-self.littleheight)/2+15)
        self.facepage.create_image(0,0,anchor='nw',image=self.lsmile0)
        self.playclock = tk.Canvas(self.initface,width=self.playclockwidth,height=self.playclockheight)
        self.playclock.create_image(0,0,anchor="nw",image=self.playclockimage)
        self.hearto2page = [] 
        self.tasklist = []
        self.readclock()
        #刷新显示图片
        #人工智障
        _thread.start_new_thread(self.playface,("threadname",1))
        #_thread.start_new_thread(self.readtext,("treadname",1))
        #_thread.start_new_thread(self.starttest,("treadname",1))
        #闹钟
        _thread.start_new_thread(self.clock,("threadname",1))
    def clock(self,threadname,p):
        while True:
            time_now=[time.localtime(time.time()).tm_hour,time.localtime(time.time()).tm_min]
            if time_now in clocktime:
                #开始打铃
                self.playclocking = True
                playclockpage(self.master,winheight,winwidth)
            time.sleep(1)
    def readclock(self):
        #闹钟内容读取
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
                self.tasklist.append(templist)
                line = self.f.readline()
            else:
                self.tasklist.append([int(line)])
                line = self.f.readline()
        self.f.close()
        self.pushinclock()
    #转换成今日要闹钟的时间
    def pushinclock(self):
        for i in range(0,len(self.tasklist)):
            templist = self.tasklist[i]
            if templist[0]!=0:
                day_Week = datetime.now().weekday()
                if day_Week in templist[2]:
                    if templist[0] not in clocktime:
                        clocktime.append(templist[0])
        self.writeclock()
    # 将时钟写入文件
    def writeclock(self):
        with open('doc/clockplan.txt','w') as file_handle:   # .txt可以不自己新建,代码会自动新建
            for i in range(0,len(self.tasklist)):
                templist = self.tasklist[i]
                if templist[0]!=0:
                    file_handle.write("1")     # 写入
                    file_handle.write('\n')         # 有时放在循环里面需要自动转行，不然会覆盖上一条数据
                    file_handle.write(str(templist[0][0])+","+str(templist[0][1]))
                    file_handle.write('\n')
                    if templist[1]:
                        file_handle.write("1")
                    else:
                        file_handle.write("0")
                    file_handle.write("\n")
                    string = ""
                    for item in templist[2]:
                        string = string+ str(item)+","
                    string = string[:-1]
                    file_handle.write(string)
                    file_handle.write("\n")
                else:
                    file_handle.write("0")
                    file_handle.write("\n")
    def transint(self,lists):
        temp = []
        for item in lists:
            temp.append(int(item))
        return temp
    def gotovideo(self):
        #self.initface.destroy()
        self.child.append(videopage(self.master, winheight, winwidth))

    def gotophoto(self,threadname = "threadname",x=1):
        #self.initface.destroy()
        self.child.append(photopage(self.master, winheight, winwidth))
        print("self.child===============================",len(self.child))

    def gotomusic(self):
        self.child.append(musicpage(self.master, winheight, winwidth))
    def gotohearto2(self):
        self.hearto2page.append(hearto2page(self,self.master,winheight,winwidth))
    #心率
    def gotoheartpage(self):
        self.child.append(heartpage(self,self.master, winheight, winwidth))
    #紧急呼救
    def emecall(self):
        #打开串口，波特率115200，无校验，停止位1，数据位8，连接超时2秒
        ser = serial.Serial("/dev/ttyS0",
                            115200,
                            parity='N',
                            stopbits=1,
                            bytesize=8,
                            timeout=2)

        #拨打电话
        # ser.write('ATD' + num + ';\n'.encode())
        ser.write('ATD18792858682;\n'.encode())

        #讀取返回字符串長度並打印
        serlen = ser.inWaiting()
        print(ser.read(serlen))
        
        #ser.write('AT+CLIP=1;\n'.encode())#开启来电显示功能
        #ser.write('ATA;\n'.encode())#接听来电

    def callfamily(self):
        callpage(self.master, winheight, winwidth)

    #设置定时闹钟
    def gotoclockpage(self):
        clockpage(self,self.master,winheight,winwidth)
    #观察环境参数
    def gotoenvpage(self):
        envpage(self.master,winheight,winwidth)
    #测血压
    def bloodpressuretest(self,callclass,theadname,name):
        #打开串口，波特率9600，无校验，停止位1，数据位8，连接超时2秒
        ser=serial.Serial("/dev/ttyUSB0", 9600, parity='N', stopbits=1, bytesize=8, timeout=5)

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
    def workinggif(self,treadname,x):
        flag = 0
        plus = True
        while True:
            if flag == 0:
                self.buttonB.config(image=self.working0)
            if flag == 1:
                self.buttonB.config(image=self.working1)
            if flag == 2:
                self.buttonB.config(image=self.working2)
            if flag == 3:
                self.buttonB.config(image=self.working3)
            if flag == 4:
                self.buttonB.config(image=self.working4)
            if flag == 5:
                self.buttonB.config(image=self.working5)
            if plus:
                flag = flag + 1
            else:
                flag = flag - 1
            if flag ==5:
                plus = False
            if flag ==0:
                plus = True
            time.sleep(0.2)
    def readtext(self,treadname,x):
        while True:
            with open('out.txt', 'r') as file_to_read:
                while True:
                    lines = file_to_read.readline() # 整行读取数据
                    if not lines:
                        break
                    print(lines)
            time.sleep(1)
    def test(self):
        os.system("arecord -d %d -r 16000 -c 1 -t wav -f S16_LE record.wav" %
            (length, ))
        with open("record.wav", 'rb') as fp:
            res = client.asr(fp.read(), 'wav', 16000, {
                'dev_pid': 1537,
            })
        res = res['result'][0]
        print(res)
        if "照片" in res:
            _thread.start_new_thread(self.gotophoto,("threadname",1))
            return
        if "视频" in res:
            self.gotovideo()
            return
        if "音乐" in res:
            self.gotomusic()
            return
        if "心率" in res:
            self.gotoheartpage()
            return
        if "电话" in res:
            self.callfamily()
            return
        if "退出" in res:
            self.child[0].back()
    def print_sound(self,indata, outdata, frames, time, status):
        volume_norm = np.linalg.norm(indata)*10
        if int(volume_norm)>100:
            self.test()
            print(int(volume_norm))
    def starttest(self,threadname,x):
        with sd.Stream(callback=self.print_sound):
            sd.sleep(duration * 1000)
    def playface(self,treadname,x):
        while True:
            self.smileface()
            if self.emojiid == 0:
                self.happyface()
            if self.emojiid == 1:
                self.dislikeface()
    def smileface(self):
        flag = 0
        plus = True
        while self.smiling:
            if flag ==0:
                self.facepage.create_image(0,0,anchor='nw',image=self.lsmile0)
            if flag ==1:
                self.facepage.create_image(0,0,anchor='nw',image=self.lsmile1)
            if flag ==2:
                self.facepage.create_image(0,0,anchor='nw',image=self.lsmile2)
            if flag ==3:
                self.facepage.create_image(0,0,anchor='nw',image=self.lsmile3)
            if plus:
                flag = flag + 1
            else:
                flag = flag - 1
            if flag == 0:
                plus = True
            if flag == 4:
                plus = False
            if plus:
                time.sleep(0.05)
            else:
                time.sleep(0.1)
            if flag == 1 and plus:
                time.sleep(3)          
    def happyface(self):
        self.facepage.create_image(0,0,anchor='nw',image=self.happy)
        time.sleep(2)
        self.smiling = True
    def dislikeface(self):
        self.facepage.create_image(0,0,anchor='nw',image=self.dislike)
        time.sleep(2)
        self.smiling = True
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
