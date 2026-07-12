#!/usr/bin/env python3
import time

import Function
import hardware
import vision_


def main():
    hardware.Robot_Init()
    time.sleep(0.1)
    input("初始化完成。放入魔方并合拢双爪，确认安全后按 Enter：")

    vision_.turn_false()
    Function.SolvingCube()

    time.sleep(0.01)
    hardware.loosen_both()
    time.sleep(0.01)
    hardware.loose_hand()
    time.sleep(0.08)
    hardware.odrive_out_of_closeloop()

    # Wait for the pneumatic system to release pressure.
    time.sleep(5)
    hardware.catch_both()
    time.sleep(0.1)
    hardware.open_hand()
    input("复原完成，确认安全后按 Enter 释放夹爪：")
    time.sleep(0.1)
    hardware.loose_hand()
    time.sleep(0.1)
    input("流程结束，按 Enter 退出：")


if __name__ == "__main__":
    main()
