# !/usr/bin/python
# -*- coding: UTF-8 -*-

#库调用
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from mutagen.mp3 import MP3
from PIL import Image,ImageTk
import pygame as py
import os.path
import glob


#窗口定义
window = tk.Tk()
window.title("基于Python tkinter Mp3 Player 1.0")
window.geometry("820x550")
window.attributes("-alpha",0.91)
#window.iconbitmap("error")

#批量导入本地歌曲
realpath = os.path.realpath(__file__) #当前绝对路径
dirname = os.path.dirname(realpath)
extension = 'mp3'
file_list = glob.glob('*.'+extension) #返回一个列表
#播放列表
aulist = []
aulist.extend(file_list) #拼接至播放列表
print(aulist)
#歌曲时长列表
aulen = []
for tik in range(len(aulist)):    
    audio = MP3(aulist[tik])
    aulen.append(audio.info.length)
print(aulen)


#插画
im1=Image.open("srcimage/book.jpg")
im1 = im1.resize((400,400))
img1=ImageTk.PhotoImage(im1)
imLabel1=tk.Label(window,image=img1,height=400, width=500).pack()
im2=Image.open("srcimage/book.jpg")
im2 = im2.resize((200,50))
img2=ImageTk.PhotoImage(im2)
imLabel2=tk.Label(window,image=img2,width=200, height=40 ).place(x=615,y=1)


#播放列表可视化
scr1 = scrolledtext.ScrolledText(window, bg="white", width=18, height=10,font=("Times New Roman",13))
#滚动文本框（宽，高（这里的高应该是以行数为单位），字体样式）
scr1.place(x=0, y=0) #滚动文本框在页面的位置
for num in range(len(aulist)):
    scr1.insert(tk.INSERT, '\n%d. %s\n' % (num+1, aulist[num]))
scr2 = scrolledtext.ScrolledText(window, bg="white", width=18, height=15,font=("Times New Roman",13))
scr2.insert(tk.INSERT, '播放记录:\n'  )
scr2.place(x=0, y=220)
#下拉选项
cmb = ttk.Combobox(window, width=22)
cmb['value'] = aulist
cmb.current(0)
cmb.place(x=629,y=50)

def re_set():
    delete_it()
    realpath = os.path.realpath(__file__)  # 当前绝对路径
    dirname = os.path.dirname(realpath)
    extension = 'mp3'
    file_list = glob.glob('*.' + extension)  # 返回一个列表
    # 播放列表
    global aulist
    aulist = []
    aulist.extend(file_list)  # 拼接至播放列表
    for k in range(len(aulist)):
        scr1.insert(tk.INSERT, '\n%s:\n'%aulist[k])
    print("重新导入成功！",aulist)


#全局变量
count = 0
flag = False
#播放主功能函数
def replay():
    # 初始化
    py.mixer.init()
    # 文件加载
    global count
    global flag
    if len(aulist) == 0:
        flag = True
    if flag == False:
        flag = True
        # 播放  第一个是播放值 -1代表当前单曲循环播放，第二个参数代表开始播放的时间
        py.mixer.music.load(aulist[count])
        py.mixer.music.play(-1, 0.3)
        scr2.insert(tk.INSERT, '%s\n\n' % aulist[count])
        print("正在播放：", aulist[count])
    else:
        flag = False
        py.mixer.music.pause()

#实现轮回切歌
def last_one():
    global count
    global flag
    if count != 0:
        count -= 1
        flag = False
        replay()
    else:
        flag = False
        count = len(aulist)-1
        replay()


def next_one():
    global count
    global flag
    if count != len(aulist)-1:
        count += 1
        flag = False
        replay()
    else:
        flag = False
        count = 0
        replay()


hit_it = False
def pause():
    global hit_it
    if hit_it == False:
        hit_it = True
        py.mixer.music.pause()
    else:
        hit_it = False
        py.mixer.music.unpause()


#进度条控制1
scale1 = tk.Scale(window, from_=0, to=int(max(aulen)), orient='horizonta', tickinterval=50, length=400)
scale1.place(x=208, y=405)
def jump_to1():
    global count
    py.mixer.init()
    py.mixer.music.load(aulist[count])
    py.mixer.music.play(-1, scale1.get())
    print("跳至第：%d 秒"%scale1.get()) #超过当前歌曲长度自动从头播放


#列表选择切歌
def sel_t():
    global count
    py.mixer.init()
    for num in range(len(aulist)):
        if cmb.get() == aulist[num]:
            count = num
    py.mixer.music.load(aulist[count])
    py.mixer.music.play(-1, 0.3)
    scr2.insert(tk.INSERT, '%s\n\n' % aulist[count])
    print("当前播放:%s"%cmb.get())


#自定义播放列表
scr3 = scrolledtext.ScrolledText(window, bg="white", width=18, height=18,font=("Times New Roman",13))
scr3.place(x=625, y=130)


#添加至自定义列表
def add_to():
    global aulist
    scr3.insert(tk.INSERT, "%s\n\n"%cmb.get())
    aulist.append(cmb.get())
    scr1.insert(tk.INSERT, "\n%s\n"%cmb.get())
    print("添加成功！", aulist)


#标签
text1 = tk.Text(window, bg = 'white', width=23,height=1)
text1.insert(tk.INSERT, "       我的歌单") #INSERT索引表示插入光标当前的位置
text1.place(x=0, y=0)
text2 = tk.Text(window, bg = '#CCCCFF', width=14,height=1)
text2.insert(tk.INSERT, "自定义播放列表") #INSERT索引表示插入光标当前的位置
text2.place(x=660, y=110)


def delete_it():
    global aulist
    global count
    count = 0
    aulist = []
    scr1.delete('1.0','end')
    scr3.delete('1.0', 'end')
    print("曲库已清空！")


#控件布局
photo1 = tk.PhotoImage(file='srcimage/book.jpg')
btn1 = tk.Button(window, text="播放", font = ("经典雅黑", 12), image=photo1, height=50, width=50, bg="#66CCFF", command = replay)
btn1.place(x=380,y=470)
photo2 = tk.PhotoImage(file='srcimage/book.jpg')
btn2 = tk.Button(window, text="上一首",image = photo2,height=30, width=30, bg="#33CCFF", anchor='center', command = last_one)
btn2.place(x=320,y=480)
photo3 = tk.PhotoImage(file='srcimage/book.jpg')
btn3 = tk.Button(window, text="下一首",image = photo3,height=30, width=30, bg="#00CCFF", command = next_one)
btn3.place(x=455,y=480)
btn4 = tk.Button(window, text="暂停", font = ("经典雅黑", 10), height=1, width=3, bg="#00CCFF", command = pause)
btn4.place(x=510,y=485)
btn5 = tk.Button(window, text="跳至", font = ("经典雅黑", 10), height=1, width=3, bg="#00CCFF", command =jump_to1)
btn5.place(x=270,y=485)
btn6 = tk.Button(window, text="选择", font = ("经典雅黑", 10), height=1, width=3, bg="white", command =sel_t)
btn6.place(x=695,y=80)
btn7 = tk.Button(window, text="添加", font = ("经典雅黑", 10), height=1, width=3, bg="#CCCCFF", command =add_to)
btn7.place(x=640,y=485)
btn8 = tk.Button(window, text="重置曲库", font = ("经典雅黑", 10), height=1, width=7, bg="#CCCCFF", command =delete_it)
btn8.place(x=700,y=485)
btn9 = tk.Button(window, text="刷新曲库", font = ("经典雅黑", 10), height=1, width=7, bg="#CCCCFF", command =re_set)
btn9.place(x=50,y=515)

window.mainloop()

