#!/usr/bin/env python3
# import sys
# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import time
import cv2
import threading
import numpy as np
# import kociemba
import twophase.solver  as sv
import hardware
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


#img1
    block_u1 = exchange((262,64))
    block_u2 = exchange((360,65))
    block_u3 = exchange((461,64))
    block_u4 = exchange((257,119))
    block_u5 = exchange((366,118))
    block_u6 = exchange((467,120))
    block_u7 = exchange((250,193))
    block_u8 = exchange((365,186))
    block_u9 = exchange((481,192))

    block_f1 = exchange((249,274))
    block_f2 = exchange((363,269))
    block_f3 = exchange((484,274))
    block_f4 = exchange((259,343))
    block_f5 = exchange((358,340))
    block_f6 = exchange((469,344))
    block_f7 = exchange((264,398))
    block_f8 = exchange((358,401))
    block_f9 = exchange((456,400))


#img2
    block_b1 = exchange((217,34))
    block_b2 = exchange((320,37))
    block_b3 = exchange((415,38))
    block_b4 = exchange((215,106))
    block_b5 = exchange((317,104))
    block_b6 = exchange((414,108))
    block_b7 = exchange((172,190))
    block_b8 = exchange((313,198))
    block_b9 = exchange((460,186))



    block_d1 = exchange((401,447))
    block_d2 = exchange((310,440))
    block_d3 = exchange((218,444))
    block_d4 = exchange((417,373))
    block_d5 = exchange((316,374))
    block_d6 = exchange((205,367))
    block_d7 = exchange((455,292))
    block_d8 = exchange((311,299))
    block_d9 = exchange((167,291))

#img3
    block_l1 = exchange((347,38))
    block_l2 = exchange((427,128))
    block_l3 = exchange((514,220))
    block_l4 = exchange((238,108))
    block_l5 = exchange((336,218))
    block_l6 = exchange((425,312))
    block_l7 = exchange((160,210))
    block_l8 = exchange((243,309))
    block_l9 = exchange((333,393))


