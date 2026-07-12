#!/usr/bin/env python3
# import sys
# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import os
import time
import cv2
import threading
import numpy as np
import kociemba
import twophase.solver  as sv
import hardware

CAMERA_DEVICES = [
    os.getenv("RUBIK_CAMERA_1", "/dev/video2"),
    os.getenv("RUBIK_CAMERA_2", "/dev/video4"),
    os.getenv("RUBIK_CAMERA_3", "/dev/video6"),
    os.getenv("RUBIK_CAMERA_4", "/dev/video8"),
]
# import vision_test
# img_cube1 = None
# img_cube2 = None
# img_cube3 = None
# img_cube4 = None
# img_cube5 = None
flag = True
flag_main = True
ok_flag = False

img_flag1 = 0
img_flag2 = 0
img_flag3 = 0
img_flag4 = 0
img_flag5 = 0
soving_flag = 0
sovingdown_flag = 0
cubestate = ""
def cube_recognize():
    global img_cube1,img_cube2,img_cube3,img_cube4,cubestate,ok_flag
    img1 = img_cube1
    img2 = img_cube2
    img3 = img_cube3
    img4 = img_cube4
    # img4 = img_cube5
    sta_cube = []

    block_u1 = exchange((231, 118))
    block_u2 = exchange((295, 122))
    block_u3 = exchange((365, 122))
    block_u4 = exchange((225, 157))
    block_u5 = exchange((298, 159))
    block_u6 = exchange((365, 154))
    block_u7 = exchange((214, 208))
    block_u8 = exchange((293, 204))
    block_u9 = exchange((375, 205))

    block_f1 = exchange((216, 270))
    block_f2 = exchange((298, 267))
    block_f3 = exchange((373, 265))
    block_f4 = exchange((227, 317))
    block_f5 = exchange((297, 317))
    block_f6 = exchange((376, 315))
    block_f7 = exchange((230, 354))
    block_f8 = exchange((300, 353))
    block_f9 = exchange((369, 350))

    block_b1 = exchange((274, 129))
    block_b2 = exchange((332, 128))
    block_b3 = exchange((392, 130))
    block_b4 = exchange((263, 163))
    block_b5 = exchange((334, 166))
    block_b6 = exchange((399, 160))
    block_b7 = exchange((257, 208))
    block_b8 = exchange((332, 207))
    block_b9 = exchange((410, 208))

    block_d1 = exchange((396, 344))
    block_d2 = exchange((334, 348))
    block_d3 = exchange((272, 346))
    block_d4 = exchange((404, 311))
    block_d5 = exchange((332, 309))
    block_d6 = exchange((268, 312))
    block_d7 = exchange((412, 263))
    block_d8 = exchange((334, 267))
    block_d9 = exchange((258, 261))

    block_l1 = exchange((282, 98))
    block_l2 = exchange((368, 187))
    block_l3 = exchange((454, 275))
    block_l4 = exchange((215, 198))
    block_l5 = exchange((282, 265))
    block_l6 = exchange((367, 356))
    block_l7 = exchange((108, 261))
    block_l8 = exchange((208, 332))
    block_l9 = exchange((276, 439))

    block_r1 = exchange((449, 262))
    block_r2 = exchange((371, 347))
    block_r3 = exchange((287, 424))
    block_r4 = exchange((362, 188))
    block_r5 = exchange((290, 266))
    block_r6 = exchange((227, 326))
    block_r7 = exchange((287, 107))
    block_r8 = exchange((224, 203))
    block_r9 = exchange((129, 264))


    # piex1_r = (5, 1, 83)
    # piex1_g = (34, 150, 1)
    # piex1_b = (126, 45, 0)
    # piex1_o = (67, 93, 237)
    # piex1_y = (255, 182, 250)
    # piex1_w = (200, 200, 200)
