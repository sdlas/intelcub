import tkinter as tk
import tkinter.colorchooser
import pygame as py
import time
import _thread
from tkinter import *
import cv2
from PIL import Image, ImageTk
import multiprocessing
import glob
from backbtn import backbtn #返回按钮
from title import title
from background import background
winheight = 0
winwidth = 0
class photopage():
    def __init__(self,master,_winheight,_winwidth):
        #获取本地图片文件
        self.extensionlist = ['jpg']
        self.imagelist = []
        for extension in self.extensionlist: 
            file_list = glob.glob('photos/*.'+extension) #返回一个列表
            for item  in file_list:
                self.imagelist.append(item[7:])
        
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.photowidth = self.winwidth/8
        self.photopadding = self.winwidth/64
        self.master = master
        self.imagereadlist=[]
        self.topheight = 130 #顶部标题高度
        #读取图片
        for n in range(0,len(self.imagelist)):
            self.imagereadlist.append(ImageTk.PhotoImage(self.goodimage(n)))
        self.photopage = tk.Canvas(self.master,bg="pink",width=self.winwidth,height=self.winheight)
        self.photopage.place(x=0,y=0)
        self.photopage.configure(highlightthickness=0)
         #背景
        bg = background(self.photopage,self.winheight,self.winwidth,"call")
        #返回按钮
        backbtn(self.photopage,self.winheight,self.winwidth)
        #标题
        title(self.photopage,self.winheight,self.winwidth,"看照片")
        #图片缩略图放置
        for n in range(0,len(self.imagelist)):
            locals()['self.tempbutton'+str(n)] = tk.Button(self.photopage,image=self.imagereadlist[n], width=self.photowidth,height=self.photowidth,command=self.returnfun(n),bd=0)
            locals()['self.tempbutton'+str(n)].place(x=n%7*(self.photowidth+self.photopadding)+self.photopadding,y=int((n+1)/8)*(self.photowidth+self.photopadding)+self.topheight)
        bg.showimage()
    def back(self):
        self.photopage.destroy()
        #self.vbar.destory()
    def showbigimage(self,x):
        bigimage(self.photopage,x,self.winheight,self.winwidth,self.imagelist)
    def returnfun(self,x):
        return lambda:self.showbigimage(x)
    def goodimage(self,id):
        tempimage = Image.open("photos/"+self.imagelist[id])
        imgwidth = tempimage.size[0]
        imgheight = tempimage.size[1]
        imgscale = imgwidth/imgheight
        if imgscale>1:
            #将高度设置到最大
            tempimage = tempimage.resize((int(self.photowidth*imgscale),int(self.photowidth)))
        else:
            #将宽度设置到最大
            tempimage = tempimage.resize((int(self.photowidth),int(self.photowidth/imgscale)))
        return tempimage
