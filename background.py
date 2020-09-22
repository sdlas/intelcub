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

class background():
    def __init__(self,master,_winheight,_winwidth,str):
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.master =master
        self.backimg = ImageTk.PhotoImage(Image.open("srcimage/background.jpg").resize((int(self.winwidth),int(self.winheight)))) 
        self.backgroundcanvas = tk.Canvas(self.master,width = self.winwidth,height = self.winheight)
        self.backgroundcanvas.place(x=0,y=0)
    def showimage(self):
        def video_loop():
            try:
                while True:
                    self.backgroundcanvas.create_image(0,0,anchor='nw',image=self.backimg)  
                    #canvas4.create_image(0,0,anchor='nw',image=picture1) 
                    self.backgroundcanvas.update_idletasks()  #最重要的更新是靠这两句来实现
                    self.backgroundcanvas.update()
            except:
                self.master.destroy()
            
        video_loop()