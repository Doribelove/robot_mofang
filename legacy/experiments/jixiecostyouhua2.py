import random
import time
from copy import deepcopy
import jixiecost
import twophase.solver as sv
import math

# 初始代价表              
transtable2 = transtable2 ={'U1': 6.7, 'U2': 4, 'U3': 7, 'D1': 4, 'D2': 1, 'D3': 4, 'F1': 6.3, 'F2': 4, 'F3': 7, 'I1': 10, 'I2': 7, 'I3': 10, 'l1': 10, 'l2': 7.7, 'l3': 10, 'Z1': 10, 'Z2': 7, 'Z3': 10, 'r1': 10, 'r2': 7, 'r3': 10, 'B1': 4, 'B2': 1.5, 'B3': 4}

#!/usr/bin/env python3
import time
from copy import deepcopy

import twophase.solver as sv

arm_slow_time_90 = 0.072
arm_slow_time_180 = 0.104
arm_Medium_time_90 = 0.074
arm_Medium_time_180 = 0.098
arm_fast_time_90 = 0.045#0.07
arm_fast_time_180 = 0.085
hand_open_time = 0.064#0.064
hand_close_time = 0.113#0.115
r_speed_state = 'initial'
l_speed_state = 'initial'
r_arm_act_time_90 = 0.22
r_arm_act_time_180 = 0.22
l_arm_act_time_90 = 0.22
l_arm_act_time_180 = 0.22

# 空转-----1当前爪夹　　2对面爪带动　　可复用
# 　带动-------对面爪夹　可复用
#  拧动－－－－不能复用
#  张开－－－－　1当前爪空转　　２对面带动　　不能复用
# 　闭合－－－－　1对面爪张开｜（可以）　　2当前爪拧动｜不能　　3对面拧动｜可以


def _KociembaTrans(KociembaCode):
    _Solution = []
    Cnt_Solution = 0  # 步数
    Step_temp = ''
    for i in range(len(KociembaCode)):
        if (KociembaCode[i] != ' '):  # 把'换成3
            Step_temp += KociembaCode[i]
        else:  # 一步结束 加进去
            _Solution.append(Step_temp)
            Step_temp = ''
            Cnt_Solution += 1
    return _Solution

def jiancost(code, cost1, cost2):
    if len(code) != 0:
        if code[-1] in ['B1', 'B3', 'F1', 'F3', 'l1', 'l3', 'r1', 'r3']:
            cost1 = cost1 - 6
            cost2 = cost2 - 2
            # print('big')
        elif code[-1] in ['D1', 'D3', 'U1', 'U3', 'I1', 'I3', 'Z1', 'Z3']:
            cost2 = cost2 - 6
            cost1 = cost1 - 2
            # print('little')
    return cost1, cost2

