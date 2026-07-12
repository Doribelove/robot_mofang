#!/usr/bin/env python3
# import sys
# from tokenize import tabsize
# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import hardware
import moving
import vision_
import KociembaTrans
# import kociemba
import time
import cv2
import twophase.solver  as sv

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
    # Solution = kociemba.solve(vision_.cubestate)
    time_begin = time.time()
    time_begin0 = time.time()
    Solution = sv.solve(vision_.cubestate,0,0.4)
    # Solution = sv.solve(CubeState,0,0.4)
    print('解算时间 = ' + str(time.time()-time_begin))
    kk = Solution.rfind(' ', 0,len(Solution) )
    Solution = Solution[0:kk]
    # Solution = kociemba.solve(CubeState)
    print(Solution)
    # input("按键开始动作复原")
    time_begin = time.time()
    steps,cost,flag = KociembaTrans.TransToRealSolution(Solution)
    print('搜索时间 = ' + str(time.time()-time_begin))
    print('解算＋搜索时间 = ' + str(time.time()-time_begin0))
    # print(steps)
    print('cost'+ str(cost))
    print('flag:'+flag)
    print('步骤数：'+str(len(steps)))
    # input('按键开始动作')
    moving.steps_Move(steps)
    time.sleep(0.05)
    hardware.loosen_both()
if __name__ == '__main__':
    # hardware.Robot_Init()
    # input("按键抓住")
    # hardware.catch_both()
    # input("按键开始")
    # CubeState = 'RUFFULUDLDUUBRRFRBLBBLFRUULBFDLDFFURDDBLLDRFRLBFDBBDRU'
    # Solution = kociemba.solve(CubeState)
    # #hardware.faster_Arms()
    # print(Solution)
    # steps,cost,flag = KociembaTrans.TransToRealSolution(Solution)
    # print(steps)
    # print('cost'+ str(cost))
    # print('flag:'+flag)
    # moving.steps_Move(steps)
    # time.sleep(1)
    # hardware.loosen_both()
    pass