class bigimage():
    def __init__(self,master,id,_winheight,_winwidth,imagelist):
        self.imagelist =imagelist
        self.winwidth = _winwidth
        self.winheight = _winheight
        self.curid = id
        self.master = master
        self.bigimage = tk.Canvas(self.master,bg="pink",width=self.winwidth,height=self.winheight)
        self.bigimage.configure(highlightthickness=0)
        self.bigimage.place(x=0,y=0)
        self.paddingl = 200 #水平的间隙
        self.paddingv = 60 #竖直方向的间隙 
        self.canvaswidth = self.winwidth-self.paddingl*2
        self.canvasheight = self.winheight-self.paddingv*2
        self.canvasscale = self.canvaswidth/self.canvasheight
        self.pointbtnwidth = 100 #切换图片按钮的大小
        self.pointbtnpadding = 50 #按钮的间距
        self.closebtnwidth = 50 #关闭按钮的大小
        self.closebtnpadding =30 #关闭按钮的间距
        self.rightimg = ImageTk.PhotoImage(Image.open("srcimage/toright.jpg").resize((int(self.pointbtnwidth),int(self.pointbtnwidth))))  
        self.leftimg = ImageTk.PhotoImage(Image.open("srcimage/toleft.jpg").resize((int(self.pointbtnwidth),int(self.pointbtnwidth))))  
        self.closeimg = ImageTk.PhotoImage(Image.open("srcimage/close.jpg").resize((int(self.closebtnwidth),int(self.closebtnwidth)))) 

        
        self.showimg =  ImageTk.PhotoImage(self.goodimage(id))
        self.pos = self.rightpos(id) 
        #显示图片的地方
        self.showimagecanvas = tk.Canvas(self.bigimage,bg="pink" ,width=self.canvaswidth,height = self.canvasheight)
        self.showimagecanvas.place(x=self.paddingl,y=self.paddingv)
        self.showimagecanvas.configure(highlightthickness=0)
        #显示按钮
        self.rightbtn = tk.Button(self.bigimage,image=self.rightimg,width=self.pointbtnwidth,height=self.pointbtnwidth,command=self.changeright)
        self.leftbtn = tk.Button(self.bigimage,image=self.leftimg,width=self.pointbtnwidth,height=self.pointbtnwidth,command=self.changeleft)
        self.leftbtn.place(x=self.pointbtnpadding,y=self.winheight/2-self.pointbtnwidth/2)
        self.rightbtn.place(x=self.winwidth-self.pointbtnpadding-self.pointbtnwidth,y=self.winheight/2-self.pointbtnwidth/2)
        #关闭按钮
        self.closebtn = tk.Button(self.bigimage,image=self.closeimg,width=self.closebtnwidth,height=self.closebtnwidth,command=self.close)
        self.closebtn.place(x=self.winwidth-self.closebtnwidth-self.closebtnpadding,y=self.closebtnpadding)
        
        self.showimage()
    def changeright(self):
        self.curid = (self.curid+1)%len(self.imagelist)
        self.showimg =  ImageTk.PhotoImage(self.goodimage(self.curid)) 
        self.pos = self.rightpos(self.curid)
    def changeleft(self):
        self.curid = (self.curid-1)%len(self.imagelist)
        self.showimg =  ImageTk.PhotoImage(self.goodimage(self.curid)) 
        self.pos = self.rightpos(self.curid)
    def close(self):
        self.bigimage.destroy()
    def showimage(self):
        def video_loop():
            try:
                while True:
                    self.showimagecanvas.create_image(self.pos[0],self.pos[1],anchor='nw',image=self.showimg)  
                    #canvas4.create_image(0,0,anchor='nw',image=picture1) 
                    self.master.update_idletasks()  #最重要的更新是靠这两句来实现
                    self.master.update()
            except:
                self.close()
            
        video_loop()
        #self.face1.mainloop()
        self.vc1.release()
        cv2.destroyAllWindows()
    #返回合适比例的图片
    def goodimage(self,id):
        tempimage = Image.open("photos/"+self.imagelist[id])
        imgwidth = tempimage.size[0]
        imgheight = tempimage.size[1]
        imgscale = imgwidth/imgheight
        if imgscale<self.canvasscale:
            #将高度设置到最大
            tempimage = tempimage.resize((int(self.canvasheight*imgscale),int(self.canvasheight)))
        else:
            #将宽度设置到最大
            tempimage = tempimage.resize((int(self.canvaswidth),int(self.canvaswidth/imgscale)))
        return tempimage
    #返回图片适合的放置位置
    def rightpos(self,id):
        tempimage = Image.open("photos/"+self.imagelist[id])
        imgwidth = tempimage.size[0]
        imgheight = tempimage.size[1]
        imgscale = imgwidth/imgheight
        posx = 0 
        posy = 0
        if imgscale<self.canvasscale:
            #将高度设置到最大
            tempimage = tempimage.resize((int(self.canvasheight*imgscale),int(self.canvasheight)))
            posy = 0
            posx = (self.canvaswidth-self.canvasheight*imgscale)/2
        else:
            #将宽度设置到最大
            posy = (self.canvasheight-self.canvaswidth/imgscale)/2
            posx = 0
            tempimage = tempimage.resize((int(self.canvaswidth),int(self.canvaswidth/imgscale)))
        return posx,posy
if __name__ == '__main__':    
    root = tk.Tk()
    root.attributes("-fullscreen",True)
    winwidth = root.winfo_screenwidth()
    winheight = root.winfo_screenheight()
    photopage(root,winheight,winwidth)
    root.mainloop()