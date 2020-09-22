#usr/bin/python3

#
import serial

def call(num)
    #
    ser = serial.Serial("com1", 115200, parity='N', stopbits=1, bytesize = 0, timeout=3)
    
    #
    ser.write('ATD'+num+';\r\n'.encode())

    #du
