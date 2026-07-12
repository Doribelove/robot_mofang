#!/usr/bin/env python3
import odrive
import time
from odrive.enums import *
import serial
import time

serial_is_connected = 0
odrive_is_connected = 0
odrv = None
ser = None
arm_calibrate_angles = [-0.329, -0.283]

def serial_connect():
    global serial_is_connected
    global ser
    try:
        ser = serial.Serial("COM6")
    except Exception as error:
        print("Serial Error")
        print(error)
    else:
        serial_is_connected = 1
        print("Serial Connected")
def send_command(command):
    ser.write(command.encode())
def arm_right_slow():
    print('右臂开始调速为slow')
    # print('accel_limit = 30')
    # time.sleep(0.1)
    odrv.axis0.trap_traj.config.accel_limit = 90
    # print('decel_limit = 30')
    # time.sleep(0.1)
    odrv.axis0.trap_traj.config.decel_limit = 90
    # print('inertia = 0.008')
    # time.sleep(0.1)
    odrv.axis0.controller.config.inertia = 0.0055
    # print('pos_gain = 70')
    # time.sleep(0.1)
    odrv.axis0.controller.config.pos_gain = 70
    # print('vel_integrator_gain =0.01')
    # time.sleep(0.1)
    odrv.axis0.controller.config.vel_integrator_gain =4
    # print('vel_gain = 1.5')
    # time.sleep(0.1)
    odrv.axis0.controller.config.vel_gain = 0.9
def arm_right_Medium():
    print('右臂开始调速为Medium')
    # print('accel_limit = 60')
    # time.sleep(0.1)
    odrv.axis0.trap_traj.config.accel_limit = 120
    # print('decel_limit = 60')
    # time.sleep(0.1)
    odrv.axis0.trap_traj.config.decel_limit = 120
    # print('inertia = 0.009')
    # time.sleep(0.1)
    odrv.axis0.controller.config.inertia = 0.0065
    # print('pos_gain = 70')
    # time.sleep(0.1)
    odrv.axis0.controller.config.pos_gain = 90
    # print('vel_integrator_gain =0.01')
    # time.sleep(0.1)
    odrv.axis0.controller.config.vel_integrator_gain =4
    # print('vel_gain = 1.5')
    # time.sleep(0.1)
    odrv.axis0.controller.config.vel_gain = 0.9
    # print('速度60完成')
def arm_right_fast():
    print('右臂开始调速为fast')
    odrv.axis0.trap_traj.config.accel_limit = 120
    odrv.axis0.trap_traj.config.decel_limit = 120
    odrv.axis0.controller.config.inertia = 0.012
    odrv.axis0.controller.config.pos_gain = 90
    odrv.axis0.controller.config.vel_integrator_gain =4
    odrv.axis0.controller.config.vel_gain = 0.9
def arm_left_slow():
    print('左臂开始调速为slow')
    # print('accel_limit = 30')
    # time.sleep(0.1)
    odrv.axis1.trap_traj.config.accel_limit = 90
    # print('decel_limit = 30')
    # time.sleep(0.1)
    odrv.axis1.trap_traj.config.decel_limit = 90
    # print('inertia = 0.007')
    # time.sleep(0.1)
    odrv.axis1.controller.config.inertia = 0.006
    # print('config.pos_gain = 70')
    # time.sleep(0.1)
    odrv.axis1.controller.config.pos_gain = 70
    # print('vel_integrator_gain =0.01')
    # time.sleep(0.1)
    odrv.axis1.controller.config.vel_integrator_gain =4
    # print('vel_gain = 1.5')
    # time.sleep(0.1)
    odrv.axis1.controller.config.vel_gain = 0.9
    # print('速度30完成')
def arm_left_Medium():
    print('左臂开始调速为Medium')
    # print('accel_limit = 60')
    # time.sleep(0.1)
    odrv.axis1.trap_traj.config.accel_limit = 120
    # print('decel_limit = 60')
    # time.sleep(0.1)
    odrv.axis1.trap_traj.config.decel_limit = 120
    # print('inertia = 0.01')
    # time.sleep(0.1)
    odrv.axis1.controller.config.inertia = 0.006
    # print('config.pos_gain = 70')
    # time.sleep(0.1)
    odrv.axis1.controller.config.pos_gain = 90
    # print('vel_integrator_gain =0.01')
    # time.sleep(0.1)
    odrv.axis1.controller.config.vel_integrator_gain =4
    # print('vel_gain = 1.5')
    # time.sleep(0.1)
    odrv.axis1.controller.config.vel_gain = 0.9
    # print('速度60完成')
def arm_left_fast():
    print('左臂开始调速为fast')
    odrv.axis1.trap_traj.config.accel_limit = 120
    odrv.axis1.trap_traj.config.decel_limit = 120
    odrv.axis1.controller.config.inertia = 0.0135
    odrv.axis1.controller.config.pos_gain = 30
    odrv.axis1.controller.config.vel_integrator_gain =0.5
    odrv.axis1.controller.config.vel_gain = 0.6
def odrive_connect():
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
def odrive_calibrate():
    print('Robot arm start calibrating')
    odrv.axis0.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH #axis0　右侧
    while odrv.axis0.current_state != 1:
        time.sleep(0.1)
    odrv.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    time.sleep(1)
    odrv.axis0.controller.input_pos = arm_calibrate_angles[0]
    time.sleep(1)
    odrv.axis1.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH ##axis1　左侧
    while odrv.axis1.current_state != 1:
        time.sleep(0.1)
    odrv.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    time.sleep(1)
    odrv.axis1.controller.input_pos = arm_calibrate_angles[1]
    print('Robot arm is calibrated!')



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
def catch_both():
    send_command("AC\n")
    time.sleep(0.06)
# def returnToInitial():

def Robot_Init():
    # odrive_connect()
    odrive_calibrate()#标定机械臂
    # wait_cube_hand()

odrive_connect()
serial_connect()

