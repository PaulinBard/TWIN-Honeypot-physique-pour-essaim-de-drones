from pymavlink import mavutil

import fonction
import time
connection = mavutil.mavlink_connection('udpin:localhost:14550')  # la sim
# the_connection = mavutil.mavlink_connection('udpin:localhost:20001')#le proxy
connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" %
      (connection.target_system, connection.target_component))
# connection.mav.command_long_send(connection.target_system,
#                                      connection.target_component,
#                                      55,
#                                      0, 1, 6, 0, 0, 0, 0, 0)
# fonction.rep(connection, 'COMMAND_ACK')
connection.mav.command_long_send(connection.target_system,
                                     connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                                     0, 1, 21196, 0, 0, 0, 0, 0)
fonction.rep(connection, 'COMMAND_ACK')

time.sleep(2)

connection.mav.command_long_send(connection.target_system,
                                     connection.target_component,
                                     mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                                     0, 0, 0, 0, 0, 0, 0, 10)
fonction.rep(connection, 'COMMAND_ACK')

# PROBLEME AU TAKEOFF sur px4 car pymavlink tenu par ardupilot 
# mouvement incorect
# soit mode interdit takeoff
# soit paremtere mauvais ou d'autre parametre doivent etre setup avant
# fichier de setup des var global a trouver ?

# lancer sur ardupilot  working 
# telecharger:
# https://ardupilot.org/dev/docs/building-setup-linux.html

# lancer:
# cd ardupilot/ArduCopter
# ./Tools/autotest/sim_vehicle.py --map --console
#mode guided

#  avec gazebo
# tekecharger:
# https://ardupilot.org/dev/docs/sitl-with-gazebo.html

# lancer :
# cd ardupilot/ArduCopter
#premier terminal
# gz sim -v4 -r iris_runway.sdf
# 
# second terminal
# ../Tools/autotest/sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON --map --console
#mode guided
