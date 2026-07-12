#!/usr/bin/env python3
import os
import odrive
import time
from odrive.enums import *
import serial

SERIAL_PORT = os.getenv("RUBIK_SERIAL_PORT", "/dev/ttyUSB0")
SERIAL_BAUDRATE = int(os.getenv("RUBIK_SERIAL_BAUDRATE", "115200"))
ODRIVE_SERIAL_NUMBER = os.getenv("RUBIK_ODRIVE_SERIAL_NUMBER")

serial_is_connected = 0
odrive_is_connected = 0
odrv = None
ser = None
arm_calibrate_angles = [0.122, 0.1315]

def serial_connect():
    global serial_is_connected
    global ser
    try:
        ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1)
    except Exception as error:
        raise RuntimeError(
            "Unable to open Arduino serial port {} at {} baud".format(
                SERIAL_PORT, SERIAL_BAUDRATE
            )
        ) from error
    else:
        serial_is_connected = 1
        print("Serial Connected")
def send_command(command):
    if ser is None or not ser.is_open:
        raise RuntimeError("Arduino serial port is not connected")
    ser.write(command.encode())

# 90档
def arm_right_slow():
    print('右臂开始调速为slow')
    odrv.axis0.trap_traj.config.accel_limit = 60
    odrv.axis0.trap_traj.config.decel_limit = 60
    # odrv.axis1.controller.config.inertia = 0.0135
    # odrv.axis0.controller.config.pos_gain = 120
    # odrv.axis0.controller.config.vel_integrator_gain =4
    odrv.axis0.controller.config.vel_gain = 0.55
def arm_right_Medium():
    print('右臂开始调速为Medium')
    # odrv.axis0.trap_traj.config.accel_limit = 120
    # odrv.axis0.trap_traj.config.decel_limit = 120
    # # odrv.axis1.controller.config.inertia = 0.0135
    # # odrv.axis0.controller.config.pos_gain = 120
    # # odrv.axis0.controller.config.vel_integrator_gain =4
    # odrv.axis0.controller.config.vel_gain = 0.64
    odrv.axis0.trap_traj.config.accel_limit = 120
    odrv.axis0.trap_traj.config.decel_limit = 120
    # odrv.axis1.controller.config.inertia = 0.0135
    # odrv.axis0.controller.config.pos_gain = 120
    # odrv.axis0.controller.config.vel_integrator_gain =4
    odrv.axis0.controller.config.vel_gain = 0.55
def arm_right_fast():
    print('右臂开始调速为fast')
    odrv.axis0.trap_traj.config.accel_limit = 120
    odrv.axis0.trap_traj.config.decel_limit = 120
    # odrv.axis1.controller.config.inertia = 0.0135
    # odrv.axis0.controller.config.pos_gain = 120
    # odrv.axis0.controller.config.vel_integrator_gain =4
    odrv.axis0.controller.config.vel_gain = 0.55
def arm_left_slow():
    print('左臂开始调速为slow')
    odrv.axis1.trap_traj.config.accel_limit = 60
    odrv.axis1.trap_traj.config.decel_limit = 60
    # odrv.axis1.controller.config.inertia = 0.0135
    # odrv.axis1.controller.config.pos_gain = 120
    # odrv.axis1.controller.config.vel_integrator_gain =4
    odrv.axis1.controller.config.vel_gain = 0.72
def arm_left_Medium():
    print('左臂开始调速为Medium')
    # odrv.axis1.trap_traj.config.accel_limit = 120
    # odrv.axis1.trap_traj.config.decel_limit = 120
    # # odrv.axis1.controller.config.inertia = 0.0135
    # # odrv.axis1.controller.config.pos_gain = 120
    # # odrv.axis1.controller.config.vel_integrator_gain =4
    # odrv.axis1.controller.config.vel_gain = 0.52
    odrv.axis1.trap_traj.config.accel_limit = 120
    odrv.axis1.trap_traj.config.decel_limit = 120
    # odrv.axis1.controller.config.inertia = 0.0135
    # odrv.axis1.controller.config.pos_gain = 120
    # odrv.axis1.controller.config.vel_integrator_gain =4
    odrv.axis1.controller.config.vel_gain = 0.6
