from pymavlink import mavutil
import conf
import time
import fonction
import sys

# from pymavlink.dialects.v10.ardupilotmega import *
source_sys = 1
# Création de la connexion avec le numéro de système source = 1
connection = mavutil.mavlink_connection(
    device=f'udpout:{conf.PROXY_ADDRESS}:{conf.PROXY_PORT}', source_system=source_sys)
drone_address = 0
drone = 0


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
            client_sys = msg.get_srcSystem()
            client_comp = msg.get_srcComponent()
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
                connection.mav.command_ack_send(
                    32, mavutil.mavlink.MAV_RESULT_ACCEPTED)

            except:
                print('pas marche pos')
                # RENVOYER ACK
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
                connection.mav.command_ack_send(
                    msg.command, mavutil.mavlink.MAV_RESULT_ACCEPTED)
            except:
                print('pas marche takeoff')
                # RENVOYER ACK
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

# NON FOCNTIONNEL


def boucle_link():
    print('boucle principale')
    # Boucle principale
    while True:
        # Attendre de recevoir un message
        msg = connection.recv_match()

        # Vérifier si le message est valide
        if not msg:
            continue
        # print(msg)
        # Traitement des messages reçus
        if msg.get_type() == 'HEARTBEAT':
            print(
                f'Received HEARTBEAT message from system {msg.get_srcSystem()}')
            # EXECUTER FONCTION VERS SIMS
            # RENVOYER ACK

        elif msg.get_type() == 'PING':
            print(f'Received PING message from system {msg.get_srcSystem()}')
            # EXECUTER FONCTION VERS SIMS
            # RENVOYER ACK

        elif msg.get_type() == 'GLOBAL_POSITION_INT':
            print(
                f'Received GLOBAL_POSITION_INT message from system {msg.get_srcSystem()}')
            # EXECUTER FONCTION VERS SIMS
            # RENVOYER ACK

        elif msg.get_type() == 'COMMAND_LONG' and str(msg.command) == '400' and (str(msg.param1)) == '1.0':

            print(
                f'Received ARM  message from system {msg.get_srcSystem()}')
            # EXECUTER FONCTION VERS SIMS
            # fonction.arm(drone) #probleme port ??
            # RENVOYER ACK
            print('ack')
            connection.mav.command_ack_send(
                msg.command, mavutil.mavlink.MAV_RESULT_ACCEPTED)
        elif msg.get_type() == 'COMMAND_LONG' and str(msg.command) == '400' and (str(msg.param1)) == '0.0':
            print(
                f'Received DISARM  message from system {msg.get_srcSystem()}')
            # EXECUTER FONCTION VERS SIMS
            # RENVOYER ACK

        elif msg.get_type() == 'COMMAND_LONG' and str(msg.command) == '22':

            print(
                f'Received TAKE_OFF message from system {msg.get_srcSystem()}')
            # EXECUTER FONCTION VERS SIMS
            # fonction.takeoff(drone)
            # RENVOYER ACK
            connection.mav.command_ack_send(
                msg.command, mavutil.mavlink.MAV_RESULT_ACCEPTED)

        else:
            print(
                f'Received {msg} et {str(msg.param1)} message from system {msg.get_srcSystem()}')

        # Autres traitements de messages d'une demande de connexion


try:

    if sys.argv[1] == 'sdk':
        drone_address = f'udp://:{conf.DRONE_PORT}'  # MAVSDK
        drone2_address = f'udp://:{conf.DRONE_PORT2}'  # MAVSDK
        print("sdk")
        boucle_att()
        boucle_sdk()
    if sys.argv[1] == 'link':
        print("link")

        drone = mavutil.mavlink_connection(
            'udpin:localhost:14550')  # POURMAVLINK
        boucle_att()
        boucle_link()
    if sys.argv[1] == 'fast':
        drone_address = 'udp://:14540'  # MAVSDK
        drone = mavutil.mavlink_connection(
            'udpin:localhost:14550')  # POURMAVLINK
        print("fast")
        boucle_sdk()
except IndexError:
    print('pas d''argument')
    drone_address = 'udp://:14540'  # MAVSDK
    drone = mavutil.mavlink_connection('udpin:localhost:14550')  # POURMAVLINK

    boucle_att()
    boucle_sdk()
