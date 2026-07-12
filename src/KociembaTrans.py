#!/usr/bin/env python3
from logging import root
import time
import kociemba
import copy
import moving
import odrive
def _KociembaTrans(KociembaCode):
    _Solution = []
    Cnt_Solution = 0    #步数
    Step_temp = ''
    for i in range(len(KociembaCode)):
        if (KociembaCode[i] != ' '):    #把'换成3
            if (KociembaCode[i] == '\''):
                Step_temp += '3'
            elif (KociembaCode[i] == '2'):
                Step_temp += '2'
            else:
                Step_temp += KociembaCode[i]
        else:           #一步结束 加进去
            _Solution.append(Step_temp)
            Step_temp = ''
            Cnt_Solution += 1
    _Solution.append(Step_temp)  #把最后一个加进去
    for i in range(len(_Solution)):     #把单字母后加1
        if (len(_Solution[i]) == 1):
            _Solution[i] += '1'
    return _Solution
def _SolutionTrans(Solution):
    Standard = 'UDFBRL'
    transtable = {'U' :'DUFBLR',#U U->D D->U L->R R->L
                  'D' :'UDFBRL',
                  'F' :'UDBFLR',#F F->B B->F L->R R->L
                  'L' :'LRFBUD',#L L->D D->R R->U U->L
                  'R' :'RLFBDU',#R R->D D->L L->U U->R
                  'B' :'UDFBRL'}
    for i in range(len(Solution)):
        for j in range((i+1),len(Solution)):
            for face in range(len(Standard)):
                if (Solution[j][0] == Standard[face]):
                    Solution[j] = Solution[j].replace(Standard[face],transtable[Solution[i][0]][face])
                    break
    return Solution

def _SolutionTransAndOptimize(Solution):#返回Solution的最优机械步骤（R->R\r  L->L\l）和最优时间成本
    Standard = 'UDFBRL'
    transtable = {'U' :('DUFBLR',0.4),#U U->D D->U L->R R->L
                  'D' :('UDFBRL',0),
                  'F' :('UDBFLR',0.4),#F F->B B->F L->R R->L

                  'I' :('LRFBUD',0.6),#L L->D D->R R->U U->L        
                  'l' :('UDLRFB',0.6),#l L->B B->R R->F F->L        

                  'Z' :('RLFBDU',0.6),#R R->D D->L L->U U->R        
                  'r' :('UDRLBF',0.6),#r R->B B->L L->F F->R        
                  'B' :('UDFBRL',0)}
    cost = 0
    # cost_l = 0
    # cost_L = 0
    # Solution_l = []
    # Solution_L = []
    # Solution_temp_l = []
    # Solution_temp_L = []
    for i in range(len(Solution)):
        if Solution[i][0] == 'L':
            Solution_l = Solution[i:len(Solution)]#当前步骤到结束步骤（前面的已经优化好了）
            Solution_l[0] = Solution_l[0].replace('L','l')
            Solution_L = Solution[i:len(Solution)]#当前步骤到结束步骤（前面的已经优化好了）
            Solution_L[0] = Solution_L[0].replace('L','I')
            Solution_temp_l,cost_l = _SolutionTransAndOptimize(Solution_l)#进入110行
            Solution_temp_L,cost_L = _SolutionTransAndOptimize(Solution_L)
            if cost_L < cost_l:         
                # print('low:'+str(cost_L)+' high:'+str(cost_l))
                # print(Solution_temp_L)
                _Solution = Solution[0:i]#之前的步骤（不包括当前步骤）
                if (Solution_temp_L[0][0] == 'I'):
                    Solution_temp_L[0] = Solution_temp_L[0].replace('I','L')
                _Solution = _Solution + Solution_temp_L
                cost = cost+cost_L
                return _Solution,cost
            else:
                # print('1low:'+str(cost_l)+' 1high:'+str(cost_L))
                # print(Solution_temp_l)
                _Solution = Solution[0:i]
                if (Solution_temp_l[0][0] == 'I'):#似乎不需要，因为l里面不可能有Ｉ
                    Solution_temp_l[0] = Solution_temp_l[0].replace('I','L')
                _Solution = _Solution + Solution_temp_l
                cost = cost+cost_l
                return _Solution,cost
        elif Solution[i][0] == 'R':
            Solution_r = Solution[i:len(Solution)]
            Solution_r[0] = Solution_r[0].replace('R','r')
            Solution_R = Solution[i:len(Solution)]
            Solution_R[0] = Solution_R[0].replace('R','Z')
            Solution_temp_r,cost_r = _SolutionTransAndOptimize(Solution_r)
            Solution_temp_R,cost_R = _SolutionTransAndOptimize(Solution_R)
            if cost_R < cost_r:
                # print('2low:'+str(cost_R)+' 2high:'+str(cost_r))
                _Solution = Solution[0:i]
                if (Solution_temp_R[0][0] == 'Z'):
                    Solution_temp_R[0] = Solution_temp_R[0].replace('Z','R')
                _Solution = _Solution + Solution_temp_R 
                cost = cost+cost_R
                return _Solution,cost
            else:
                # print('3low:'+str(cost_r)+' 3high:'+str(cost_R))
                _Solution = Solution[0:i]
                if (Solution_temp_r[0][0] == 'Z'):
                    Solution_temp_r[0] = Solution_temp_r[0].replace('Z','R')
                _Solution = _Solution + Solution_temp_r
                cost = cost+cost_r
                return _Solution,cost
        else:#如果当前步骤不是Ｌ或Ｒ，则不需要优化．　　将当前步骤的成本加上，后续步骤转换
            cost = cost + transtable[Solution[i][0]][1]#成本查表
            for j in range((i+1),len(Solution)):#后续步骤（不包括当前）　每个步骤都因为执行当前步骤而发生了变化
                for face in range(len(Standard)):
                    if (Solution[j][0] == Standard[face]):
                        Solution[j] = Solution[j].replace(Standard[face],transtable[Solution[i][0]][0][face])
                        break
    for i in range(len(Solution)):
        # cost = cost + transtable[Solution[i][0]][1]
        if (Solution[i][0] == 'Z'):
            Solution[i] = Solution[i].replace('Z','R')
        if (Solution[i][0] == 'I'):
            Solution[i] = Solution[i].replace('I','L')
    
    return Solution, cost
