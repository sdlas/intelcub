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

class title():
    def __init__(self,master,_winheight,_winwidth,str):
        self.winheight = _winheight
        self.winwidth = _winwidth
        self.master =master
        self.topheight = 130 #顶部标题高度
        self.titleheight = self.topheight/2
        self.titlewidth = self.titleheight*7
        self.titlepadding = self.topheight/4 #顶部按钮的间距
        self.title = tk.Canvas(self.master,bg="white",height = self.titleheight,width = self.titlewidth)
        self.title.place(x=(self.winwidth-self.titlewidth)/2,y=20)
        self.title.create_text(self.titlewidth/2,self.titleheight/2,text=str,font=("宋体",35))
    def passit(self):
        pass