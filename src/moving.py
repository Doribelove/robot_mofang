#!/usr/bin/env python3
import math
import hardware
import time
import odrive
import KociembaTrans
import kociemba

# 空转-----1当前爪夹　　2对面爪带动　　可复用
#　带动-------对面爪夹　可复用
#  拧动－－－－不能复用
#  张开－－－－　1当前爪空转　　２对面带动　　不能复用
#　闭合－－－－　1对面爪张开｜（可以）　　2当前爪拧动｜不能　　3对面拧动｜可以

arm_fast_time_180 = 0.085
r_arm_act_time_90 = 0.22
r_arm_act_time_180 = 0.22
l_arm_act_time_90 = 0.22
l_arm_act_time_180 = 0.22
# 80速度
# arm_slow_time_90 = 0.092
# arm_slow_time_180 = 0.122
# arm_Medium_time_90 = 0.082
# arm_Medium_time_180 = 0.105
# arm_fast_time_90 = 0.07#0.07
# arm_fast_time_180 = 0.09
# hand_open_time = 0.062#0.08
# hand_close_time = 0.115#0.09
# r_speed_state = 'initial'
# l_speed_state = 'initial'
# r_arm_act_time_90 = 0.22
# r_arm_act_time_180 = 0.22
# l_arm_act_time_90 = 0.22
# l_arm_act_time_180 = 0.22

# #90
# arm_slow_time_90 = 0.085
# arm_slow_time_180 = 0.115
# arm_Medium_time_90 = 0.078
# arm_Medium_time_180 = 0.098
# arm_fast_time_90 = 0.068#0.07
# arm_fast_time_180 = 0.09
# hand_open_time = 0.06#0.064
# hand_close_time = 0.115#0.115
# r_speed_state = 'initial'
# l_speed_state = 'initial'
# r_arm_act_time_90 = 0.22
# r_arm_act_time_180 = 0.22
# l_arm_act_time_90 = 0.22
# l_arm_act_time_180 = 0.22

# # 50sudu
# # arm_slow_time_90 = 0.055
# # arm_slow_time_180 = 0.094
# arm_slow_time_90 = 0.06
# arm_slow_time_180 = 0.105
# arm_Medium_time_90 = 0.0615
# arm_Medium_time_180 = 0.098
# arm_fast_time_90 = 0.0265#0.07
# hand_open_time = 0.06#0.064
# hand_close_time = 0.11#0.115
# r_speed_state = 'initial'
# l_speed_state = 'initial'

# #60sudu
# arm_slow_time_90 = 0.052
# arm_slow_time_180 = 0.092
# arm_Medium_time_90 = 0.06
# arm_Medium_time_180 = 0.098
# arm_fast_time_90 = 0.026#0.07
# hand_open_time = 0.058#0.064
# hand_close_time = 0.109#0.115
# r_speed_state = 'initial'
# l_speed_state = 'initial'

#chechi
arm_slow_time_90 = 0.065
arm_slow_time_180 = 0.10
arm_Medium_time_90 = 0.078
arm_Medium_time_180 = 0.102
arm_fast_time_90 = 0.075#0.07
hand_open_time = 0.068#0.064
hand_close_time = 0.12#0.115
r_speed_state = 'initial'
l_speed_state = 'initial'

# arm_slow_time_90 = 0.12
# # arm_slow_time_90 = 0.054
# # arm_slow_time_180 = 0.093
# arm_slow_time_180 = 0.15
# arm_Medium_time_90 = 0.12
# arm_Medium_time_180 = 0.15
# arm_fast_time_90 = 0.1#0.07
# hand_open_time = 0.14#0.064
# hand_close_time = 0.15#0.115
# r_speed_state = 'initial'
# l_speed_state = 'initial'
# arm_fast_time_180 = 0.085
# r_arm_act_time_90 = 0.22
# r_arm_act_time_180 = 0.22
# l_arm_act_time_90 = 0.22
# l_arm_act_time_180 = 0.22

time_testnow = time.time()
angleR=0
angleL=0

