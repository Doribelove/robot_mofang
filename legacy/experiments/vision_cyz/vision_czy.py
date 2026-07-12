#!/usr/bin/env python3
# import sys
# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import time
import cv2
import threading
import numpy as np
import kociemba
import twophase.solver  as sv

print("vision module start working!")
if __name__ == '__main__':
    cap1 = cv2.VideoCapture('/dev/video2')
    '''cap1.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)# where 0.25 means "manual exposure, manual iris"  opencv4
    cap1.set(cv2.CAP_PROP_EXPOSURE, 15)
    cap1.set(cv2.CAP_PROP_CONTRAST, 30)
    cap1.set(cv2.CAP_PROP_AUTO_WB, 0) #禁用白平衡
    cap1.set(cv2.CAP_PROP_WB_TEMPERATURE, 4600)
    cap1.set(cv2.CAP_PROP_BUFFERSIZE, 1)'''
    cap1.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    # cap1.release()
    cap2 = cv2.VideoCapture('/dev/video4')
    '''cap2.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)# where 0.25 means "manual exposure, manual iris" opencv4
    cap2.set(cv2.CAP_PROP_EXPOSURE, 10000)
    cap2.set(cv2.CAP_PROP_BRIGHTNESS, 1)  
    cap2.set(cv2.CAP_PROP_CONTRAST, 30)
    cap2.set(cv2.CAP_PROP_AUTO_WB, 0) #禁用白平衡
    cap2.set(cv2.CAP_PROP_WB_TEMPERATURE, 4350)
    cap2.set(cv2.CAP_PROP_BUFFERSIZE, 1)'''
    cap2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    # cap2.release()
    cap3 = cv2.VideoCapture('/dev/video6')
    '''cap3.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)# where 0.25 means "manual exposure, manual iris" opencv4
    cap3.set(cv2.CAP_PROP_EXPOSURE, 8) 
    cap3.set(cv2.CAP_PROP_BRIGHTNESS, -20)    
    cap3.set(cv2.CAP_PROP_AUTO_WB, 0) #禁用白平衡
    cap3.set(cv2.CAP_PROP_WB_TEMPERATURE, 4600)
    cap3.set(cv2.CAP_PROP_BUFFERSIZE, 1)'''
    cap3.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    # cap3.release()
    cap4 = cv2.VideoCapture('/dev/video8')
    '''cap4.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)# where 0.25 means "manual exposure, manual iris" opencv4
    cap4.set(cv2.CAP_PROP_EXPOSURE, 10) 
    cap4.set(cv2.CAP_PROP_BRIGHTNESS, 0)
    cap4.set(cv2.CAP_PROP_CONTRAST, 20)
    cap4.set(cv2.CAP_PROP_AUTO_WB, 1) #禁用白平衡
    cap4.set(cv2.CAP_PROP_WB_TEMPERATURE, 4600)
    cap4.set(cv2.CAP_PROP_BUFFERSIZE, 1)'''
    cap4.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    # CV_CAP_PROP_CONTRAST
    # cap4.release()
    # cap3 = cv2.VideoCapture(3)
    # cap4 = cv2.VideoCapture(4)
    # cap2 = cv2.VideoCapture('/dev/video222')
    # cap4 = cv2.VideoCapture(4)


    while (True):
        ret1,img_cube1,  = cap1.read()
        cv2.imshow("cube1",img_cube1)
        cv2.imwrite('11.jpg', img_cube1)
        cv2.waitKey(1)
        ret1,img_cube2,  = cap2.read()
        cv2.imshow("cube2",img_cube2)
        cv2.imwrite('22.jpg', img_cube2)
        cv2.waitKey(1)
        ret1,img_cube3,  = cap3.read()
        cv2.imshow("cube3",img_cube3)
        cv2.imwrite('33.jpg', img_cube3)
        cv2.waitKey(1)
        ret1,img_cube4,  = cap4.read()
        cv2.imshow("cube4",img_cube4)
        cv2.imwrite('44.jpg', img_cube4)
        cv2.waitKey(1)