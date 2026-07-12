#!/usr/bin/env python3
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import hardware
import time
import Function
import moving
import vision_
import cv2 
# import kociemba
import KociembaTrans
time.sleep(1)
hardware.Robot_Init()
# input("按键抓住")
# hardware.catch_both()
# vision_.turn_false()
# time.sleep(1)
# input("按键开始识别魔方")
Function.SolvingCube()
input('结束')