def TransToRealSolution(KociembaCode):
    # solution = _KociembaTrans(KociembaCode)#指令转换为123
    solution = KociembaCode.split(" ")
    print("转换符号后：")
    print(solution)
    print('魔方步骤数：'+str(len(solution)))
    #return _SolutionTransAndOptimize(solution)
    return _SolutionTransAndOptimizeDfs(solution)

def time_act(Action):
    if(Action[1] == 'slow'):
        if(Action[2] == 180):
            return moving.arm_slow_time_180
        else:
            return moving.arm_slow_time_90
    elif(Action[1] == 'Medium'):
        if(Action[2] == 180):
            return moving.arm_Medium_time_180
        else:
            return moving.arm_Medium_time_90
    elif(Action[1] == 'fast'):
        if(Action[2] == 180):
            return moving.arm_fast_time_180
        else:
            return moving.arm_fast_time_90
    elif (Action[1] == 'open'):
           return moving.hand_open_time
    elif (Action[1] == 'close'):
           return moving.hand_close_time

def steps_trans(Solution):
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
    time = 0
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
    # print('Step_list:')
    # print(Step_list)
    # print('Step_list_Optimized:')
    # print(Step_list_Optimized)
    # print('cnt:')
    # print(cnt)
    for step in Step_list_Optimized:
        time += time_act(step)
    return Step_list_Optimized, time

