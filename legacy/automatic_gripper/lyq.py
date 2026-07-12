#!/usr/bin/env python3
import serial
import odrive


global odrv
global odrive_is_connected
try:
    print('Odrive start connecting')
    odrv = odrive.find_any()
    # arm_right_fast()
    # arm_left_fast()
    time.sleep(0.02)
    print('Odrive is connected!')
except Exception as error:
    print("Odrive Connection Error")
    print(error)