#img4
    block_r1 = exchange((494,240))
    block_r2 = exchange((429,333))
    block_r3 = exchange((313,419))
    block_r4 = exchange((442,150))
    block_r5 = exchange((315,241))
    block_r6 = exchange((211,332))
    block_r7 = exchange((319,61))
    block_r8 = exchange((222,133))
    block_r9 = exchange((140,234))




    piex1_r = (49, 43, 162)
    piex1_g = (116, 218, 0)
    piex1_b = (197, 90, 0)
    piex1_o = (114, 133, 248)
    piex1_y = (137, 246, 168)
    piex1_w = (224, 201, 156)




    piex2_r = (49, 38, 140)
    piex2_g = (90, 202, 0)
    piex2_b = (194, 97, 0)
    piex2_o = (95, 115, 234)
    piex2_y = (113, 245, 162)
    piex2_w = (194, 180, 127)



    piex3_r = (5, 1, 83)
    piex3_g = (34, 150, 1)
    piex3_b = (126, 45, 0)
    piex3_o = (67, 93, 237)
    piex3_y = (79, 213, 161)
    piex3_w = (176, 169, 142)



    piex4_r = (49, 45, 148)
    piex4_g = (80, 195, 0)
    piex4_b = (191, 104, 10)
    piex4_o = (80, 111, 250)
    piex4_y = (67, 217, 157)
    piex4_w = (189, 184, 151)

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
    print(best_labels1)

    state1 = [None]*18
    for i in range(6,len(best_labels1)):
        for j in range(6):
            if (best_labels1[i] == best_labels1[j]):
                state1[i-6] = j
    print(state1)

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
    print(best_labels2)

    state2 = [None]*18
    for i in range(6,len(best_labels2)):
        for j in range(6):
            if (best_labels2[i] == best_labels2[j]):
                state2[i-6] = j
    print(state2)

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
    print(best_labels3)

    state3 = [None]*9
    for i in range(6,len(best_labels3)):
        for j in range(6):
            if (best_labels3[i] == best_labels3[j]):
                state3[i-6] = j
    print(state3)

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
    print(best_labels4)

    state4 = [None]*9
    for i in range(6,len(best_labels4)):
        for j in range(6):
            if (best_labels4[i] == best_labels4[j]):
                state4[i-6] = j
    print(state4)

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
    print(state_)
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
    print(state)
    # return state

    cubestate = state

    if (cube_judge() == False):
        return

    ok_flag = True
    hardware.catch_both()
    turn_main_false()
    

    # cv2.putText(img1, state[0], exchange(block_u1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img1, state[1], exchange(block_u2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img1, state[2], exchange(block_u3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img1, state[3], exchange(block_u4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img1, state[4], exchange(block_u5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img1, state[5], exchange(block_u6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img1, state[6], exchange(block_u7), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img1, state[7], exchange(block_u8), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img1, state[8], exchange(block_u9), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # cv2.putText(img4, state[9],  exchange(block_r1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img4, state[10], exchange(block_r2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img4, state[11], exchange(block_r3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img4, state[12], exchange(block_r4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img4, state[13], exchange(block_r5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img4, state[14], exchange(block_r6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img4, state[15], exchange(block_r7), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img4, state[16], exchange(block_r8), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img4, state[17], exchange(block_r9), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # cv2.putText(img1, state[18], exchange(block_f1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img1, state[19], exchange(block_f2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img1, state[20], exchange(block_f3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img1, state[21], exchange(block_f4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img1, state[22], exchange(block_f5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img1, state[23], exchange(block_f6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img1, state[24], exchange(block_f7), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img1, state[25], exchange(block_f8), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img1, state[26], exchange(block_f9), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # cv2.putText(img2, state[27], exchange(block_d1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img2, state[28], exchange(block_d2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img2, state[29], exchange(block_d3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img2, state[30], exchange(block_d4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img2, state[31], exchange(block_d5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img2, state[32], exchange(block_d6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img2, state[33], exchange(block_d7), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img2, state[34], exchange(block_d8), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img2, state[35], exchange(block_d9), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # cv2.putText(img3, state[36], exchange(block_l1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img3, state[37], exchange(block_l2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img3, state[38], exchange(block_l3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img3, state[39], exchange(block_l4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img3, state[46], exchange(block_l5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img3, state[41], exchange(block_l6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img3, state[42], exchange(block_l7), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img3, state[43], exchange(block_l8), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img3, state[44], exchange(block_l9), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)    

    # cv2.putText(img2, state[36], exchange(block_b1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img2, state[37], exchange(block_b2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img2, state[38], exchange(block_b3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img2, state[39], exchange(block_b4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img2, state[46], exchange(block_b5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img2, state[41], exchange(block_b6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img2, state[42], exchange(block_b7), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img2, state[43], exchange(block_b8), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(img2, state[44], exchange(block_b9), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)   

    # cv2.imshow('img1', img1)
    # cv2.imshow('img2', img2)
    # cv2.imshow('img3', img3)
    # cv2.imshow('img4', img4)

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

    cap1 = cv2.VideoCapture('/dev/video111')
    cap1.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)# where 0.25 means "manual exposure, manual iris"  opencv4
    cap1.set(cv2.CAP_PROP_EXPOSURE, 15)
    cap1.set(cv2.CAP_PROP_CONTRAST, 30)
    cap1.set(cv2.CAP_PROP_AUTO_WB, 0) #禁用白平衡
    cap1.set(cv2.CAP_PROP_WB_TEMPERATURE, 4600)
    cap1.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap1.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    # cap1.release()
    cap2 = cv2.VideoCapture('/dev/video222')
    cap2.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)# where 0.25 means "manual exposure, manual iris" opencv4
    cap2.set(cv2.CAP_PROP_EXPOSURE, 14)
    cap2.set(cv2.CAP_PROP_BRIGHTNESS, 0)  
    cap2.set(cv2.CAP_PROP_CONTRAST, 30)
    cap2.set(cv2.CAP_PROP_AUTO_WB, 0) #禁用白平衡
    cap2.set(cv2.CAP_PROP_WB_TEMPERATURE, 4350)
    cap2.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    # cap2.release()
    cap3 = cv2.VideoCapture('/dev/video333')
    cap3.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)# where 0.25 means "manual exposure, manual iris" opencv4
    cap3.set(cv2.CAP_PROP_EXPOSURE, 8) 
    cap3.set(cv2.CAP_PROP_BRIGHTNESS, -20)    
    cap3.set(cv2.CAP_PROP_AUTO_WB, 0) #禁用白平衡
    cap3.set(cv2.CAP_PROP_WB_TEMPERATURE, 4600)
    cap3.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap3.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    # cap3.release()
    cap4 = cv2.VideoCapture('/dev/video444')
    cap4.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)# where 0.25 means "manual exposure, manual iris" opencv4
    cap4.set(cv2.CAP_PROP_EXPOSURE, 10) 
    cap4.set(cv2.CAP_PROP_BRIGHTNESS, 0)
    cap4.set(cv2.CAP_PROP_CONTRAST, 20)
    cap4.set(cv2.CAP_PROP_AUTO_WB, 0) #禁用白平衡
    cap4.set(cv2.CAP_PROP_WB_TEMPERATURE, 4600)
    cap4.set(cv2.CAP_PROP_BUFFERSIZE, 1)
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
        # if (flag == False):
        cube_recognize()
        # cap1.release()
        # cap2 = cv2.VideoCapture(2)
        # ret1,img_cube2,  = cap2.read()
        # cv2.imshow("cube2",img_cube2)
        # cv2.waitKey(1)
        # cap2.release()
        
        # ret2,img_cube2,  = cap2.read()
        # ret3,img_cube3,  = cap3.read()
        # ret4,img_cube4,  = cap4.read()
    # cap2.release()
    # cap3 = cv2.VideoCapture('/dev/video333')
    # time.sleep(3)
    # ret1,img_cube3,  = cap3.read()
    # cv2.imshow("cube3",img_cube3)
    # cv2.waitKey(1)
    # cap3.release()
    # cap1 = cv2.VideoCapture('/dev/video111')
    # time.sleep(3)
    # ret1,img_cube1,  = cap1.read()
    # cv2.imshow("cube1",img_cube1)
    # cv2.waitKey(15)
    # cap1.release()
    # ret1,img_cube4,  = cap4.read()
    # cv2.imshow("cube4",img_cube4)
    # cv2.waitKey(10)
    # cap4.release()
    # cap1 = cv2.VideoCapture('/dev/video111')
    # cv2.imwrite('11.jpg', img_cube1)
    # cv2.imwrite('22.jpg', img_cube2)
    # cv2.imwrite('33.jpg', img_cube3)
    # cv2.imwrite('44.jpg', img_cube4)
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
    # global img_cube1,img_cube2,img_cube3,img_cube4
    # img_cube1 = cv2.imread('11.jpg')
    # img_cube2 = cv2.imread('22.jpg')
    # img_cube3 = cv2.imread('33.jpg')
    # img_cube4 = cv2.imread('44.jpg')
    # cube_recognize()
    # cv2.waitKey(0)
    # Solution = kociemba.solve(cubestate)
    # print(Solution)
    # cv2.imshow("cube1",img_cube1)
    input()
    turn_false()
    input()
    