#这里是白边的
    piex1_r = (10, 10, 145)
    piex1_g = (55, 135, 5)
    piex1_b = (120, 85, 0)
    piex1_o = (40, 55, 225)
    piex1_y = (60, 160, 155)
    piex1_w = (140, 145, 140)


    piex2_r = (40, 40, 140)
    piex2_g = (55, 120, 25)
    piex2_b = (110, 85, 30)
    piex2_o = (60, 70, 230)
    piex2_y = (60, 145, 155)
    piex2_w = (140, 140, 140)


    piex3_r = (40, 40, 140)
    piex3_g = (50, 130, 30)
    piex3_b = (130, 90, 35)
    piex3_o = (70, 75, 215)
    piex3_y = (80, 170, 170)
    piex3_w = (155, 155, 155)


    piex4_r = (5, 5, 160)
    piex4_g = (30, 140, 5)
    piex4_b = (140, 75, 0)
    piex4_o = (35, 40, 255)
    piex4_y = (10, 170, 170)
    piex4_w = (152, 155, 155)

# #黑白混合#################################
#     #黑白混合
#     piex1_r = (10, 10, 132)
#     piex1_g = (50, 125, 5)
#     piex1_b = (122, 77, 0)
#     piex1_o = (30, 52, 215)
#     piex1_y = (50, 150, 145)
#     piex1_w = (135, 140, 135)


#     piex2_r = (40, 40, 125)
#     piex2_g = (55, 112, 30)
#     piex2_b = (110, 76, 30)
#     piex2_o = (50, 65, 215)
#     piex2_y = (55, 145, 147)
#     piex2_w = (137, 137, 137)


#     piex3_r = (40, 40, 135)
#     piex3_g = (50, 130, 30)
#     piex3_b = (127, 87, 30)
#     piex3_o = (70, 76, 215)
#     piex3_y = (82, 172, 170)
#     piex3_w = (157, 157, 157)


