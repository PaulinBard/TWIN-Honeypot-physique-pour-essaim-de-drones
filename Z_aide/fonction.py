from pymavlink import mavutil
#from pymavlink.dialects.v20 import mavutil
import math


def rep(connection, mavtype):
    msg = connection.recv_match(type=mavtype, blocking=True)
    print('message : '+str(msg))


def arm(connection):
    print('arm...')
    connection.mav.command_long_send(connection.target_system,
                                     connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                                     0, 1, 0, 0, 0, 0, 0, 0)
    rep(connection, 'COMMAND_ACK')


def disarm(connection):
    print('disarm...')
    connection.mav.command_long_send(connection.target_system,
                                     connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                                     0, 0, 0, 0, 0, 0, 0, 0)
    rep(connection, 'COMMAND_ACK')


def takeoff(connection, hauteur):
    print('takeoff')
    connection.mav.command_long_send(connection.target_system,
                                     connection.target_component,
                                     mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                                     #0, 0, 0, 0, 0, 473977431, 85455947, 488180+hauteur)
                                     0, 0, 0, 0, 0, 0, 0, hauteur)
    rep(connection, 'COMMAND_ACK')


def mode(connection, mode):
    connection.mav.set_mode_send(connection.target_system,
                                 mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                                 connection.mode_mapping()[mode])

    rep(connection, 'COMMAND_ACK')

def position(connection):
    #A FAIREE
    rep(connection, 'COMMAND_ACK')

def land(connection):
    #A fAIRE
    rep(connection, 'COMMAND_ACK')