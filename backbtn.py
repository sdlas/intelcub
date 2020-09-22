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

class backbtn():
    def __init__(self,master,_winheight,_winwidth):
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.master =master
        self.topheight = 130 #顶部标题高度
        self.backbtnheight = self.topheight/2
        self.backbtnwidth = self.backbtnheight
        self.backbtnpadding = self.topheight/4 #顶部按钮的间距
        self.backimg = ImageTk.PhotoImage(Image.open("srcimage/toleft.jpg").resize((int(self.backbtnwidth),int(self.backbtnheight)))) 
        self.backbtn = tk.Button(self.master,image = self.backimg,height=self.backbtnheight,width=self.backbtnwidth,command=self.back)
        self.backbtn.place(x=self.backbtnpadding,y=self.backbtnpadding) 
    def back(self):
        self.master.destroy()