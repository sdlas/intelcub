# 语音识别   文字转换为音频
from aip import AipSpeech
import pygame as py
import time
import os
import _thread
class wordtovoice():
    def __init__(self,mainclass,string):
        self.app_id = "22734117"
        self.api_key = "dGN7IjSC9ZbeaEb9wpumWF8I"
        self.secret_key = "7wDCfXsZ8blwwa2peLOwVOHIoZuOyHUm"
        client = AipSpeech(self.app_id, self.api_key, self.secret_key)
        # 第一个参数：文本信息，第二个参数：语言
        result = client.synthesis(
            string,
            "zh",
            1,
            {
                "vlo": 6,  # 音量
                "spd": 2,  # 语速
                "pit": 9,  # 语调
                "per": 0  # 0:女 1：男 4：萝莉
            })
        # print(result)
        # 第一个参数：文件名，第二个参数是操作
        with open("tempvoice.mp3", "wb") as f:
            # f.write(json.dumps(result).encode())
            f.write(result)
        #play
        _thread.start_new_thread(self.playaudio,("theadname",0))
    def playaudio(self,threadname,x):
        os.system("mpg123 tempvoice.mp3")