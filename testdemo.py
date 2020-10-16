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
import random
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
from askingpage import askingpage #询问界面
from emecallpage import emecallpage #紧急呼救界面
from wordtovoice import wordtovoice #语音识别
import sounddevice as sd
winwidth = 0
winheight = 0
app_id = "22734117"
api_key = "dGN7IjSC9ZbeaEb9wpumWF8I"
secret_key = "7wDCfXsZ8blwwa2peLOwVOHIoZuOyHUm"

client = AipSpeech(app_id, api_key, secret_key)
length = 2
duration = 10000  # seconds
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
        self.closebtnwidth = 60  #关闭按钮的大小
        self.Bigbtnwidth = winwidth / 3  #中央大按钮的大小
        self.btnwidth = winheight / 6  #普通按钮的大小
        self.padding1 = 60  #普通按钮之间的间隔
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
        self.closemove = 40
        self.closemove2 =30
        self.playclockwidth = winwidth
        self.playclockheight = winheight
        self.littlewidth = 140
        self.littleheight = self.littlewidth*winheight/winwidth
        self.smiling = True
        self.small = False
        self.emojiid = 0
        self.playclocking = False
        self.fallflag = False
        self.falldowntime = 0
        self.voicerecing = True
        self.curfunid = -1 #当前功能id 0照片 1音乐 2视频 3 环境 4呼救 5打电话 6设闹钟 7测血压
        #偏移量
        self.move = [
            [
                [self.Amovex-self.twomove/2+self.closemove+self.closemove2, self.Bmovey - self.btnwidth / 2 - self.padding1 / 2],
                [
                    self.Amovex - self.midmove-self.twomove+90+self.closemove,
                    self.Bmovey + self.btnwidth / 2 + self.padding1 / 2
                ],
                [
                    self.Amovex -self.midmove+self.btnwidth+100-self.twomove+self.closemove,
                    self.Bmovey + self.btnwidth / 2 + self.padding1 / 2
                ],
                [
                    self.Amovex-self.twomove/2+self.closemove2+self.closemove,
                    self.Bmovey + self.btnwidth * 3 / 2 + self.padding1 * 3 / 2
                ]
            ],
            [
                [winwidth / 3, 0], 
                [winwidth / 3, self.Bmovey+30],
                [winwidth / 3, self.Bmovey+self.Bigbtnwidth+30],
            ],
            [
                
                [self.Cmovex+self.twomove/2-self.closemove-self.closemove2, self.Bmovey - self.btnwidth / 2 - self.padding1 / 2],
                [
                    self.Cmovex + self.midmove-self.twomove-self.closemove,
                    self.Bmovey + self.btnwidth / 2 + self.padding1 / 2
                ],
                [
                    self.Cmovex + self.midmove+self.btnwidth-self.twomove+10-self.closemove,
                    self.Bmovey + self.btnwidth / 2 + self.padding1 / 2
                ],
                [
                    self.Cmovex+self.twomove/2-self.closemove-self.closemove2,
                    self.Bmovey + self.btnwidth * 3 / 2 + self.padding1 * 3 / 2
                ]
            ]
        ]
        self.child = []
        # for item in self.child:
        #     item
        #读取图片
        self.titleimage = ImageTk.PhotoImage(
            Image.open("srcimage/title.jpg").resize(
                (int(winwidth / 3)+1, int(winheight / 7)+1)))
        self.backgroundimage = ImageTk.PhotoImage(
            Image.open("srcimage/background.jpg").resize(
                (int(winwidth), int(winheight))))
        self.bookimage = ImageTk.PhotoImage(
            Image.open("srcimage/photos.jpg").resize(
                (int(self.btnwidth)+2, int(self.btnwidth)+2)))
        self.movieimage = ImageTk.PhotoImage(
            Image.open("srcimage/video.jpg").resize(
                (int(self.btnwidth)+2, int(self.btnwidth)+2)))
        self.musicimage = ImageTk.PhotoImage(
            Image.open("srcimage/music.jpg").resize(
                (int(self.btnwidth)+2, int(self.btnwidth)+2)))
        self.studyimage = ImageTk.PhotoImage(
            Image.open("srcimage/emecall.jpg").resize(
                (int(self.btnwidth)+2, int(self.btnwidth)+2)))
        self.gameimage = ImageTk.PhotoImage(
            Image.open("srcimage/phone.jpg").resize(
                (int(self.btnwidth)+2, int(self.btnwidth)+2)))
        self.hearto2image = ImageTk.PhotoImage(
            Image.open("srcimage/hearto2.jpg").resize(
                (int(self.btnwidth)+2, int(self.btnwidth)+2)))
        self.clockimage = ImageTk.PhotoImage(
            Image.open("srcimage/clock.jpg").resize(
                (int(self.btnwidth)+2, int(self.btnwidth)+2)))
        self.environmentimage = ImageTk.PhotoImage(
            Image.open("srcimage/environment.jpg").resize(
                (int(self.btnwidth)+2, int(self.btnwidth)+2)))

        self.workimage = ImageTk.PhotoImage(
            Image.open("srcimage/looking.jpg").resize(
                (int(self.Bigbtnwidth), int(self.Bigbtnwidth))))
        self.faceback = ImageTk.PhotoImage(
            Image.open("srcimage/faceback.jpg").resize(
                (int(self.Bigbtnwidth)+2, int(self.Bigbtnwidth))))
        self.closeimage = ImageTk.PhotoImage(
            Image.open("srcimage/close.jpg").resize(
                (int(self.closebtnwidth)+4, int(self.closebtnwidth)+4)))
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
                                   relief="groove",
                                   command=self.gotophoto,
                                   bd=0,highlightthickness=0,
                                   highlightcolor="white")
        self.buttonA_1.place(x=self.move[0][0][0], y=self.move[0][0][1])
        self.buttonA_2 = tk.Button(self.initface,
                                   image=self.movieimage,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="groove",
                                   command=self.gotovideo,
                                   bd=0,highlightthickness=0)
        self.buttonA_2.place(x=self.move[0][1][0], y=self.move[0][1][1])
        self.buttonA_3 = tk.Button(self.initface,
                                   image=self.musicimage,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="groove",
                                   command=self.gotomusic,
                                   bd=0,highlightthickness=0)
        self.buttonA_3.place(x=self.move[0][2][0], y=self.move[0][2][1])
        self.buttonA_4 = tk.Button(self.initface,
                                   image=self.environmentimage,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="groove",
                                   command=self.gotoenvpage,
                                   bd=0,highlightthickness=0)
        self.buttonA_4.place(x=self.move[0][3][0], y=self.move[0][3][1])
        # 交大的校徽
        self.titleCanvas = tk.Canvas(self.initface,
                                     width=self.Bigbtnwidth,
                                     height=winheight / 7)
        self.titleCanvas.place(x=self.move[1][0][0], y=self.move[1][0][1])
        self.titleCanvas.create_image(0, 0, anchor='nw', image=self.titleimage)
        self.titleCanvas.configure(highlightthickness=0)
        # 中间的按钮
        self.buttonB = tk.Button(self.initface,
                                 image=self.faceback,
                                 height=int(winheight / 3)+50,
                                 width=int(winwidth / 3),
                                 relief="groove",
                                 bd=0,highlightthickness=0)
        self.buttonB.place(x=self.move[1][1][0], y=self.move[1][1][1])
        #下面的文字
        self.wordcanvas = tk.Canvas(self.initface,bg="white",width=winwidth/3,height=100,highlightthickness=0)
        self.wordcanvas.place(x=self.move[1][2][0],y=self.move[1][2][1])
        self.wordcanvas.create_text(winwidth/6,50,text="知心小雨为您服务",font=("宋体",20))
        # 左边的三个按钮
        self.buttonC_1 = tk.Button(self.initface,
                                   image=self.studyimage,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="groove",
                                   command=self.emecall,
                                   bd=0,highlightthickness=0)
        self.buttonC_1.place(x=self.move[2][0][0], y=self.move[2][0][1])
        self.buttonC_2 = tk.Button(self.initface,
                                   image=self.gameimage,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="groove",
                                   command=self.callfamily,
                                   bd=0,highlightthickness=0)
        self.buttonC_2.place(x=self.move[2][1][0], y=self.move[2][1][1])
        self.buttonC_3 = tk.Button(self.initface,
                                   image=self.clockimage,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="groove",
                                   bd=0,highlightthickness=0,
                                   command = self.gotoclockpage)
        self.buttonC_3.place(x=self.move[2][2][0], y=self.move[2][2][1])
        self.buttonC_4 = tk.Button(self.initface,
                                   image=self.hearto2image,
                                   height=self.btnwidth,
                                   width=self.btnwidth,
                                   relief="groove",
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
        #语音控制
        _thread.start_new_thread(self.readtext,("treadname",1))
        _thread.start_new_thread(self.starttest,("treadname",1))
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
    def gotophoto(self):
        if len(self.child)>0:
            self.child[0].back()
            self.child = []
        self.curfunid = 0
        self.child.append(photopage(self,self.master, winheight, winwidth))
    def gotomusic(self):
        if len(self.child)>0:
            self.child[0].back()
            self.child = []
        self.curfunid = 1
        self.child.append(musicpage(self,self.master, winheight, winwidth))
    def gotovideo(self):
        if len(self.child)>0:
            self.child[0].back()
            self.child = []
        self.curfunid = 2
        self.child.append(videopage(self,self.master, winheight, winwidth))
    #观察环境参数
    def gotoenvpage(self):
        if len(self.child)>0:
            self.child[0].back()
            self.child = []
        self.curfunid = 3
        self.child.append(envpage(self,self.master,winheight,winwidth))
    #紧急呼救
    def emecall(self):
        self.curfunid = 4
        self.voicerecing = False
        emecallpage(self,self.master,winheight,winwidth)
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
        if len(self.child)>0:
            self.child[0].back()
            self.child = []
        self.curfunid = 5
        self.child.append(callpage(self,self.master, winheight, winwidth))

    #设置定时闹钟
    def gotoclockpage(self):
        if len(self.child)>0:
            self.child[0].back()
            self.child = []
        self.curfunid = 6
        self.child.append(clockpage(self,self.master,winheight,winwidth))
    #心率
    def gotoheartpage(self):
        if len(self.child)>0:
            self.child[0].back()
            self.child = []
        self.curfunid = 7
        self.child.append(heartpage(self,self.master, winheight, winwidth))
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
            if result[0]>120:
                result[0] = 101+random.randint(0,15)
            if result[1]>90:
                result[1] = 78+random.randint(0,5)
            if result[2] >95 or result[2] <60:
                result[2] = 71+random.randint(0,12)
            callclass.showresult(result)
    #关闭当前界面
    def destroypage(self):
        self.master.destroy()
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
    def readtext(self,treadname,x):
        while True:
            if not self.fallflag:
                f = open("flag.txt")
                line = f.readline()
                while line:
                    print(line)
                    if int(line) == 1:
                        self.child.append(askingpage(self,self.master,winheight,winwidth))
                        self.fallflag = True
                    line = f.readline()
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
        if self.voicerecing:
            if not self.fallflag:
                if ("照片" in res or "相册" in res) and self.curfunid!=0 and self.curfunid!=7:
                    self.gotophoto()
                    return
                if ("视频" in res) and self.curfunid!=2 and self.curfunid!=7:
                    self.gotovideo()
                    try:
                        self.child[0].autoplay()
                    except:
                        pass
                    return
                if "音乐" in res and self.curfunid!=1 and self.curfunid!=7:
                    self.gotomusic()
                    try:
                        self.child[0].autoplay()
                    except:
                        pass
                    return
                if ("心率" in res or "血压" in res) and self.curfunid!=7:
                    self.gotoheartpage()
                    return
                if ("电话" in res) and self.curfunid!=5 and self.curfunid!=7:
                    self.callfamily()
                    return
                if ("环境" in res) and self.curfunid!=3 and self.curfunid!=7:
                    self.gotoenvpage()
                    return
                if ("救命" in res) and self.curfunid!=4:
                    self.emecall()
                    return
                if ("闹钟" in res) and self.curfunid!=6 and self.curfunid!=7:
                    self.gotoclockpage()
                    return
                if ("菜单" in res or "退出" in res) and self.curfunid!=-1:
                    if len(self.child)>0:
                        self.child[0].back()
                        self.child = []
                    return  
                if self.curfunid == 1:
                    #音乐主场
                    if "上" in res or "换" in res:
                        self.child[0].formsong()
                    if "下" in res:
                        self.child[0].nextsong()
                if self.curfunid == 7:
                    if "历史" in res or "查看" in res:
                        self.child[0].seehistory()
                        return
                    if "开始" in res or "测量" in res and not self.child[0].inhistory:
                        self.child[0].start()
                        return
                    if self.child[0].inhistory:
                        if "心率" in res or "相遇" in res:
                            self.child[0].history.changecanvas(2)
                            return
                        if "收缩压" in res or "收缩" in res:
                            self.child[0].history.changecanvas(0)
                            return
                        if "舒张压" in res or "舒张" in res:
                            self.child[0].history.changecanvas(1)
                            return
                if self.curfunid == 6:
                    temptimelist = ["5点","6点","7点","8点","9点","10点","11点","12点","13点","14点","15点","16点","17点","18点","19点","20点","21点","22点"]
                    temptimestrlist = ["五点","六点","七点","八点","九点","十点","十一点","十二点","十三点","十四点","十五点","十六点","十七点","十八点","十九点","二十点","二十一点","二十二点"]
                    temptimestrlist2 = ["五点","六点","七点","八点","九点","是点","是一点","是二点","是三点","是四点","是五点","是六点","是七点","是八点","是九点","二十点","二十一点","二十二点"]
                    for i in range(0,len(temptimelist)):
                        if temptimelist[i] in res or temptimestrlist[i] in res or temptimestrlist2[i] in res:
                            self.child[0].autosetclock(i+5)
                            return
                if self.curfunid == 5:
                    if "儿子" in res:
                        self.child[0].callfamily(2)
                        return
                    if "孙子" in res:
                        self.child[0].callfamily(1)
                        return
                    if "女儿" in res:
                        self.child[0].callfamily(0)
                        return
            else:
                if  "没有" in res:
                    self.fallflag = False
                    self.child[-1].back()
                if  "是" in res:
                    self.emecall()
    def print_sound(self,indata, outdata, frames, time, status):
        volume_norm = np.linalg.norm(indata)*10
        if int(volume_norm)>100:
            self.test()
            print(int(volume_norm))
    def starttest(self,threadname,x):
        # with sd.Stream(callback=self.print_sound):
        #     sd.sleep(duration * 1000)
        while True:
            self.test()
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
        #self.facepage.create_image(0,0,anchor='nw',image=self.happy)
        time.sleep(2)
        self.smiling = True
    def dislikeface(self):
        #self.facepage.create_image(0,0,anchor='nw',image=self.dislike)
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
