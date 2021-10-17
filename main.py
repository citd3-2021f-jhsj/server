import socket
<<<<<<< HEAD
import pickle
import time
from _thread import *
import queue
import random, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns

AllowedErrorrange=2#constant or Variable
def MappingFunc(RssiVal, id):
    #mapping from Rssi signal to distance
    # 0.3m: -44, 6.7m: -63  8.8m: -75
    height= 1.5#(높이 보정)
    if id==0:
        measuredpower= -50
        knownsignal= 1.56
        cap = 10
    elif id==1:
        measuredpower = -50
        knownsignal =2.83
        cap = 10
    elif id==2:
        measuredpower = -50
        knownsignal = 0.77
        cap=10
    prediction=10**((measuredpower-RssiVal)/(10*knownsignal))
    return min(cap, math.sqrt(max((prediction)**2-height**2, 0)))
def GaussianVal(mean, Variance, x):
    return math.exp(-1*(x-mean)**2/2/Variance)/math.sqrt(2*math.pi*Variance)
def GetDists(Receivers, Datas):
    Dists=[]
    for i, Pos in enumerate(Receivers):
        print("from Receiver "+str(i)+"at position"+str(Pos))
        RssiV=Datas[i]
        tempData= MappingFunc(RssiV, i)
        Dists.append(tempData)
    print(Dists)
    return Dists

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def distance(fromA, toB):
    return (math.sqrt((fromA[0]-toB[0])**2+(fromA[1]-toB[1])**2))
def ProbEval(X, Y):
    #가우시안 분포로 하고 싶은데 귀찮아서 그냥 다른걸로 함
    #return (max(1-abs(X-Y)/AllowedErrorrange, 0))
    return (GaussianVal(X, Y*AllowedErrorrange+0.1, Y))
=======
>>>>>>> parent of cbd3a0f (server tmp code)


HOST = '0.0.0.0'
PORT = 50007

# 소켓 생성
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    print('binding')
    s.bind((HOST, PORT))
    print('listening')
    s.listen(1)

    conn, addr = s.accept()

    with conn:
        print('connected {}:{}'.format(addr[0], addr[1]))
        while True:
<<<<<<< HEAD
            # listen
            try:
                conn.listen(1)
                cli, addr = conn.accept()
                print(f"[INFO] Client connection established - {addr[0]}:{addr[1]}")
                num_curr_clients += 1
                start_new_thread( thread_main, (cli, addr[0], addr[1]) )
            except Exception as e:
                pass

        # shutdown before continue
        conn.close()
        time.sleep(1)
def Animate(i):
    plt.plot()
if __name__ == "__main__":
    Roomsize = (6.7, 8.8)  # 가로 6.7m, 세로 8.8m
    ReceiversPosition = [(0, 8.8), (0, 0), (6.7, 0)]  # All Positions should be consist of positive Real numbers
    # (0,0)------------------------(1,0)
    # |
    # |
    # |
    # |
    # |
    # |
    # |
    # (1,1)
    # seperate queue to receive data
    start_new_thread( receive_main_thread, () )

    # get stream and process
    while True:
        buffer = []
        base_time = time.time()
        while time.time() - base_time < 2 :
            buffer.append( global_queue.get() )

        # TODO tmp coding ; average values collected for 3s of beacon 1
        valuemap = [ [], [], [] ]
        for k, d in buffer:
            if k == 'A': #(4.6, 3.3)
                if '1C' in d.keys():
                    valuemap[0].append(d['1C'])
            if k == 'B':  #(4.2, 3.0)
                if '1C' in d.keys():
                    valuemap[1].append(d['1C'])
            if k == 'C': #(4.5, 3.0)
                if '1C' in d.keys():
                    valuemap[2].append(d['1C'])
                    #시간 ㅈㄴ 길게 해서 평균내기?
                    #상수 바꾸는건 의미 있을지 모르겠다
        avgvalue = [ sum(i)/len(i) if len(i)>0 else -60 for i in valuemap ]
        print(avgvalue)

        # TODO here

        Data=avgvalue
        Distances = GetDists(ReceiversPosition, Data)
        # sampling that divides field in sampling x sampling size gird
        sampling = 50  # 1m당 몇번 scan할것인지
        highscore = 0
        highposition = None
        Rememberfield = [[] for i in range(int(sampling * Roomsize[0]))]
        for i in range(int(sampling * Roomsize[0])):
            for j in range(int(sampling * Roomsize[1])):
                ScanX = float(i / sampling)
                ScanY = float(j / sampling)
                Score = 1
                for k, RecP in enumerate(ReceiversPosition):
                    Score *= ProbEval(distance((ScanX, ScanY), RecP), Distances[k])
                    # scan 한 포지션에 있을 확률을 계산
                Rememberfield[i].append(Score)
                if Score >= highscore:
                    highscore = Score
                    highposition = (ScanX, ScanY)
        ax = sns.heatmap(Rememberfield)
        print(highposition)
        ani=FuncAnimation(plt.gcf(), Animate,interval=2000)
        # TODO tmp coding end
        #plt.show()
        #print(buffer)

=======
            data = conn.recv(1024)
            print('data: {}'.format(str(data)))
            if not data:
                break
            conn.send(b'hey')
>>>>>>> parent of cbd3a0f (server tmp code)
