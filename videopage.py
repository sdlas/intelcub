from mttkinter import mtTkinter as tk
import tkinter.colorchooser
import pyglet
import sys
import pygame
import time
import _thread
import threading
from threading import Thread
from tkinter import *
import cv2
from PIL import Image, ImageTk
import multiprocessing
from moviepy.editor import*
import os.path
import os
import glob
from backbtn import backbtn #返回按钮
from title import title
from background import background

window_width=960
window_height=620
image_width=320
image_height=int(window_height*1)
imagepos_x=0
imagepos_y=0
butpos_x=450
butpos_y=450
class videopage():
    def __init__(self,master,_winheight,_winwidth):
        self.extensionlist = ['mp4']
        self.videolist = []
        for extension in self.extensionlist:
            file_list = glob.glob('videos/*.' + extension)  #返回一个列表
            for item in file_list:
                self.videolist.append(item[6:])
        self.master = master
        self.master.config(bg='blue')
        self.playing = False #当前是否有视频正在播放
        # 屏幕宽高
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.videowidth = self.winwidth/8
        self.videopadding = self.winwidth/64
        self.topheight = 130 #顶部标题高度
        self.firstimagelist = []
        for n in range(0,len(self.videolist)):
            self.firstimagelist.append(self.getfirstimage(self.videolist[n]))
        # 获取每个视频的第一张图
        # 视频集画框
        self.videocanvas = tk.Canvas(self.master,bg="pink",height=self.winheight,width=self.winwidth)
        self.videocanvas.place(x=0,y=0)
        #背景
        bg = background(self.videocanvas,self.winheight,self.winwidth,"call")
        #返回按钮
        backbtn(self.videocanvas,self.winheight,self.winwidth)
        #标题
        title(self.videocanvas,self.winheight,self.winwidth,"播放视频")
        # 视频缩略图放置
        for n in range(0,len(self.videolist)):
            locals()['self.tempbutton'+str(n)] = tk.Button(self.videocanvas,image=self.firstimagelist[n], width=self.videowidth,height=self.videowidth,command=self.returnfun(n),bd=0)
            locals()['self.tempbutton'+str(n)].place(x=n%7*(self.videowidth+self.videopadding)+self.videopadding,y=int((n+1)/8)*(self.videowidth+self.videopadding)+self.topheight)
        bg.showimage()
    # 按钮点击响应函数
    def playvideo(self,x):
        self.showpygletvideo(self.videolist[x])
        #showvideo(self.videopage,x,self.winheight,self.winwidth)
    def returnfun(self,x):
        return lambda:self.playvideo(x)
    #图像转换，用于在画布中显示
    def tkImage(self,vc):
        ref,frame = vc.read()
        cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pilImage = Image.fromarray(cvimage)
        pilImage = pilImage.resize((image_width, image_height),Image.ANTIALIAS)
        tkImage =  ImageTk.PhotoImage(image=pilImage)
        return tkImage
    #获取每个视频的第一张图片
    def getfirstimage(self,str):
        vc = cv2.VideoCapture('videos/'+str)
        ref,frame = vc.read()
        cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pilImage = Image.fromarray(cvimage)
        imgwidth = pilImage.size[0]
        imgheight = pilImage.size[1]
        imgscale = imgwidth/imgheight
        if imgscale > 1:
            #将高度设置到最大
            pilImage = pilImage.resize((int(self.videowidth*imgscale),int(self.videowidth)))
        else:
            #将宽度设置到最大
            pilImage = pilImage.resize((int(self.videowidth),int(self.videowidth/imgscale)))
        tkImage =  ImageTk.PhotoImage(image=pilImage)
        return tkImage
    #图像的显示与更新
    def video(self,):
        def video_loop():
            try:
                while True:
                    picture1=self.tkImage(self.vc1)
                    self.canvas1.create_image(0,0,anchor='nw',image=picture1)  
                    #canvas4.create_image(0,0,anchor='nw',image=picture1) 
                    self.videopage.update_idletasks()  #最重要的更新是靠这两句来实现
                    self.videopage.update()
            except:
                self.back()
            
        video_loop()
        #self.face1.mainloop()
        self.vc1.release()
        cv2.destroyAllWindows()
    def back(self):
        self.videocanvas.destroy()
    def showpygletvideo(self,name):
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
        pygame.display.set_mode((640,480),1300,32)
        clip = VideoFileClip('videos/'+name)
        self.playing = True
        clip.preview()
        pygame.quit()
    def quitpygame(self):
        pygame.quit()
