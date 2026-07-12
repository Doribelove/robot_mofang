import hardware
import time
import Function
import moving
import vision_
import cv2 
import kociemba
import KociembaTrans
time.sleep(1)

time.sleep(1)

input("按键抓住")
Solution = kociemba.solve('RDLRUFLRDRUDLRLLBLUFBLFFUBURRBFDUUDBDUFBLBRDFFLFUBDDRB')
realsolution = KociembaTrans.TransToRealSolution(Solution)
hardware.Solution_Move(realsolution)