def _Acting(Action, s_time=0):
    global time_testnow
    global angleR,angleL
    global r_speed_state, l_speed_state
    global r_arm_act_time_90, r_arm_act_time_180, l_arm_act_time_90, l_arm_act_time_180
    time_testnow=time.time()
    if (Action[0] == 'RW'): #axis0　右臂
        #调速
        if(Action[1] == 'slow' and r_speed_state != Action[1]):
            hardware.arm_right_slow()
            time.sleep(0.02)
            r_arm_act_time_90 = arm_slow_time_90
            r_arm_act_time_180 = arm_slow_time_180
            r_speed_state = 'slow'
        elif(Action[1] == 'Medium' and r_speed_state != Action[1]):
            hardware.arm_right_Medium()
            time.sleep(0.02)
            r_arm_act_time_90 = arm_Medium_time_90
            r_arm_act_time_180 = arm_Medium_time_180
            r_speed_state = 'Medium'
        elif(Action[1] == 'fast' and r_speed_state != Action[1]):
            hardware.arm_right_fast()
            time.sleep(0.02)
            r_arm_act_time_90 = arm_fast_time_90
            r_arm_act_time_180 = arm_fast_time_180
            r_speed_state = 'fast'
        #旋转
        if (Action[2] == 90):
           hardware.arm0_rotate90_clockwise()
           print("R90\n")
           print(time.time()-time_testnow)
           time_testnow=time.time()
           angleR+=1
           time.sleep(r_arm_act_time_90)
        elif (Action[2] == -90):
           hardware.arm0_rotate90_anticlockwise()
           print("R90\n")
           print(time.time()-time_testnow)
           time_testnow=time.time()
           angleR+=1
           time.sleep(r_arm_act_time_90)
        elif (Action[2] == 180): 
           hardware.arm0_rotate180_clockwise()
           print("R180\n")
           print(time.time()-time_testnow)
           time_testnow=time.time()
           time.sleep(r_arm_act_time_180)
       
    elif (Action[0] == 'LW'): #axis1　左臂
       # print(hardware.odrv_up.axis0.trap_traj.config.accel_limit)
       # print(hardware.odrv_up.axis1.trap_traj.config.accel_limit)
       # print(hardware.odrv_up.axis0.trap_traj.config.decel_limit)
       # print(hardware.odrv_up.axis1.trap_traj.config.decel_limit)
       # print('')
        #调速
        if(Action[1] == 'slow' and l_speed_state != Action[1]):
            hardware.arm_left_slow()
            time.sleep(0.02)
            l_arm_act_time_90 = arm_slow_time_90
            l_arm_act_time_180 = arm_slow_time_180
            l_speed_state = 'slow'
        elif(Action[1] == 'Medium' and l_speed_state != Action[1]):
            hardware.arm_left_Medium()
            time.sleep(0.02)
            l_arm_act_time_90 = arm_Medium_time_90
            l_arm_act_time_180 = arm_Medium_time_180
            l_speed_state = 'Medium'
        elif(Action[1] == 'fast' and l_speed_state != Action[1]):
            hardware.arm_left_fast()
            time.sleep(0.02)
            l_arm_act_time_90 = arm_fast_time_90
            l_arm_act_time_180 = arm_fast_time_180
            l_speed_state = 'fast'
        #旋转
        if (Action[2] == 90):
            # if (l_speed_state != 'fast'):
            #     hardware.arm1_rotate90_clockwise()
            # else:
            # hardware.odrv.axis1.controller.config.inertia = 0.023
            hardware.arm1_rotate90_clockwise()
            print("L90\n")
            print(time.time()-time_testnow)
            time_testnow=time.time()
            angleL+=1
            time.sleep(l_arm_act_time_90)
        elif (Action[2] == -90):
            # if (l_speed_state != 'fast'):
            #     hardware.arm1_rotate90_anticlockwise()
            # else:
            # hardware.odrv.axis1.controller.config.inertia = 0.023
            hardware.arm1_rotate90_anticlockwise()
            print("-L90\n")
            print(time.time()-time_testnow)
            time_testnow=time.time()
            angleL+=1
            time.sleep(l_arm_act_time_90)
        elif (Action[2] == 180): 
            # if (l_speed_state != 'fast'):
            #     hardware.arm1_rotate180_clockwise()
            # else:
            # hardware.odrv.axis1.controller.config.inertia = 0.04
            hardware.arm1_rotate180_clockwise()
            print("L180\n")
            print(time.time()-time_testnow)
            time_testnow=time.time()
            time.sleep(l_arm_act_time_180)

    elif (Action[0] == 'RH'): #右手
       if (Action[1] == 'open'): 
           hardware.loosen_hand0()
           time.sleep(hand_open_time)
       if (Action[1] == 'close'):
           hardware.catch_hand0()
           time.sleep(hand_close_time+s_time)
           print('s_time='+str(s_time)+' sleep='+str(hand_close_time+s_time))
    elif (Action[0] == 'LH'): #左手
       if (Action[1] == 'open'):
           hardware.loosen_hand1()
           time.sleep(hand_open_time)
       if (Action[1] == 'close'):
           hardware.catch_hand1()
           time.sleep(hand_close_time+s_time)
           print('s_time='+str(s_time)+' sleep='+str(hand_close_time+s_time))


