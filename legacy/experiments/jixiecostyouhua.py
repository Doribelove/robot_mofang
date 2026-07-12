import time
import twophase.solver as sv
import jixiecost
import jixiecost2

# 假设这个函数包含了 `jixiecost.py` 中的主函数逻辑
def calculate_timejixie():
    cubestring = 'RDLRUFLRDRUDLRLLBLUFBLFFUBURRBFDUUDBDUFBLBRDFFLFUBDDRB'
    Solution = sv.solve(cubestring, 0, 0.08)
    Solution = jixiecost._KociembaTrans(Solution)
    
    # 提取优化后的解法和步骤
    realsolution, costbushu = jixiecost._SolutionTransAndOptimize(Solution)
    s = jixiecost.jixie1(realsolution)
    y = jixiecost.youhua1(s)
    z = jixiecost.jixie2(y)
    
    # 计算 timejixie
    timejixie = 0
    for step in z:
        timejixie += jixiecost.time_act(step)
    
    return timejixie


# 这个函数循环执行100次，累加每次的timejixie值
def total_timejixie_over_10_runs():
    total_timejixie1 = 0
    for i in range(10):
        total_timejixie1 += calculate_timejixie()
    
    print(f"Total timejixie over 10 runs: {total_timejixie1/10}")
    return total_timejixie1/10

# 执行函数
# total_timejixie_over_100_runs()
