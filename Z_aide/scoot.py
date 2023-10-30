from pymavlink import mavutil
the_connection = mavutil.mavlink_connection(device='udpin:localhost:20001', source_system=1)
#the_connection.wait_heartbeat()
# print("Heartbeat from system (system %u component %u)" %
# (the_connection.target_system, the_connection.target_component))

i = 0
while (True and i != 30):
    the_connection.mav.heartbeat_send(
            1, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
    msg = the_connection.recv_match(blocking=True)
    print(str(msg)+"\n")
    i += 1


# SCOOT MSG PING AND ACK

# while (True):

#     msg = the_connection.recv_match(blocking=True,type='COMMAND_ACK' and 'PING',timeout=11)
#     if not msg:
#             print('time out')
#             break
#     list_ignore= ['ATTITUDE_TARGET','HOME_POSITION','HEARTBEAT','ALTITUDE','ESTIMATOR_STATUS','EXTENDED_SYS_STATE','GPS_RAW_INT','OPEN_DRONE_ID_LOCATION','SCALED_PRESSURE','SYS_STATUS','OPEN_DRONE_ID_SYSTEM','UTM_GLOBAL_POSITION','VFR_HUD','POSITION_TARGET_GLOBAL_INT','POSITION_TARGET_LOCAL_NED','ATTITUDE_TARGET ','LOCAL_POSITION_NED','BATTERY_STATUS','SERVO_OUTPUT_RAW','GLOBAL_POSITION_INT','ATTITUDE','ATTITUDE_QUATERNION']
#     if msg.get_type() not in list_ignore:
#         print(str(msg)+"\n")
   
   
    # ONLY FISRT MSG AU SOL
# if msg.get_type() == 'LOCAL_POSITION_NED' or msg.get_type() == 'POSITION_TARGET_LOCAL_NED' or msg.get_type() == 'ATTITUDE_TARGET' or msg.get_type() == 'GLOBAL_POSITION_INT' or msg.get_type() == 'ATTITUDE_QUATERNION' or msg.get_type() == 'SERVO_OUTPUT_RAW' or msg.get_type() == 'ATTITUDE':
#         continue