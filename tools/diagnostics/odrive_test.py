#!/usr/bin/env python3
# AXIS_STATE_UNDEFINED             = 0,
# AXIS_STATE_IDLE                  = 1,
# AXIS_STATE_STARTUP_SEQUENCE      = 2,
# AXIS_STATE_FULL_CALIBRATION_SEQUENCE = 3,
# AXIS_STATE_MOTOR_CALIBRATION     = 4,
# AXIS_STATE_SENSORLESS_CONTROL    = 5,
# AXIS_STATE_ENCODER_INDEX_SEARCH  = 6,
# AXIS_STATE_ENCODER_OFFSET_CALIBRATION = 7,
# AXIS_STATE_CLOSED_LOOP_CONTROL   = 8,
# AXIS_STATE_LOCKIN_SPIN           = 9,
# AXIS_STATE_ENCODER_DIR_FIND      = 10,
# AXIS_STATE_HOMING                = 11,

#   Motor_Up_serial_number = 208334654230
#   Motor_Down_serial_number = 207A34634230
import odrive
import time

odrive_is_connected = 0
odrv_up = None
odrv_down = None
odrive_calibrate_angles = [0.12, -0.315]
def odrive_connect():
    global odrv_up, odrv_down
    global odrive_is_connected
    try:
        print('Odrive start connecting')
        odrv_up = odrive.find_any(serial_number="208334654230") 
        odrv_down = odrive.find_any(serial_number="207A34634230")
        print('Odrive is connected!')
        odrive_is_connected = 1 
    except Exception as error:
        print("Odrive Error")
        print(error)
odrive_connect()
def odrive_up_calibrate():
    odrv_up.axis0.requested_state = 6
    while odrv_up.axis0.current_state != 1:
        time.sleep(0.1)
    odrv_up.axis0.requested_state = 8
    time.sleep(1)
    odrv_up.axis0.controller.input_pos = 0.12
    time.sleep(1)
    odrv_up.axis1.requested_state = 6
    while odrv_up.axis1.current_state != 1:
        time.sleep(0.1)
    odrv_up.axis1.requested_state = 8
    time.sleep(1)
    odrv_up.axis1.controller.input_pos = -0.315
def odrive_down_calibrate():
    odrv_down.axis0.requested_state = 6
    while odrv_down.axis0.current_state != 1:
        time.sleep(0.1)
    odrv_down.axis0.requested_state = 8
    time.sleep(1)
    # odrive_down.axis0.controller.input_pos = 0.12
    time.sleep(1)
    odrv_down.axis1.requested_state = 6
    while odrv_down.axis1.current_state != 1:
        time.sleep(0.1)
    odrv_down.axis1.requested_state = 8
    time.sleep(1)
    # odrive_down.axis1.controller.input_pos = -0.315
# odrive_up_calibrate()