def _SolutionTransAndOptimize(Solution):  # 返回Solution的最优机械步骤（R->R\r  L->L\l）和最优时间成本
    Standard = 'UDFBRL'
    transtable1 = {'U': ('DUFBLR'),  # U U->D D->U L->R R->L
                   'D': ('UDFBRL'),
                   'F': ('UDBFLR'),  # F F->B B->F L->R R->L
                   'I': ('LRFBUD'),  # L L->D D->R R->U U->L
                   'l': ('UDLRFB'),  # l L->B B->R R->F F->L
                   'Z': ('RLFBDU'),  # R R->D D->L L->U U->R
                   'r': ('UDRLBF'),  # r R->B B->L L->F F->R
                   'B': ('UDFBRL')}

    cost = 0
    # cost_l = 0
    # cost_L = 0
    # Solution_l = []
    # Solution_L = []
    # Solution_temp_l = []
    # Solution_temp_L = []
    for i in range(len(Solution)):
        if Solution[i][0] == 'L':
            Solution_l = Solution[i:len(Solution)]  # 当前步骤到结束步骤（前面的已经优化好了）
            Solution_l[0] = Solution_l[0].replace('L', 'l')
            Solution_L = Solution[i:len(Solution)]  # 当前步骤到结束步骤（前面的已经优化好了）
            Solution_L[0] = Solution_L[0].replace('L', 'I')
            Solution_temp_l, cost_l = _SolutionTransAndOptimize(Solution_l)  # 进入110行
            Solution_temp_L, cost_L = _SolutionTransAndOptimize(Solution_L)
            _Solution = Solution[0:i]
            cost_L, cost_l = jiancost(_Solution, cost_L, cost_l)
            if cost_L < cost_l:
                # print('low:'+str(cost_L)+' high:'+str(cost_l))
                # print(Solution_temp_L)
                if (Solution_temp_L[0][0] == 'I'):
                    Solution_temp_L[0] = Solution_temp_L[0].replace('I', 'L')
                _Solution = _Solution + Solution_temp_L
                cost = cost + cost_L
                return _Solution, cost
            else:
                # print('1low:' + str(cost_l) + ' 1high:' + str(cost_L))
                # print(Solution_temp_l)
                _Solution = _Solution + Solution_temp_l
                cost = cost + cost_l
                return _Solution, cost
        elif Solution[i][0] == 'R':
            Solution_r = Solution[i:len(Solution)]
            Solution_r[0] = Solution_r[0].replace('R', 'r')
            Solution_R = Solution[i:len(Solution)]
            Solution_R[0] = Solution_R[0].replace('R', 'Z')
            Solution_temp_r, cost_r = _SolutionTransAndOptimize(Solution_r)
            Solution_temp_R, cost_R = _SolutionTransAndOptimize(Solution_R)
            _Solution = Solution[0:i]
            cost_R, cost_r = jiancost(_Solution, cost_R, cost_r)
            if cost_R < cost_r:
                # print('2low:'+str(cost_R)+' 2high:'+str(cost_r))
                if (Solution_temp_R[0][0] == 'Z'):
                    Solution_temp_R[0] = Solution_temp_R[0].replace('Z', 'R')
                _Solution = _Solution + Solution_temp_R
                cost = cost + cost_R
                return _Solution, cost
            else:
                # print('3low:'+str(cost_r)+' 3high:'+str(cost_R))
                _Solution = _Solution + Solution_temp_r
                cost = cost + cost_r
                return _Solution, cost
        else:  # 如果当前步骤不是Ｌ或Ｒ，则不需要优化．　　将当前步骤的成本加上，后续步骤转换
            for j in range((i + 1), len(Solution)):
                for face in range(len(Standard)):
                    if (Solution[j][0] == Standard[face]):
                        Solution[j] = Solution[j].replace(Standard[face], transtable1[Solution[i][0]][face])
                        break
            if i == len(Solution) - 1:
                cost = cost + transtable2[Solution[i]]
            else:
                if Solution[i] in ['D1', 'D3', 'U1', 'U3', 'I1', 'I3', 'Z1', 'Z3']:
                    if Solution[i + 1][0] == 'U':
                        cost = cost + transtable2[Solution[i]] - 2
                    else:
                        cost = cost + transtable2[Solution[i]]
                elif Solution[i] in ['B1', 'B3', 'F1', 'F3', 'l1', 'l3', 'r1', 'r3']:
                    if Solution[i + 1][0] == 'F':
                        cost = cost + transtable2[Solution[i]] - 2
                    else:
                        cost = cost + transtable2[Solution[i]]
                else:
                    cost = cost + transtable2[Solution[i]]
    for i in range(len(Solution)):
        # cost = cost + transtable[Solution[i][0]][1]
        if (Solution[i][0] == 'Z'):
            Solution[i] = Solution[i].replace('Z', 'R')
        if (Solution[i][0] == 'I'):
            Solution[i] = Solution[i].replace('I', 'L')

    return Solution, cost


def time_act(Action):
    if (Action[1] == 'slow'):
        if (Action[2] == 180):
            return arm_slow_time_180
        else:
            return arm_slow_time_90
    elif (Action[1] == 'Medium'):
        if (Action[2] == 180):
            return arm_Medium_time_180
        else:
            return arm_Medium_time_90
    elif (Action[1] == 'fast'):
        if (Action[2] == 180):
            return arm_fast_time_180
        else:
            return arm_fast_time_90
    elif (Action[1] == 'open'):
        return hand_open_time
    elif (Action[1] == 'close'):
        return hand_close_time


