import pygame as py
import _thread
import time
import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import multiprocessing

window_width=960
window_height=720
image_width=320
image_height=int(window_height*1)
imagepos_x=0
imagepos_y=0
butpos_x=450
butpos_y=450
vc1 = cv2.VideoCapture('dance.mp4')  #读取视频

#图像转换，用于在画布中显示
def tkImage(vc):
    ref,frame = vc.read()
    cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pilImage = Image.fromarray(cvimage)
    pilImage = pilImage.resize((image_width, image_height),Image.ANTIALIAS)
    tkImage =  ImageTk.PhotoImage(image=pilImage)
    return tkImage
#图像的显示与更新
def video():
    def video_loop():
       try:
            while True:
                picture1=tkImage(vc1)
                canvas1.create_image(0,0,anchor='nw',image=picture1)  
                canvas2.create_image(0,0,anchor='nw',image=picture1)
                canvas3.create_image(0,0,anchor='nw',image=picture1)
                #canvas4.create_image(0,0,anchor='nw',image=picture1)
                win.update_idletasks()  #最重要的更新是靠这两句来实现
                win.update()
       except:
            pass
          
    video_loop()
    win.mainloop()
    vc1.release()
    cv2.destroyAllWindows()

'''布局'''
win = tk.Tk()
win.geometry(str(window_width)+'x'+str(window_height))
canvas1 =Canvas(win,bg='white',width=image_width,height=image_height)
canvas1.place(x=imagepos_x,y=imagepos_y)
canvas2 =Canvas(win,bg='white',width=image_width,height=image_height)
canvas2.place(x=320,y=0)
canvas3 =Canvas(win,bg='white',width=image_width,height=image_height)
canvas3.place(x=640,y=0)   
# canvas4 =Canvas(win,bg='white',width=image_width,height=image_height)
# canvas4.place(x=480,y=360) 

if __name__ == '__main__': 
    p1 = multiprocessing.Process(target=video)
    p1.start()
    