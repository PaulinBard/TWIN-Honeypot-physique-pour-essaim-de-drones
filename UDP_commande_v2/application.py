from pymavlink import mavutil
import conf
from fonction import *
import time
# Créer une connexion avec le proxy
proxy_address = f'udp:{conf.PROXY_ADDRESS}:{conf.PROXY_PORT}'
#proxy_address = f'udp:{conf.DRONE_ADDRESS}:{conf.DRONE_PORT}'
connection = mavutil.mavlink_connection(proxy_address)
connection.target_system=100
connection.target_component=100
# drone_address = f'udp:{conf.DRONE_ADDRESS}:{conf.DRONE_PORT}'
# connection= mavutil.mavlink_connection(drone_address)
print('connection')
# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" %
      (connection.target_system, connection.target_component))

print("envoyé heartbeat")
connection.mav.heartbeat_send(
    0, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
# COMMENCER COMMANDE
arm(connection)
time.sleep(4)
takeoff(connection, 10)
time.sleep(2)
land(connection)
time.sleep(2)
position(connection)
