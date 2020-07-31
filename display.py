import matplotlib.pyplot as plt
import sys, msvcrt
import time
import serial
import numpy as np
import re
import threading

exitFlag = 0
x_range = 1000
y = np.zeros(x_range, dtype = float)

def dataRecieve(threadName):
    ser = serial.Serial('com3',115200)
    i = 0
    data = ""
    while True:
        while ser.inWaiting() > 0:
            data += str(ser.read(1), 'utf-8')
        if data != '':
            list = re.findall(r'\-?\d+\.?\d*', data)
            #print (list)
            j = 0
            length = len(list)
            while  j < length:
                if i == x_range:
                    i = 0
                y[i]=float(list[j])
                i += 1
                j += 1
        data = ""
        if exitFlag:
            threadName.exit()

def plotDraw():
    print ("\n关闭此窗口以退出")
    plt.ion()
    plt.figure(figsize=(12, 6))
    while True:
        plt.plot(y, 'r.-') 
        plt.plot([0 for _ in y]) 
        plt.ylim(-3.2,3.2)
        plt.draw()
        plt.pause(0.25)
        plt.clf()
        if msvcrt.kbhit() and ord(msvcrt.getch()) == 27:
            exitFlag = 1
            exit()

class dataThread (threading.Thread, ):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print ("启用线程： " + self.name)
        # 获取锁，用于线程同步
        threadLock.acquire()
        dataRecieve(self.name)
        # 释放锁，开启下一个线程
        threadLock.release()
        
threadLock = threading.Lock()
threads = []

# 创建新线程
thread = dataThread(1, "dataThread")

# 开启新线程
thread.start()

# 添加线程到线程列表
threads.append(thread)

plotDraw()
# 等待所有线程完成
for t in threads:
    t.join()
