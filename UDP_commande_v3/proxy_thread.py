from pymavlink import mavutil
import conf
import time
import fonction
import sys
import threading
import asyncio
from mavsdk import System

# source discution avec client
proxy_ip = conf.PROXY_ADDRESS
proxy_port = conf.PROXY_PORT
proxy_sys = 155
proxy_comp = 155

connection = mavutil.mavlink_connection(
        device=f'udpout:{conf.PROXY_ADDRESS}:{conf.PROXY_PORT}', source_system=proxy_sys)# out difuser sur 
# discution avec les sims
drone_ip=conf.DRONE_ADDRESS
drone_port=conf.DRONE_PORT
drone_address = f'udp://:{conf.DRONE_PORT}'
drone = mavutil.mavlink_connection(device='udpin:localhost:14540', source_system=1)# in ecouter sur


proxy_drone_sec = mavutil.mavlink_connection(
    device=f'udpin:{conf.PROXY2_ADDRESS}:{conf.PROXY2_PORT}')

# VARIABLES
d_arm = False
d_disarm = False
d_pos = False
d_takeoff = True
d_land = True



# Connection au drone


def boucle_drone():
    i = 0
    while i < 3:
        try:
            print('try connect drone')
            fonction.connect_sdk(drone_address)
            print('le drone est connecter')
            break
        except:
            print("il n'y a pas de drone")
            i += 1

def boucle_proxy():
    while True:
        proxy_drone_sec.mav.heartbeat_send(
            proxy_sys, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
        msg = proxy_drone_sec.recv_match(blocking=True, timeout=1)
        if not msg:
            continue
        if msg.get_type() == 'HEARTBEAT':
            print('Connexion acceptée (heartbeat) de la part de',
                  msg.get_srcSystem())
            break

#RENVOIE TOUS LES MSG DE LA SIM SUR LE PORT PROXY
def sim_to_client(drone_ip, drone_port, drone2_ip, drone2_port, client_ip, client_port):
    while(True):
            msg = drone.recv_match(blocking=True,timeout=1)
            if not msg:
                continue
            try:
                connection.mav.send(msg)
            except:
                connection.mav.heartbeat_send(
            proxy_sys, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
                continue
    return 0

#RENVOIE COMMANDE DE CLIENT VERS DRONE
def client_to_sim(drone_ip, drone_port, drone2_ip, drone2_port, client_ip, client_port):
    while True:
        msg = connection.recv_match(blocking=True,timeout=1)
        if not msg:
                continue
        
        #FAIRE DU TRAITEMENT


        try:
            drone.mav.send(msg)
        except:
            drone.mav.heartbeat_send(
            proxy_sys, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
            continue


    return 0

#thread
t1 = threading.Thread(target=client_to_sim, args=(1, 1, 1, 1, 1, 1))
t2 = threading.Thread(target=sim_to_client, args=(1, 1, 1, 1, 1, 1))





boucle_drone()#il faut avoir lancer le drone
boucle_proxy()# il faut lancer le server proxy sec de UDP2


t1.start()
t2.start()


t1.join()
t2.join()
