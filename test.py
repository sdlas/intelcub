#usr/bin/python3

#导入pyserial模块
import serial
import pyqtgraph as pg
import array
import time

#串口配置，選擇USB0，波特率115200，無校驗位，停止位1，數據位8，超時10s
ser=serial.Serial('COM6',115200,parity='N',stopbits=1,bytesize=8,timeout=10)

while(1):
    #獲取字符串長度
    serlen = ser.inWaiting()
    #打印字符串
    print(ser.read(serlen))
    #程序延時1s
    time.sleep(1)