# class showvideo():
#     def __init__(self,master,id,_winheight,_winwidth):
#         #常量定义
#         self.winheight = _winheight
#         self.winwidth = _winwidth
#         self.curid = id
#         self.master = master
#         self.videoscreen = tk.Canvas(self.master,bg="pink",width=self.winwidth,height=self.winheight)
#         self.videoscreen.configure(highlightthickness=0)
#         self.videoscreen.place(x=0,y=0)
#         self.paddingl = 200 #水平的间隙
#         self.paddingv = 60 #竖直方向的间隙 
#         self.canvaswidth = self.winwidth-self.paddingl*2
#         self.canvasheight = self.winheight-self.paddingv*2
#         self.canvasscale = self.canvaswidth/self.canvasheight
#         self.pointbtnwidth = 100 #切换图片按钮的大小
#         self.pointbtnpadding = 50 #按钮的间距
#         self.closebtnwidth = 50 #关闭按钮的大小
#         self.closebtnpadding =30 #关闭按钮的间距
#         self.rightimg = ImageTk.PhotoImage(Image.open("srcimage/toright.jpg").resize((int(self.pointbtnwidth),int(self.pointbtnwidth))))  
#         self.leftimg = ImageTk.PhotoImage(Image.open("srcimage/toleft.jpg").resize((int(self.pointbtnwidth),int(self.pointbtnwidth))))  
#         self.closeimg = ImageTk.PhotoImage(Image.open("srcimage/close.jpg").resize((int(self.closebtnwidth),int(self.closebtnwidth)))) 

        
#         # self.showimg =  ImageTk.PhotoImage(self.goodimage(id))
#         # self.pos = self.rightpos(id) 
#         #显示视频的地方
#         self.showvideocanvas = tk.Canvas(self.videoscreen,bg="pink" ,width=self.canvaswidth,height = self.canvasheight)
#         self.showvideocanvas.place(x=self.paddingl,y=self.paddingv)
#         self.showvideocanvas.configure(highlightthickness=0)
#         #显示按钮
#         self.rightbtn = tk.Button(self.videoscreen,image=self.rightimg,width=self.pointbtnwidth,height=self.pointbtnwidth,command=self.changeright)
#         self.leftbtn = tk.Button(self.videoscreen,image=self.leftimg,width=self.pointbtnwidth,height=self.pointbtnwidth,command=self.changeleft)
#         self.leftbtn.place(x=self.pointbtnpadding,y=self.winheight/2-self.pointbtnwidth/2)
#         self.rightbtn.place(x=self.winwidth-self.pointbtnpadding-self.pointbtnwidth,y=self.winheight/2-self.pointbtnwidth/2)
#         #关闭按钮
#         self.closebtn = tk.Button(self.videoscreen,image=self.closeimg,width=self.closebtnwidth,height=self.closebtnwidth,command=self.close)
#         self.closebtn.place(x=self.winwidth-self.closebtnwidth-self.closebtnpadding,y=self.closebtnpadding)
        
#         #准备播放视频
#         self.vc1 =  cv2.VideoCapture('videos/'+videolist[self.curid])
#         self.pos = self.rightpos(self.vc1)
#         # video = VideoFileClip('videos/video5.mp4') 
#         # audio = video.audio 
#         # audio.write_audiofile('video5.mp3')
#         # videoplay = threading.Thread(target=self.video, args=(10,12))
#         # audioplay = threading.Thread(target=self.audio, args=(10,12))
#         # audioplay.daemon = True
#         # videoplay.daemon = True
#         # audioplay.start()
#         # self.video(10,12)
#         #audioplay.start()
#         _thread.start_new_thread( self.video, ("Thread", 0))
#          #_thread.start_new_thread(self.video,("Thread2",0))
#     def changeright(self):
#         pass
#     def changeleft(self):
#         pass
#     def close(self):
#         self.videoscreen.destroy()
#         pass
#     #图像转换，用于在画布中显示
#     def tkImage(self,vc):
#         ref,frame = vc.read()
#         cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         pilImage = Image.fromarray(cvimage)
#         imgwidth = pilImage.size[0]
#         imgheight = pilImage.size[1]
#         imgscale = imgwidth/imgheight
#         if imgscale<self.canvasscale:
#             #将高度设置到最大
#             pilImage = pilImage.resize((int(self.canvasheight*imgscale),int(self.canvasheight)))
#         else:
#             #将宽度设置到最大
#             pilImage = pilImage.resize((int(self.canvaswidth),int(self.canvaswidth/imgscale)))
#         tkImage =  ImageTk.PhotoImage(image=pilImage)
#         return tkImage
#     def rightpos(self,vc):
#         ref,frame = vc.read()
#         cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         pilImage = Image.fromarray(cvimage)
#         imgwidth = pilImage.size[0]
#         imgheight = pilImage.size[1]
#         imgscale = imgwidth/imgheight
#         posx = 0 
#         posy = 0
#         if imgscale<self.canvasscale:
#             #将高度设置到最大
#             pilImage = pilImage.resize((int(self.canvasheight*imgscale),int(self.canvasheight)))
#             posy = 0
#             posx = (self.canvaswidth-self.canvasheight*imgscale)/2
#         else:
#             #将宽度设置到最大
#             posy = (self.canvasheight-self.canvaswidth/imgscale)/2
#             posx = 0
#             pilImage = pilImage.resize((int(self.canvaswidth),int(self.canvaswidth/imgscale)))
#         return posx,posy
#     #获取每个视频的第一张图片
#     def video(self,threadName, delay):
#         def video_loop():
#             try:
#                 while True:
#                     picture1=self.tkImage(self.vc1)
#                     self.showvideocanvas.create_image(self.pos[0],self.pos[1],anchor='nw',image=picture1)  
#                     self.showvideocanvas.update_idletasks()  #最重要的更新是靠这两句来实现
#                     self.showvideocanvas.update()
#             except:
#                 self.close()  
#         video_loop()
#         # self.vc1.release()
#     def audio(self,threadName, delay):
#         py.mixer.init()
#         # 文件加载
#         track=py.mixer.music.load('video5.mp3')
#         # 播放，第一个是播放值 -1代表循环播放， 第二个参数代表开始播放的时间
#         py.mixer.music.play(-1, 0)
#         while True:  #一定要有whlie让程序暂停在这，否则会自动停止
#             pass
#     def great(self):
#         print("great")