def _SolutionTransAndOptimizeDfs(Solution):

    Standard = 'UDFBRL'
    transtable = {'U' :('DUFBLR',0.4),#U U->D D->U L->R R->L
                  'D' :('UDFBRL',0),
                  'F' :('UDBFLR',0.4),#F F->B B->F L->R R->L

                  'I' :('LRFBUD',0.6),#L L->D D->R R->U U->L        
                  'l' :('UDLRFB',0.6),#l L->B B->R R->F F->L        

                  'Z' :('RLFBDU',0.6),#R R->D D->L L->U U->R        
                  'r' :('UDRLBF',0.6),#r R->B B->L L->F F->R        
                  'B' :('UDFBRL',0)}
    min_cost = 99999
    min_solution=None
    min_steps = None
    min_flag = ''
    cnt = 0
    cnt_test = 0

    time_begin = time.time()

    #定义路径类
    class SolvePath:
        def __init__(self):
            self.solve_before = []
            self.solve_after = []
            self.cost = 0
            self.steps = []
            self.flag = ''
    #DFS
    root = SolvePath()
    root.solve_after = Solution

    stack = []
    stack.append(root)
    while stack:
        temp = stack.pop()

        #for i in range(len(temp.solve_after)):
        while temp.solve_after:
            #print(temp.solve_after[0])
            if temp.solve_after[0][0] == 'L':
                #入栈　不做处理
                leaf_l = copy.deepcopy(temp)
                #print(leaf_l.solve_after[0])
                leaf_l.solve_after[0] = leaf_l.solve_after[0].replace('L','l')
                #print(leaf_l.solve_after[0])
                stack.append(leaf_l)
                leaf_I = copy.deepcopy(temp)
                #print(leaf_I.solve_after)
                leaf_I.solve_after[0] = leaf_I.solve_after[0].replace('L','I')
                #print(leaf_I.solve_after)
                stack.append(leaf_I)
                break#去处理栈顶
            elif temp.solve_after[0][0] == 'R':
                #入栈　不做处理
                leaf_r = copy.deepcopy(temp)
                leaf_r.solve_after[0] = leaf_r.solve_after[0].replace('R','r')
                stack.append(leaf_r)
                leaf_Z = copy.deepcopy(temp)
                leaf_Z.solve_after[0] = leaf_Z.solve_after[0].replace('R','Z')
                stack.append(leaf_Z)
                break#去处理栈顶
            elif (len(temp.solve_after)>1 and temp.solve_after[0][0] == 'F' and temp.solve_after[1][0] == 'B'):
                leaf_f = copy.deepcopy(temp)
                leaf_f.solve_after[0] = leaf_f.solve_after[0].replace('F','f')
                leaf_f.flag += 'fB '
                stack.append(leaf_f)
                leaf_B = copy.deepcopy(temp)
                leaf_B.solve_after[0:2] = [leaf_B.solve_after[1],leaf_B.solve_after[0]]
                # leaf_B.solve_after[0] = leaf_B.solve_after[0].replace('F','B')
                # leaf_B.solve_after[1] = leaf_B.solve_after[1].replace('B','F')
                leaf_B.flag += 'BF '
                stack.append(leaf_B)   
                cnt_test += 1
                break#去处理栈顶             
            elif (len(temp.solve_after)>1 and temp.solve_after[0][0] == 'U' and temp.solve_after[1][0] == 'D'):
                leaf_u = copy.deepcopy(temp)
                leaf_u.solve_after[0] = leaf_u.solve_after[0].replace('U','u')
                leaf_u.flag += 'uD '
                stack.append(leaf_u)
                leaf_D = copy.deepcopy(temp)
                leaf_D.solve_after[0:2] = [leaf_D.solve_after[1],leaf_D.solve_after[0]]
                # leaf_D.solve_after[0] = leaf_D.solve_after[0].replace('U','D')
                # leaf_D.solve_after[1] = leaf_D.solve_after[1].replace('D','U')
                leaf_D.flag += 'DU '
                stack.append(leaf_D)   
                cnt_test += 1
                break#去处理栈顶   
            else: #当前步骤既不是Ｌ也不是Ｒ，也不是FB和UD
                #处理
                temp.solve_before.append(temp.solve_after[0])
                temp.solve_after.pop(0)
                if (temp.solve_before[-1][0] == 'f'):
                    temp.solve_before[-1] = temp.solve_before[-1].replace('f', 'F')
                elif (temp.solve_before[-1][0] == 'u'):
                    temp.solve_before[-1] = temp.solve_before[-1].replace('u', 'U')
                for j in range(len(temp.solve_after)):#后续步骤（不包括当前）　每个步骤都因为执行当前步骤而发生了变化
                    for face in range(len(Standard)):
                        if (temp.solve_after[j][0] == Standard[face]):
                            temp.solve_after[j] = temp.solve_after[j].replace(Standard[face],transtable[temp.solve_before[-1][0]][0][face])
                            break
                if (temp.solve_before[-1][0] == 'I'):
                    temp.solve_before[-1] = temp.solve_before[-1].replace('I', 'L')
                elif (temp.solve_before[-1][0] == 'Z'):
                    temp.solve_before[-1] = temp.solve_before[-1].replace('Z', 'R')

                
        if temp.solve_after == []:#已经到达尾节点
            temp.steps, temp.cost = steps_trans(temp.solve_before)
            cnt += 1
            # print("路径号："+ str(cnt))
            # print("该路径为：")
            # print(temp.solve_before)
            # print("该路径用时："+str(temp.cost))
            # if(temp.flag != ''):
            #     print('temp.flag:'+temp.flag)
            if temp.cost < min_cost:
                min_cost = temp.cost
                min_solution = temp.solve_before
                min_steps = temp.steps
                min_flag = temp.flag
            if (time.time()-time_begin >0.5):
                print('搜索超时，自动退出')
                break
            # print('解算时间 = ' + str(time.time()-time_begin))

    print("非递归法DFS搜索的最优路径：")
    print(min_solution)
    print("非递归法DFS搜索的最优动作：")
    # print(min_steps)
    print("非递归法DFS搜索的时间代价：")
    print(min_cost)
    print('cnt_test:'+str(cnt_test))
    return min_steps, min_cost ,min_flag





if __name__ == '__main__':
    # solution = TransToRealSolution('F\' D')
    # print(solution)
    Solution = kociemba.solve('LLLDUDDUULRDLRUDLDBBBFFBFFBURRUDUURRULLDLDRRRFFFFBBFBB')
    solution = _KociembaTrans(Solution)
    print(solution)
    sss = []
    sss = sss+ solution
    ssssss = _SolutionTrans(sss)
    print('1'+str(solution))
    print(ssssss)
    wwww = solution
    solu  =_SolutionTransAndOptimize(wwww)
    print(solu)
            