def arm_left_fast():
    print('左臂开始调速为fast')
    odrv.axis1.trap_traj.config.accel_limit = 120
    odrv.axis1.trap_traj.config.decel_limit = 120
    # odrv.axis1.controller.config.inertia = 0.0135
    # odrv.axis1.controller.config.pos_gain = 120
    # odrv.axis1.controller.config.vel_integrator_gain =4
    odrv.axis1.controller.config.vel_gain = 0.6
def odrive_connect():
    global odrv
    global odrive_is_connected
    try:
        print('Odrive start connecting')
        if ODRIVE_SERIAL_NUMBER:
            odrv = odrive.find_any(serial_number=ODRIVE_SERIAL_NUMBER)
        else:
            odrv = odrive.find_any()
        # arm_right_fast()
        # arm_left_fast()
        time.sleep(0.02)
        odrive_is_connected = 1
        print('Odrive is connected!') 
    except Exception as error:
        raise RuntimeError("Unable to connect to ODrive") from error
def odrive_calibrate():
    print('Robot arm start calibrating')
    odrv.axis0.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH #axis0　右侧
    while odrv.axis0.current_state != 1:
        time.sleep(0.1)
    odrv.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    time.sleep(0.5)
    arm_right_Medium()
    time.sleep(0.2)
    odrv.axis0.controller.input_pos = arm_calibrate_angles[0]
    time.sleep(1)
    odrv.axis1.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH ##axis1　左侧
    while odrv.axis1.current_state != 1:
        time.sleep(0.1)
    arm_left_Medium()
    time.sleep(0.1)
    odrv.axis1.controller.config.vel_gain-=0.04
    time.sleep(0.1)
    odrv.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    time.sleep(0.5)
    odrv.axis1.controller.input_pos = arm_calibrate_angles[1]
    print('Robot arm is calibrated!')

def odrive_out_of_closeloop():
    time.sleep(0.1)
    while odrv.axis0.current_state != 8:
        time.sleep(0.1)
    odrv.axis0.requested_state= AXIS_STATE_IDLE
    time.sleep(0.2)
    while odrv.axis1.current_state != 8:
        time.sleep(0.1)
    odrv.axis1.requested_state= AXIS_STATE_IDLE
    time.sleep(1)



def arm0_rotate90_clockwise(): #从正上方看下去是顺时针 move_incremental后input_pos也随之变化
    odrv.axis0.controller.move_incremental(0.25,True)
def arm0_rotate180_clockwise():
    odrv.axis0.controller.move_incremental(0.5,True)    
def arm0_rotate90_anticlockwise():
    odrv.axis0.controller.move_incremental(-0.25,True)  

def arm1_rotate90_clockwise():
    # odrv.axis1.controller.config.inertia = 0.023
    odrv.axis1.controller.move_incremental(0.25,True)#从正上方看下去是顺时针　move_incremental后input_pos也随之变化
def arm1_rotate180_clockwise():
    # odrv.axis1.controller.config.inertia = 0.041
    odrv.axis1.controller.move_incremental(0.5,True)
def arm1_rotate90_anticlockwise():
    # odrv.axis1.controller.config.inertia = 0.023
    odrv.axis1.controller.move_incremental(-0.25,True) 

def open_hand():
    send_command("CP\n")
def catch_hand0():
    send_command("RC\n")
def loosen_hand0():
    send_command("RO\n")
def catch_hand1():
    send_command("LC\n")
def loosen_hand1():
    send_command("LO\n")

def wait_cube_hand():
    send_command("AO\n")
def loosen_both():
    send_command("AO\n")
def loose_hand():
    send_command("OP\n")
def catch_both():
    send_command("AC\n")
    time.sleep(0.06)
# def returnToInitial():

def Robot_Init():
    serial_connect()
    odrive_connect()
    odrive_calibrate()#标定机械臂
    # wait_cube_hand()
    #
