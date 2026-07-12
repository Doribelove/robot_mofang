#!/usr/bin/env python3
# import sys
# from tokenize import tabsize
# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import hardware
import moving
import vision_
import KociembaTrans
import kociemba
import time
import cv2
import twophase.solver  as sv
import jixiecost

arm_acting_time_90 = 0.2
arm_acting_time_180 = 0.23
hand_acting_time = 0.12
scan_time = 0.1



def SolvingCube():

    # vision_.turn_false()    
    # input()
    # CubeState = 'DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD'
    # CubeState = 'UUUUUUUUUBBBRRRFFFRRRFFFLLLDDDDDDDDDFFFLLLBBBLLLBBBRRR'
    # CubeState = ('U B B2 D\'')
    # input("按键开始解算魔方")
    # CubeState = 'BDBDUUFUFLLULRDBBLRFUBFFBURLBDRDRFLDUFDRLDRUDRRLLBFFBU'
    while (vision_.ok_flag != True):
        time.sleep(0.001)
    # time_begin = time.time()
    
    # print('识别时间 = ' + str(time.time()-time_begin))
    print('vision_.cubestate')
    print(vision_.cubestate)
    hardware.open_hand()
    time.sleep(0.005)
    hardware.catch_both()
    # time.sleep(0.01)
    # Solution = kociemba.solve(vision_.cubestate)
    time_begin = time.time()
    Solution = sv.solve(vision_.cubestate,0,0.08)
    # steps,cost,flag = KociembaTrans.TransToRealSolution(Solution)
    # Solution = sv.solve(CubeState,0,0.4)
    print('解算时间 = ' + str(time.time()-time_begin))
    Solution = jixiecost._KociembaTrans(Solution)
    print(Solution)
    print(len(Solution))
    Solution = jixiecost.jisuan(0, Solution)
    # Solution = ['U2', 'R2', 'D1', 'R2', 'U3', 'L3', 'B2', 'R3', 'D1', 'F2', 'U2', 'L2', 'B2', 'L2', 'B1', 'L2',
    # 'F1', 'U2']
    realsolution, costbushu = jixiecost._SolutionTransAndOptimize(Solution)
    print(realsolution)
    s = jixiecost.jixie1(realsolution)
    y = jixiecost.youhua1(s)
    z = jixiecost.jixie2(y)
    print(z)
    print(len(z))

    moving.steps_Move(z)
    print(len(z))

if __name__ == '__main__':
    # hardware.Robot_Init()
    # # input("按键抓住")
    # # hardware.catch_both()
    # # input("按键开始")
    # CubeState = 'RUFFULUDLDUUBRRFRBLBBLFRUULBFDLDFFURDDBLLDRFRLBFDBBDRU'
    # Solution = kociemba.solve(CubeState)
    # #hardware.faster_Arms()
    # print(Solution)
    # Solution=KociembaTrans._KociembaTrans(Solution)
    # steps,cost,flag = KociembaTrans.TransToRealSolution(Solution)
    # print(steps)
    # print('cost'+ str(cost))
    # print('flag:'+flag)
    t=0.3
    time.sleep(t)
    hardware.odrive_calibrate()
    time.sleep(t)
    input()
    hardware.open_hand()
    time.sleep(0.1)
    hardware.catch_both()
    time.sleep(t)
    input()
    www=['R3','F3','B2','R3','L3','U1','R3','D1','F2','L3','B1','R1','D2','R2','D3','F2','B2','U3']
    solu,flag,time1=KociembaTrans._SolutionTransAndOptimizeDfs(www)
    # steps=[('RW', 'Medium', -90), ('RH', 'open'), ('RW', 'fast', 90), ('RH', 'close'), ('LH', 'open'), ('RW', 'slow', 90), ('LH', 'close'), ('RH', 'open'), ('RW', 'fast', -90), ('RH', 'close'), ('LW', 'Medium', -90), ('LH', 'open'), ('LW', 'fast', 90), ('LH', 'close'), ('RW', 'Medium', 180), ('LW', 'Medium', 180), ('LH', 'open'), ('RW', 'slow', 180), ('LH', 'close'), ('LW', 'Medium', 90), ('LH', 'open'), ('LW', 'fast', -90), ('LH', 'close'), ('LW', 'Medium', 180), ('RH', 'open'), ('LW', 'slow', 180), ('RH', 'close'), ('RW', 'Medium', 90), ('RH', 'open'), ('RW', 'fast', -90), ('RH', 'close'), ('LW', 'Medium', -90), ('LH', 'open'), ('LW', 'fast', 90), ('RW', 'slow', 180), ('LH', 'close'), ('LW', 'Medium', 180), ('LW', 'Medium', -90), ('LH', 'open'), ('LW', 'fast', 90), ('LH', 'close'), ('RH', 'open'), ('LW', 'slow', 180), ('RH', 'close'), ('RW', 'Medium', 90), ('RH', 'open'), ('RW', 'fast', -90), ('RH', 'close'), ('LW', 'Medium', 90), ('LH', 'open'), ('LW', 'fast', -90), ('LH', 'close'), ('RH', 'open'), ('LW', 'slow', 180), ('RH', 'close'), ('RW', 'Medium', 180), ('LH', 'open'), ('RW', 'slow', 90), ('LH', 'close'), ('RH', 'open'), ('RW', 'fast', -90), ('RH', 'close'), ('LW', 'Medium', -90), ('LH', 'open'), ('LW', 'fast', 90), ('RW', 'slow', 90), ('LH', 'close'), ('RH', 'open'), ('RW', 'fast', -90), ('RH', 'close'), ('LW', 'Medium', 180), ('LW', 'Medium', 180), ('RW', 'Medium', 180), ('LW', 'Medium', 180), ('LW', 'Medium', 90), ('LH', 'open'), ('LW', 'fast', -90), ('LH', 'close'), ('LW', 'Medium', 180)]
    print(solu)
    moving.steps_Move(solu)
    time.sleep(0.02)
    hardware.loosen_both()
    time.sleep(0.02)
    hardware.loose_hand()
    time.sleep(0.1)
    hardware.odrive_out_of_closeloop()
    hardware.catch_both()