#     piex4_r = (5, 5, 165)
#     piex4_g = (35, 150, 5)
#     piex4_b = (160, 89, 0)
#     piex4_o = (35, 40, 255)
#     piex4_y = (10, 190, 190)
#     piex4_w = (155, 166, 166)

    ####################################
    # #这里是黑边的
    # piex1_r = (10, 10, 120)
    # piex1_g = (45, 115, 5)
    # piex1_b = (125, 70, 0)
    # piex1_o = (20, 50, 205)
    # piex1_y = (40, 140, 135)
    # piex1_w = (130, 135, 130)


    # piex2_r = (40, 40, 115)
    # piex2_g = (55, 105, 35)
    # piex2_b = (110, 70, 30)
    # piex2_o = (40, 60, 200)
    # piex2_y = (50, 145, 140)
    # piex2_w = (135, 135, 135)


    # piex3_r = (40, 40, 130)
    # piex3_g = (50, 130, 30)
    # piex3_b = (125, 85, 25)
    # piex3_o = (70, 80, 215)
    # piex3_y = (85, 175, 170)
    # piex3_w = (160, 160, 160)


    # piex4_r = (5, 5, 170)
    # piex4_g = (40, 170, 5)
    # piex4_b = (190, 110, 0)
    # piex4_o = (35, 40, 255)
    # piex4_y = (60, 220, 220)
    # piex4_w = (182, 180, 180)

    ################################


    sta_cube1 = []
    sta_cube1.append(piex1_r)
    sta_cube1.append(piex1_g)
    sta_cube1.append(piex1_b)
    sta_cube1.append(piex1_o)
    sta_cube1.append(piex1_y)
    sta_cube1.append(piex1_w)

    sta_cube1.append(img1[block_u1])        
    sta_cube1.append(img1[block_u2])
    sta_cube1.append(img1[block_u3])
    sta_cube1.append(img1[block_u4])
    sta_cube1.append(img1[block_u5])
    sta_cube1.append(img1[block_u6])
    sta_cube1.append(img1[block_u7])
    sta_cube1.append(img1[block_u8])
    sta_cube1.append(img1[block_u9])
    sta_cube1.append(img1[block_f1])        
    sta_cube1.append(img1[block_f2])
    sta_cube1.append(img1[block_f3])
    sta_cube1.append(img1[block_f4])
    sta_cube1.append(img1[block_f5])
    sta_cube1.append(img1[block_f6])
    sta_cube1.append(img1[block_f7])
    sta_cube1.append(img1[block_f8])
    sta_cube1.append(img1[block_f9])
    sta_cube1 = np.float32(sta_cube1)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10,1.0)
    flags = cv2.KMEANS_PP_CENTERS
    ret, best_labels1, centers = cv2.kmeans(sta_cube1, 6, None, criteria, 10, flags)
    # print(best_labels1)

    state1 = [None]*18
    for i in range(6,len(best_labels1)):
        for j in range(6):
            if (best_labels1[i] == best_labels1[j]):
                state1[i-6] = j
    # print(state1)

    best_labels1 = best_labels1[6:len(best_labels1)]

    cv2.putText(img1, str(state1[0]), exchange(block_u1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img1, str(state1[1]), exchange(block_u2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img1, str(state1[2]), exchange(block_u3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img1, str(state1[3]), exchange(block_u4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img1, str(state1[4]), exchange(block_u5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img1, str(state1[5]), exchange(block_u6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img1, str(state1[6]), exchange(block_u7), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img1, str(state1[7]), exchange(block_u8), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img1, str(state1[8]), exchange(block_u9), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img1, str(state1[9]),  exchange(block_f1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img1, str(state1[10]), exchange(block_f2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img1, str(state1[11]), exchange(block_f3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img1, str(state1[12]), exchange(block_f4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img1, str(state1[13]), exchange(block_f5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img1, str(state1[14]), exchange(block_f6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img1, str(state1[15]), exchange(block_f7), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img1, str(state1[16]), exchange(block_f8), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img1, str(state1[17]), exchange(block_f9), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.imshow('img1', img1)
    # cv2.waitKey(0)

    sta_cube2 = []
    sta_cube2.append(piex2_r)
    sta_cube2.append(piex2_g)
    sta_cube2.append(piex2_b)
    sta_cube2.append(piex2_o)
    sta_cube2.append(piex2_y)
    sta_cube2.append(piex2_w)

    sta_cube2.append(img2[block_b1])        
    sta_cube2.append(img2[block_b2])
    sta_cube2.append(img2[block_b3])
    sta_cube2.append(img2[block_b4])
    sta_cube2.append(img2[block_b5])
    sta_cube2.append(img2[block_b6])
    sta_cube2.append(img2[block_b7])
    sta_cube2.append(img2[block_b8])
    sta_cube2.append(img2[block_b9])
    sta_cube2.append(img2[block_d1])        
    sta_cube2.append(img2[block_d2])
    sta_cube2.append(img2[block_d3])
    sta_cube2.append(img2[block_d4])
    sta_cube2.append(img2[block_d5])
    sta_cube2.append(img2[block_d6])
    sta_cube2.append(img2[block_d7])
    sta_cube2.append(img2[block_d8])
    sta_cube2.append(img2[block_d9])
    
    sta_cube2 = np.float32(sta_cube2)
    # criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10,1.0)
    # flags = cv2.KMEANS_RANDOM_CENTERS
    ret, best_labels2, centers = cv2.kmeans(sta_cube2, 6, None, criteria, 10, flags)
    # print(best_labels2)

    state2 = [None]*18
    for i in range(6,len(best_labels2)):
        for j in range(6):
            if (best_labels2[i] == best_labels2[j]):
                state2[i-6] = j
    # print(state2)

    best_labels2 = best_labels2[6:len(best_labels2)]

    cv2.putText(img2, str(state2[0]), exchange(block_b1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img2, str(state2[1]), exchange(block_b2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img2, str(state2[2]), exchange(block_b3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img2, str(state2[3]), exchange(block_b4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img2, str(state2[4]), exchange(block_b5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img2, str(state2[5]), exchange(block_b6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img2, str(state2[6]), exchange(block_b7), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img2, str(state2[7]), exchange(block_b8), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img2, str(state2[8]), exchange(block_b9), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img2, str(state2[9]),  exchange(block_d1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img2, str(state2[10]), exchange(block_d2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img2, str(state2[11]), exchange(block_d3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img2, str(state2[12]), exchange(block_d4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img2, str(state2[13]), exchange(block_d5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img2, str(state2[14]), exchange(block_d6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img2, str(state2[15]), exchange(block_d7), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img2, str(state2[16]), exchange(block_d8), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img2, str(state2[17]), exchange(block_d9), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.imshow('img2', img2)
    # cv2.waitKey(0)

    sta_cube3 = []
    sta_cube3.append(piex3_r)
    sta_cube3.append(piex3_g)
    sta_cube3.append(piex3_b)
    sta_cube3.append(piex3_o)
    sta_cube3.append(piex3_y)
    sta_cube3.append(piex3_w)

    sta_cube3.append(img3[block_l1])        
    sta_cube3.append(img3[block_l2])
    sta_cube3.append(img3[block_l3])
    sta_cube3.append(img3[block_l4])
    sta_cube3.append(img3[block_l5])
    sta_cube3.append(img3[block_l6])
    sta_cube3.append(img3[block_l7])
    sta_cube3.append(img3[block_l8])
    sta_cube3.append(img3[block_l9])
    sta_cube3 = np.float32(sta_cube3)
    # criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10,1.0)
    # flags = cv2.KMEANS_RANDOM_CENTERS
    ret, best_labels3, centers = cv2.kmeans(sta_cube3, 6, None, criteria, 10, flags)
    # print(best_labels3)

    state3 = [None]*9
    for i in range(6,len(best_labels3)):
        for j in range(6):
            if (best_labels3[i] == best_labels3[j]):
                state3[i-6] = j
    # print(state3)

    best_labels3 = best_labels3[6:len(best_labels3)]

    cv2.putText(img3, str(state3[0]), exchange(block_l1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img3, str(state3[1]), exchange(block_l2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img3, str(state3[2]), exchange(block_l3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img3, str(state3[3]), exchange(block_l4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img3, str(state3[4]), exchange(block_l5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img3, str(state3[5]), exchange(block_l6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img3, str(state3[6]), exchange(block_l7), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img3, str(state3[7]), exchange(block_l8), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img3, str(state3[8]), exchange(block_l9), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.imshow('img3', img3)
    # cv2.waitKey(0)

    sta_cube4 = []
    sta_cube4.append(piex4_r)
    sta_cube4.append(piex4_g)
    sta_cube4.append(piex4_b)
    sta_cube4.append(piex4_o)
    sta_cube4.append(piex4_y)
    sta_cube4.append(piex4_w)
    sta_cube4.append(img4[block_r1])        
    sta_cube4.append(img4[block_r2])
    sta_cube4.append(img4[block_r3])
    sta_cube4.append(img4[block_r4])
    sta_cube4.append(img4[block_r5])
    sta_cube4.append(img4[block_r6])
    sta_cube4.append(img4[block_r7])
    sta_cube4.append(img4[block_r8])
    sta_cube4.append(img4[block_r9])
    sta_cube4 = np.float32(sta_cube4)
    # criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10,1.0)
    # flags = cv2.KMEANS_RANDOM_CENTERS
    ret, best_labels4, centers = cv2.kmeans(sta_cube4, 6, None, criteria, 10, flags)
    # print(best_labels4)

    state4 = [None]*9
    for i in range(6,len(best_labels4)):
        for j in range(6):
            if (best_labels4[i] == best_labels4[j]):
                state4[i-6] = j
    # print(state4)

    best_labels4 = best_labels4[6:len(best_labels4)]

    cv2.putText(img4, str(state4[0]), exchange(block_r1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img4, str(state4[1]), exchange(block_r2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img4, str(state4[2]), exchange(block_r3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img4, str(state4[3]), exchange(block_r4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img4, str(state4[4]), exchange(block_r5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img4, str(state4[5]), exchange(block_r6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img4, str(state4[6]), exchange(block_r7), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img4, str(state4[7]), exchange(block_r8), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img4, str(state4[8]), exchange(block_r9), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.imshow('img4', img4)
    # cv2.waitKey(0)

    state_ = state1[0:9]+state4+state1[9:18]+state2[9:18]+state3+state2[0:9]
    # print(state_)
    # cv2.waitKey(0)
    # input('stop')


    state = ""

    img1 = cv2.circle(img1, exchange(block_u1), 3, (255, 0, 0), 2)
    img1 = cv2.circle(img1, exchange(block_u2), 3, (255, 0, 0), 2)
    img1 = cv2.circle(img1, exchange(block_u3), 3, (255, 0, 0), 2)
    img1 = cv2.circle(img1, exchange(block_u4), 3, (255, 0, 0), 2)
    img1 = cv2.circle(img1, exchange(block_u5), 3, (255, 0, 0), 2)
    img1 = cv2.circle(img1, exchange(block_u6), 3, (255, 0, 0), 2)
    img1 = cv2.circle(img1, exchange(block_u7), 3, (255, 0, 0), 2)
    img1 = cv2.circle(img1, exchange(block_u8), 3, (255, 0, 0), 2)
    img1 = cv2.circle(img1, exchange(block_u9), 3, (255, 0, 0), 2)

    img1 = cv2.circle(img1, exchange(block_f1), 3, (255, 0, 0), 2)
    img1 = cv2.circle(img1, exchange(block_f2), 3, (255, 0, 0), 2)
    img1 = cv2.circle(img1, exchange(block_f3), 3, (255, 0, 0), 2)
    img1 = cv2.circle(img1, exchange(block_f4), 3, (255, 0, 0), 2)
    img1 = cv2.circle(img1, exchange(block_f5), 3, (255, 0, 0), 2)
    img1 = cv2.circle(img1, exchange(block_f6), 3, (255, 0, 0), 2)
    img1 = cv2.circle(img1, exchange(block_f7), 3, (255, 0, 0), 2)
    img1 = cv2.circle(img1, exchange(block_f8), 3, (255, 0, 0), 2)
    img1 = cv2.circle(img1, exchange(block_f9), 3, (255, 0, 0), 2)
    # cv2.imshow('img1', img1)

    img2 = cv2.circle(img2, exchange(block_b1), 3, (255, 0, 0), 2)
    img2 = cv2.circle(img2, exchange(block_b2), 3, (255, 0, 0), 2)
    img2 = cv2.circle(img2, exchange(block_b3), 3, (255, 0, 0), 2)
    img2 = cv2.circle(img2, exchange(block_b4), 3, (255, 0, 0), 2)
    img2 = cv2.circle(img2, exchange(block_b5), 3, (255, 0, 0), 2)
    img2 = cv2.circle(img2, exchange(block_b6), 3, (255, 0, 0), 2)
    img2 = cv2.circle(img2, exchange(block_b7), 3, (255, 0, 0), 2)
    img2 = cv2.circle(img2, exchange(block_b8), 3, (255, 0, 0), 2)
    img2 = cv2.circle(img2, exchange(block_b9), 3, (255, 0, 0), 2)

    img2 = cv2.circle(img2, exchange(block_d1), 3, (255, 0, 0), 2)
    img2 = cv2.circle(img2, exchange(block_d2), 3, (255, 0, 0), 2)
    img2 = cv2.circle(img2, exchange(block_d3), 3, (255, 0, 0), 2)
    img2 = cv2.circle(img2, exchange(block_d4), 3, (255, 0, 0), 2)
    img2 = cv2.circle(img2, exchange(block_d5), 3, (255, 0, 0), 2)
    img2 = cv2.circle(img2, exchange(block_d6), 3, (255, 0, 0), 2)
    img2 = cv2.circle(img2, exchange(block_d7), 3, (255, 0, 0), 2)
    img2 = cv2.circle(img2, exchange(block_d8), 3, (255, 0, 0), 2)
    img2 = cv2.circle(img2, exchange(block_d9), 3, (255, 0, 0), 2)
    # cv2.imshow('img2', img2)

    img3 = cv2.circle(img3, exchange(block_l1), 3, (255, 0, 0), 2)
    img3 = cv2.circle(img3, exchange(block_l2), 3, (255, 0, 0), 2)
    img3 = cv2.circle(img3, exchange(block_l3), 3, (255, 0, 0), 2)
    img3 = cv2.circle(img3, exchange(block_l4), 3, (255, 0, 0), 2)
    img3 = cv2.circle(img3, exchange(block_l5), 3, (255, 0, 0), 2)
    img3 = cv2.circle(img3, exchange(block_l6), 3, (255, 0, 0), 2)
    img3 = cv2.circle(img3, exchange(block_l7), 3, (255, 0, 0), 2)
    img3 = cv2.circle(img3, exchange(block_l8), 3, (255, 0, 0), 2)
    img3 = cv2.circle(img3, exchange(block_l9), 3, (255, 0, 0), 2)
    # cv2.imshow('img3', img3)

    img4 = cv2.circle(img4, exchange(block_r1), 3, (255, 0, 0), 2)
    img4 = cv2.circle(img4, exchange(block_r2), 3, (255, 0, 0), 2)
    img4 = cv2.circle(img4, exchange(block_r3), 3, (255, 0, 0), 2)
    img4 = cv2.circle(img4, exchange(block_r4), 3, (255, 0, 0), 2)
    img4 = cv2.circle(img4, exchange(block_r5), 3, (255, 0, 0), 2)
    img4 = cv2.circle(img4, exchange(block_r6), 3, (255, 0, 0), 2)
    img4 = cv2.circle(img4, exchange(block_r7), 3, (255, 0, 0), 2)
    img4 = cv2.circle(img4, exchange(block_r8), 3, (255, 0, 0), 2)
    img4 = cv2.circle(img4, exchange(block_r9), 3, (255, 0, 0), 2)

    ff1 = state_[4]
    ff2 = state_[13]
    ff3 = state_[22]
    ff4 = state_[31]
    ff5 = state_[40]
    ff6 = state_[49]

    for i in state_:
        if(i == ff1):
            state=state+'U'
        elif(i == ff2):
            state=state+'R'
        elif(i == ff3):
            state=state+'F'
        elif(i == ff4):
            state=state+'D'
        elif(i == ff5):
            state=state+'L'
        elif(i == ff6):
            state=state+'B'
    # print('DEBUG')
    # print(state)
    # return state

    cubestate = state

    if (cube_judge() == False):
        return

    ok_flag = True
    # hardware.catch_both()
    turn_main_false()


    cv2.imwrite('1.jpg', img1)
    cv2.imwrite('2.jpg', img2)
    cv2.imwrite('3.jpg', img3)
    cv2.imwrite('4.jpg', img4)

def update_img_flag(ImgNum):
    global img_flag1,img_flag2,img_flag3,img_flag4,img_flag5,soving_flag
    if (ImgNum == 1):#更新第１张图片
        img_flag1 = 1
    elif (ImgNum == 2):
        img_flag2 = 1
    elif (ImgNum == 3):
        img_flag3 = 1
    elif (ImgNum == 4):
        img_flag4 = 1
    elif (ImgNum == 5):
        img_flag5 = 1
    elif (ImgNum == 0):#五张图片采集完成
        soving_flag = 1
def turn_false():
    global flag
    flag = False

def turn_main_false():
    global flag_main
    flag_main = False

def cube_judge_test():
    global cubestate
    # try:
    time_begin = time.time()
    # Solution = kociemba.solve(cubestate,None ,36)
    Solution = sv.solve(cubestate,36,0.001)
        
    print(Solution)
    # except:
    if (Solution[0] == 'E'):
        print('解算时间 = ' + str(time.time()-time_begin))
        print('识别失败')
        return False
    else:
        print('解算时间 = ' + str(time.time()-time_begin))
        print('识别成功')
        return True
        # kk = Solution.rfind(' ', 0,len(Solution) )
        # Solution = Solution[0:kk]
    # Solution = kociemba.solve(CubeState)

def cube_judge():
    global cubestate
    stand = 'URLBDF'
    time_begin = time.time()
    if (len(cubestate) != 54):
        print('识别失败　len(cubestate) != 54')
        # print('解算时间 = ' + str(time.time()-time_begin))
        return False
    for i in range(6):
        num = 0
        for j in range(54):
            if cubestate[j] == stand[i]:
                num += 1
        if (num != 9):
            print('识别失败 '+stand[i]+' != 9')
            # print('解算时间 = ' + str(time.time()-time_begin))
            return False
    print('识别成功')
    # print('解算时间 = ' + str(time.time()-time_begin))
    # Solution = kociemba.solve(cubestate)
    # print(Solution)
    return True
    
    

def Thread_UpdateImg():
    global img_flag1,img_flag2,img_flag3,img_flag4,img_flag5,soving_flag,sovingdown_flag
    global img_cube1,img_cube2,img_cube3,img_cube4,img_cube5
    global flag

    cap1 = cv2.VideoCapture(CAMERA_DEVICES[0])
    # cap1.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)# where 0.25 means "manual exposure, manual iris"  opencv4
    # cap1.set(cv2.CAP_PROP_EXPOSURE, 15)
    # cap1.set(cv2.CAP_PROP_CONTRAST, 30)
    # cap1.set(cv2.CAP_PROP_AUTO_WB, 0) #禁用白平衡
    # cap1.set(cv2.CAP_PROP_WB_TEMPERATURE, 4600)
    # cap1.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap1.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    # cap1.release()
    cap2 = cv2.VideoCapture(CAMERA_DEVICES[1])
    # cap2.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)# where 0.25 means "manual exposure, manual iris" opencv4
    # cap2.set(cv2.CAP_PROP_EXPOSURE, 14)
    # cap2.set(cv2.CAP_PROP_BRIGHTNESS, 0)  
    # cap2.set(cv2.CAP_PROP_CONTRAST, 30)
    # cap2.set(cv2.CAP_PROP_AUTO_WB, 0) #禁用白平衡
    # cap2.set(cv2.CAP_PROP_WB_TEMPERATURE, 4350)
    # cap2.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    # cap2.release()
    cap3 = cv2.VideoCapture(CAMERA_DEVICES[2])
    # cap3.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)# where 0.25 means "manual exposure, manual iris" opencv4
    # cap3.set(cv2.CAP_PROP_EXPOSURE, 8) 
    # cap3.set(cv2.CAP_PROP_BRIGHTNESS, -20)    
    # cap3.set(cv2.CAP_PROP_AUTO_WB, 0) #禁用白平衡
    # cap3.set(cv2.CAP_PROP_WB_TEMPERATURE, 4600)
    # cap3.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap3.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    # cap3.release()
    cap4 = cv2.VideoCapture(CAMERA_DEVICES[3])
    # cap4.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)# where 0.25 means "manual exposure, manual iris" opencv4
    # cap4.set(cv2.CAP_PROP_EXPOSURE, 10) 
    # cap4.set(cv2.CAP_PROP_BRIGHTNESS, 0)
    # cap4.set(cv2.CAP_PROP_CONTRAST, 20)
    # cap4.set(cv2.CAP_PROP_AUTO_WB, 0) #禁用白平衡
    # cap4.set(cv2.CAP_PROP_WB_TEMPERATURE, 4600)
    # cap4.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap4.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    # CV_CAP_PROP_CONTRAST
    # cap4.release()
    # cap3 = cv2.VideoCapture(3)
    # cap4 = cv2.VideoCapture(4)
    # cap2 = cv2.VideoCapture('/dev/video222')
    # cap4 = cv2.VideoCapture(4)
    while (flag_main):
        ret1,img_cube1,  = cap1.read()
        cv2.imshow("cube1",img_cube1)
        ret1,img_cube2,  = cap2.read()
        cv2.imshow("cube2",img_cube2)
        ret1,img_cube3,  = cap3.read()
        cv2.imshow("cube3",img_cube3)
        ret1,img_cube4,  = cap4.read()
        cv2.imshow("cube4",img_cube4)
        cv2.waitKey(1)
        if (flag == False):
            cube_recognize()

    cv2.destroyAllWindows()
    
    cv2.imwrite('11.jpg', img_cube1)
    cv2.imwrite('22.jpg', img_cube2)
    cv2.imwrite('33.jpg', img_cube3)
    cv2.imwrite('44.jpg', img_cube4)
    while(True):
        ret1,img_cube5,  = cap1.read()
        cv2.imshow("cube5",img_cube5)
        cv2.waitKey(1)

    # input()

    time.sleep(1)

def exchange(val):
    return (val[1], val[0])

queue_t = threading.Thread(target=Thread_UpdateImg)
queue_t.daemon = True
queue_t.start()
print("vision module start working!")
if __name__ == '__main__':
    input()
    turn_false()
    while (ok_flag != True):
        time.sleep(0.001)
    # time_begin = time.time()
    
    # print('识别时间 = ' + str(time.time()-time_begin))
    print('vision_.cubestate')
    print(cubestate)
    input()
    