def steps_Move(steps):
    time_begin = time.time()
    #for step in steps:
    for i in range(len(steps)):
       # input("按键动作")
       #time.sleep(0.1)
        print(steps[i])
        if (steps[i][1] == 'close' and i != len(steps)-1 and steps[i+1][1] == 'Medium' and steps[i][0][0] != steps[i+1][0][0]):
            print('优化')
            _Acting(steps[i],0.004)
        else:
            _Acting(steps[i])
    print('time = ' + str(time.time()-time_begin))
    print("angleL=")
    print(angleL)
    print("angleR=")
    print(angleR)
    if(angleL%2==1):
        _Acting(('LH','open'))
        _Acting(('LW','fast','90'))
    if(angleR%2==1):
        _Acting(('RH','open'))
        _Acting(('RW','fast','90'))

def Solution_Move(Solution): #1 means clockwise 90 degree
                     #2 means 180 degree
                     #3 means anticlockwise 90 degree
                     #RW RH means motor0 of each odrive
                     #LW LH means motor1 of each odrive
       
    dict ={   'D1': [('LW','Medium',-90), ('LH', 'open'),('LW','fast',90),('LH', 'close')],
              'D2': [('LW','Medium',180)],
              'D3': [('LW','Medium',90), ('LH', 'open'),('LW','fast',-90),('LH', 'close')],
              #D Coordinate has no change
              'B1': [('RW','Medium',-90), ('RH','open'),('RW','fast',90),('RH', 'close')],
              'B2': [('RW','Medium',180)],
              'B3': [('RW','Medium',90), ('RH','open'),('RW','fast',-90),('RH', 'close')],
              #B Coordinate has no change
              'F1': [('RH', 'open'),('LW','slow',180),('RH', 'close'),
                     ('RW','Medium',-90), ('RH', 'open'),('RW','fast',90),('RH', 'close')],
              'F2': [('RH', 'open'),('LW','slow',180),('RH', 'close'),
                     ('RW','Medium',180)],
              'F3': [('RH', 'open'),('LW','slow',180),('RH', 'close'),
                     ('RW','Medium',90), ('RH', 'open'),('RW','fast',-90),('RH', 'close')],
              #F F->B B->F L->R R->L
              'U1': [('LH', 'open'),('RW','slow',180),('LH', 'close'),
                     ('LW','Medium',-90), ('LH', 'open'),('LW','fast',90),('LH', 'close')],
              'U2': [('LH', 'open'),('RW','slow',180),('LH', 'close'),
                     ('LW','Medium',180)],
              'U3': [('LH', 'open'),('RW','slow',180),('LH', 'close'),
                     ('LW','Medium',90), ('LH', 'open'),('LW','fast',-90),('LH', 'close')],
              #U U->D D->U L->R R->L
              'L1': [('LH', 'open'),('RW','slow',-90),('LH', 'close'),('RH', 'open'),('RW','fast',90),('RH', 'close'),
                     ('LW','Medium',-90), ('LH', 'open'),('LW','fast',90),('LH', 'close')],
              'L2': [('LH', 'open'),('RW','slow',-90),('LH', 'close'),('RH', 'open'),('RW','fast',90),('RH', 'close'),
                     ('LW','Medium',180)],
              'L3': [('LH', 'open'),('RW','slow',-90),('LH', 'close'),('RH', 'open'),('RW','fast',90),('RH', 'close'),
                     ('LW','Medium',90), ('LH', 'open'),('LW','fast',-90),('LH', 'close')],
              #L L->D D->R R->U U->L
              'l1': [('RH', 'open'),('LW','slow',90),('RH', 'close'),('LH', 'open'),('LW','fast',-90),('LH', 'close'),
                     ('RW','Medium',-90), ('RH', 'open'),('RW','fast',90),('RH', 'close')],
              'l2': [('RH', 'open'),('LW','slow',90),('RH', 'close'),('LH', 'open'),('LW','fast',-90),('LH', 'close'),
                     ('RW','Medium',180)],
              'l3': [('RH', 'open'),('LW','slow',90),('RH', 'close'),('LH', 'open'),('LW','fast',-90),('LH', 'close'),
                     ('RW','Medium',90), ('RH', 'open'),('RW','fast',-90),('RH', 'close')],
              #l L->B B->R R->F F->L
              'R1': [('LH', 'open'),('RW','slow',90),('LH', 'close'),('RH', 'open'),('RW','fast',-90),('RH', 'close'),
                     ('LW','Medium',-90), ('LH', 'open'),('LW','fast',90),('LH', 'close')],
              'R2': [('LH', 'open'),('RW','slow',90),('LH', 'close'),('RH', 'open'),('RW','fast',-90),('RH', 'close'),
                     ('LW','Medium',180)],
              'R3': [('LH', 'open'),('RW','slow',90),('LH', 'close'),('RH', 'open'),('RW','fast',-90),('RH', 'close'),
                     ('LW','Medium',90), ('LH', 'open'),('LW','fast',-90),('LH', 'close')],
              #R R->D D->L L->U U->R
              'r1': [('RH', 'open'),('LW','slow',-90),('RH', 'close'),('LH', 'open'),('LW','fast',90),('LH', 'close'),
                     ('RW','Medium',-90), ('RH', 'open'),('RW','fast',90),('RH', 'close')],
              'r2': [('RH', 'open'),('LW','slow',-90),('RH', 'close'),('LH', 'open'),('LW','fast',90),('LH', 'close'),
                     ('RW','Medium',180)],
              'r3': [('RH', 'open'),('LW','slow',-90),('RH', 'close'),('LH', 'open'),('LW','fast',90),('LH', 'close'),
                     ('RW','Medium',90), ('RH', 'open'),('RW','fast',-90),('RH', 'close')],
              #r R->B B->L L->F F->R
            }
    Step_list = []
    for Commend in Solution:
       for step in dict[Commend]:
           Step_list.append(step)
    Step_list.append(('None','None'))
    Step_list_Optimized = []
    JumpFlag = 0
    cnt = 0#跳了多少步
    for step_num in range(len(Step_list)-1):   #减去('None','None')
       if (JumpFlag == 1):#
           JumpFlag = 0
           continue
       if (Step_list[step_num][0] == Step_list[step_num+1][0] and Step_list[step_num][1] == 'close'):#如果当前步和下步都是同一只手，并且当前步是关闭（下步肯定是打开），直接跳过这两步
           cnt = cnt+1
           JumpFlag = 1
           continue
       else:
           Step_list_Optimized.append(Step_list[step_num])
    print('Step_list:')
    print(Step_list)
    print('Step_list_Optimized:')
    print(Step_list_Optimized)
    print('cnt:')
    print(cnt)
    time_begin = time.time()
    for step in Step_list_Optimized:
       input("按键动作")
       time.sleep(0.5)
       _Acting(step)
    print('time = ' + str(time.time()-time_begin))
if __name__ == '__main__':
    Solution = kociemba.solve('RDLRUFLRDRUDLRLLBLUFBLFFUBURRBFDUUDBDUFBLBRDFFLFUBDDRB')
    realsolution = KociembaTrans.TransToRealSolution(Solution)
    Solution_Move(realsolution)
#     print(solution)