def jixie1(code):
    dict1 = {'D1': ['zd3', 'fw1'],
             'D2': ['zd2'],
             'D3': ['zd1', 'fw1'],
             # D Coordinate has no change
             'B1': ['zb3', 'fw3'],
             'B2': ['zb2'],
             'B3': ['zb1', 'fw3'],
             # B Coordinate has no change
             'F1': ['tz1', 'zb3', 'fw3'],
             'F2': ['tz1', 'zb2'],
             'F3': ['tz1', 'zb1', 'fw3'],
             # F F->B B->F L->R R->L
             'U1': ['tz2', 'zd3', 'fw1'],
             'U2': ['tz2', 'zd2'],
             'U3': ['tz2', 'zd1', 'fw1'],
             # U U->D D->U L->R R->L
             'L1': ['tz3', 'zd3', 'fw1'],
             'L2': ['tz3', 'zd2'],
             'L3': ['tz3', 'zd1', 'fw1'],
             # L L->D D->R R->U U->L
             'l1': ['tz4', 'zb3', 'fw3'],
             'l2': ['tz4', 'zb2'],
             'l3': ['tz4', 'zb1', 'fw3'],
             # l L->B B->R R->F F->L
             'R1': ['tz5', 'zd3', 'fw1'],
             'R2': ['tz5', 'zd2'],
             'R3': ['tz5', 'zd1', 'fw1'],
             # R R->D D->L L->U U->R
             'r1': ['tz6', 'zb3', 'fw3'],
             'r2': ['tz6', 'zb2'],
             'r3': ['tz6', 'zb1', 'fw3'],
             # r R->B B->L L->F F->R
             }
    Step_list = []
    for Commend in code:
        for step in dict1[Commend]:
            Step_list.append(step)
    Step_list.append(('None', 'None'))
    return Step_list


def youhua1(code):
    steplist = []
    jump = 0
    for i in range(len(code) - 1):
        if jump == 1:
            jump = 0
            continue
        if code[i] == 'fw1':
            if code[i + 1] == 'tz2':
                steplist.append('ft12')
                jump = 1
                continue
            elif code[i + 1] == 'tz4':
                steplist.append('ft14')
                jump = 1
                continue
            elif code[i + 1] == 'tz6':
                steplist.append('ft16')
                jump = 1
                continue
            else:
                steplist.append('fw1')
                continue
        elif code[i] == 'fw3':
            if code[i + 1] == 'tz1':
                steplist.append('ft31')
                jump = 1
                continue
            elif code[i + 1] == 'tz3':
                steplist.append('ft33')
                jump = 1
                continue
            elif code[i + 1] == 'tz5':
                steplist.append('ft35')
                jump = 1
                continue
            else:
                steplist.append('fw3')
                continue
        else:
            steplist.append(code[i])
    if steplist[-1] in ['fw1', 'fw3']:
        del steplist[-1]
    return steplist


def jixie2(code):
    dict2 = {'zd3': [('LW', 'Medium', -90)],
             'fw1': [('LH', 'open'), ('LW', 'fast', 90), ('LH', 'close')],
             'zd2': [('LW', 'Medium', 180)],
             'zd1': [('LW', 'Medium', 90)],
             # D Coordinate has no change
             'zb3': [('RW', 'Medium', -90)],
             'fw3': [('RH', 'open'), ('RW', 'fast', 90), ('RH', 'close')],
             'zb2': [('RW', 'Medium', 180)],
             'zb1': [('RW', 'Medium', 90)],
             # B Coordinate has no change
             'tz1': [('RH', 'open'), ('LW', 'slow', 180), ('RH', 'close')],
             # F F->B B->F L->R R->L
             'tz2': [('LH', 'open'), ('RW', 'slow', 180), ('LH', 'close')],
             # U U->D D->U L->R R->L
             'tz3': [('LH', 'open'), ('RW', 'slow', -90), ('LH', 'close'), ('RH', 'open'), ('RW', 'fast', 90),
                     ('RH', 'close')],
             # L L->D D->R R->U U->L
             'tz4': [('RH', 'open'), ('LW', 'slow', 90), ('RH', 'close'), ('LH', 'open'), ('LW', 'fast', -90),
                     ('LH', 'close')],
             # l L->B B->R R->F F->L
             'tz5': [('LH', 'open'), ('RW', 'slow', 90), ('LH', 'close'), ('RH', 'open'), ('RW', 'fast', -90),
                     ('RH', 'close')],
             # R R->D D->L L->U U->R
             'tz6': [('RH', 'open'), ('LW', 'slow', -90), ('RH', 'close'), ('LH', 'open'), ('LW', 'fast', 90),
                     ('LH', 'close')],
             'ft12': [('LH', 'open'), ('LW', 'slow', 90), ('RW', 'slow', 180), ('LH', 'close')],
             'ft14': [('RH', 'open'), ('LW', 'slow', 90), ('RH', 'close')],
             'ft16': [('RH', 'open'), ('LW', 'slow', -90), ('RH', 'close')],
             'ft31': [('RH', 'open'), ('RW', 'slow', 90), ('LW', 'slow', 180), ('RH', 'close')],
             'ft33': [('LH', 'open'), ('RW', 'slow', -90), ('LH', 'close')],
             'ft35': [('LH', 'open'), ('RW', 'slow', 90), ('LH', 'close')],
             # r R->B B->L L->F F->R
             }
    Step_list = []
    Step_list_Optimized = []
    JumpFlag = 0
    for Commend in code:
        for step in dict2[Commend]:
            Step_list.append(step)
    Step_list.append(('None', 'None'))
    for step_num in range(len(Step_list) - 1):  # 减去('None','None')
        if (JumpFlag == 1):  #
            JumpFlag = 0
            continue
        if (Step_list[step_num][0] == Step_list[step_num + 1][0] and Step_list[step_num][
            1] == 'close'):  # 如果当前步和下步都是同一只手，并且当前步是关闭（下步肯定是打开），直接跳过这两步
            JumpFlag = 1
            continue
        else:
            Step_list_Optimized.append(Step_list[step_num])
    return Step_list_Optimized


