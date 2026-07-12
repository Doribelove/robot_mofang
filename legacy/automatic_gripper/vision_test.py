#!/usr/bin/env python3
import sys
from tokenize import tabsize
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import vision_
import kociemba


if __name__ == '__main__':
    input()
    vision_.turn_false()
    input()
    Solution = kociemba.solve(vision_.cubestate)
    print(Solution)

