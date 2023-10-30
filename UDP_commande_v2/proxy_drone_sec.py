from pymavlink import mavutil
import conf
import time
import fonction
import sys

# from pymavlink.dialects.v10.ardupilotmega import *
source_sys = 2
# Création de la connexion avec le numéro de système source = 2
connection = mavutil.mavlink_connection(
    device=f'udpout:{conf.PROXY2_ADDRESS}:{conf.PROXY2_PORT}', source_system=source_sys)
drone_address =  drone_address = f'udp://:{conf.DRONE_PORT2}'  # MAVSDK


# Attente d'une demande de connexion
def boucle_att():
    while True:
        print("envoyé heartbeat")
        connection.mav.heartbeat_send(
            source_sys, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
        print('En attente dune connexion entrante...')
        msg = connection.recv_match()
        if not msg:
            time.sleep(1)
            continue
        if msg.get_type() == 'HEARTBEAT':
            print('Connexion acceptée (heartbeat) de la part de',
                  msg.get_srcSystem())
            break


def boucle_sdk():
    print('boucle principale')
    # Boucle principale
    while True:
        connection.mav.heartbeat_send(
            source_sys, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
        # pos = fonction.position_sdk(drone_address)

        # Attendre de recevoir un message
        msg = connection.recv_match()

        # Vérifier si le message est valide
        if not msg:
            time.sleep(1)
            continue
        # print(msg)
        # Traitement des messages reçus
        if msg.get_type() == 'HEARTBEAT':
            print(
                f'Received HEARTBEAT message from system {msg.get_srcSystem()}')
            # RENVOYER HEARTBEAT
            connection.mav.heartbeat_send(
                source_sys, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)

        elif msg.get_type() == 'PING':
            print(f'Received PING message from system {msg.get_srcSystem()}')
            # RENVOYER PING
            # A FAIRE
        elif msg.get_type() == 'LOCAL_POSITION_NED':  # detrounement de focntion
            print(
                f'Received POSITION message from system {msg.get_srcSystem()}')
            try:
                # EXECUTER FONCTION VERS SIMS
                pos = fonction.position_sdk(drone_address)
                pos2 = " "
                for char in pos:
                    if char != "[" and char != "]":
                        pos2 += char

                lst = pos2.split(",")

                # RENVOYER POSITION
                x = float(lst[0])
                y = float(lst[1])
                z = float(lst[2])

                connection.mav.local_position_ned_send(0, x, y, z, 0, 0, 0)

                # RENVOYER ACK
                try:
                    ack_msg = mavutil.mavlink.MAVLink_command_ack_message(
                        32,                   
                        mavutil.mavlink.MAV_RESULT_ACCEPTED,  
                        0, 0 ,      
                        msg.target_system,             
                        msg.target_component          
                        )

                    # Send the message
                    connection.mav.send(ack_msg)
                except:
                    connection.mav.command_ack_send(
                    32, mavutil.mavlink.MAV_RESULT_ACCEPTED)

            except:
                print('pas marche pos')
                # RENVOYER ACK
                try:
                    ack_msg = mavutil.mavlink.MAVLink_command_ack_message(
                        32,                   
                        mavutil.mavlink.MAV_RESULT_FAILED,  
                        0, 0 ,      
                        msg.target_system,             
                        msg.target_component          
                        )

                    # Send the message
                    connection.mav.send(ack_msg)
                except:
                    connection.mav.command_ack_send(
                    32, mavutil.mavlink.MAV_RESULT_FAILED)
        elif msg.get_type() == 'COMMAND_LONG' and str(msg.command) == '400':
            if (str(msg.param1)) == '1.0':
                print(
                    f'Received ARM  message from system {msg.get_srcSystem()}')

                try:
                    # EXECUTER FONCTION VERS SIMS
                    fonction.arm_sdk(drone_address)
                    print('cbon')
                    # RENVOYER ACK
                    connection.mav.command_ack_send(
                        msg.command, mavutil.mavlink.MAV_RESULT_ACCEPTED)
                except:
                    print('pas marche arm')
                    # RENVOYER ACK
                    connection.mav.command_ack_send(
                        msg.command, mavutil.mavlink.MAV_RESULT_FAILED)
            if (str(msg.param1)) == '0.0':
                print(
                    f'Received DISARM  message from system {msg.get_srcSystem()}')
                try:
                    # EXECUTER FONCTION VERS SIMS
                    fonction.disarm_sdk(drone_address)
                    print('cbon')
                    # RENVOYER ACK
                    connection.mav.command_ack_send(
                        msg.command, mavutil.mavlink.MAV_RESULT_ACCEPTED)
                except:
                    print('pas marche disarm')
                    # RENVOYER ACK
                    connection.mav.command_ack_send(
                        msg.command, mavutil.mavlink.MAV_RESULT_FAILED)
        elif msg.get_type() == 'COMMAND_LONG' and str(msg.command) == '22':

            print(
                f'Received TAKE_OFF message from system {msg.get_srcSystem()}')
            try:
                # EXECUTER FONCTION VERS SIMS
                fonction.takeoff_sdk(drone_address)
                print('cbon')
                # RENVOYER ACK
                
                try:
                    ack_msg = mavutil.mavlink.MAVLink_command_ack_message(
                        msg.command,                   
                        mavutil.mavlink.MAV_RESULT_ACCEPTED,  
                        0, 0 ,      
                        msg.target_system,             
                        msg.target_component          
                        )

                    # Send the message
                    connection.mav.send(ack_msg)
                except:
                    connection.mav.command_ack_send(
                    msg.command, mavutil.mavlink.MAV_RESULT_ACCEPTED)
            except:
                print('pas marche takeoff')
                # RENVOYER ACK
                try:
                    ack_msg = mavutil.mavlink.MAVLink_command_ack_message(
                        msg.command,                   
                        mavutil.mavlink.MAV_RESULT_FAILED,  
                        0, 0 ,      
                        msg.target_system,             
                        msg.target_component          
                        )

                    # Send the message
                    connection.mav.send(ack_msg)
                except:
                    connection.mav.command_ack_send(
                    msg.command, mavutil.mavlink.MAV_RESULT_FAILED)
        elif msg.get_type() == 'COMMAND_LONG' and str(msg.command) == '21':

            print(
                f'Received LAND message from system {msg.get_srcSystem()}')
            try:
                # EXECUTER FONCTION VERS SIMS
                fonction.land_sdk(drone_address)
                print('cbon')
                # RENVOYER ACK
                connection.mav.command_ack_send(
                    msg.command, mavutil.mavlink.MAV_RESULT_ACCEPTED)
            except:
                print('pas marche land')
                # RENVOYER ACK
                connection.mav.command_ack_send(
                    msg.command, mavutil.mavlink.MAV_RESULT_FAILED)
        else:
            print(
                f'Received {msg} et {str(msg.param1)} message from system {msg.get_srcSystem()}')

        # Autres traitements de messages d'une demande de connexion


try:
    boucle_att()
    boucle_sdk()
except IndexError:
    print('pas d''argument')