def quanjie(code):
    #code1 = _KociembaTrans(code)
    code2, costb = _SolutionTransAndOptimize(code)
    code3 = jixie1(code2)
    code4 = youhua1(code3)
    code5 = jixie2(code4)
    return len(code5)


def is_same_category(c1, c2):
    pairs = [('U', 'D'), ('D', 'U'), ('F', 'B'), ('B', 'F'), ('R', 'L'), ('L', 'R')]
    return (c1, c2) in pairs


def duichen(st, code):
    qcode = []
    if st >= len(code) - 1:
        qcode.append(deepcopy(code))
        return qcode
    for i in range(st, len(code) - 1):
        if is_same_category(code[i][0], code[i + 1][0]):
            code1 = deepcopy(code)
            code1[i], code1[i + 1] = code1[i + 1], code1[i]
            qcode.extend(duichen(i + 1, code1))
            # 这里的原始code添加可能是不必要的，取决于具体需求
    qcode.append(deepcopy(code))
    return qcode


def jisuan(st, code):
    qcode = duichen(st, code)
    print(qcode)
    print(len(qcode))
    l = []
    time1=time.time()
    qqcode = deepcopy(qcode)
    for j in range(len(qcode)):
        code2, costb = _SolutionTransAndOptimize(qqcode[j])
        code3 = jixie1(code2)
        code4 = youhua1(code3)
        code5 = jixie2(code4)
        l.append(len(code5))
    print(l)
    print(time.time()-time1)
    # 找到l中的最小值及其索引
    min_value = min(l)
    m = l.index(min_value)
    # 返回对应的最小全解值的qcode
    return qcode[m]

def sousuo(code):
    code1 = [m.name for m in code]
    code3, cost = _SolutionTransAndOptimize(code1)
    return cost

# 假设这个函数包含了jixiecost.py中机械臂操作的主逻辑
def calculate_timejixie(transtable):
    # 替换掉`_SolutionTransAndOptimize`函数中使用的代价表
    global transtable2
    transtable2 = transtable

    # 剩余的代码逻辑，假设该函数会使用`transtable2`
    cubestring = 'RUFFULUDLDUUBRRFRBLBBLFRUULBFDLDFFURDDBLLDRFRLBFDBBDRU'
    Solution = sv.solve(cubestring, 0, 0.08)
    Solution = _KociembaTrans(Solution)

    realsolution, costbushu = _SolutionTransAndOptimize(Solution)
    s = jixie1(realsolution)
    y = youhua1(s)
    z = jixie2(y)

    timejixie = 0
    for step in z:
        timejixie += time_act(step)

    return timejixie

def total_timejixie_over_10_runs(transtable):
    total_timejixie1 = 0
    maxtime=0
    mintime=999
    for i in range(52):
        k= calculate_timejixie(transtable)
        total_timejixie1 += k
        maxtime=max(maxtime,k)
        mintime=min(mintime,k)
    
    print(f"Total timejixie over 10 runs: {(total_timejixie1-maxtime-mintime)/50}")
    return (total_timejixie1-maxtime-mintime)/50

# 优化代价表的函数
def optimize_cost_table(transtable, iterations=100):
    best_table = deepcopy(transtable)
    best_time = float('inf')

    for i in range(iterations):
        # 随机调整某个操作的代价
        new_table = deepcopy(best_table)
        key = random.choice(list(new_table.keys()))
        a= math.ceil(random.uniform(-8, 8))  # 假设代价在1到15之间随机变化
        new_table[key] +=a/10
        # 使用调整后的代价表计算总时间
        current_time = total_timejixie_over_10_runs(new_table)

        if current_time < best_time:
            best_time = current_time
            best_table = deepcopy(new_table)


        print(f"Iteration {i+1}: Best Time = {best_time}")

    return best_table

# 执行优化
optimized_table = optimize_cost_table(transtable2, iterations=10)
print("Optimized Cost Table:", optimized_table)
input()
