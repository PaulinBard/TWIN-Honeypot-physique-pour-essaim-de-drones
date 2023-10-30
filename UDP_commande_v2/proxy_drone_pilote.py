from pymavlink import mavutil
import conf
import time
import fonction
import sys

source_sys = 0
connection = 0
drone_address = 0
proxy_drone_sec = 0
d_arm = False
d_disarm = False
d_pos = False
d_takeoff = True
d_land = True
# Création de la connexion


def Bind_all():
    print('bind')
    global source_sys
    global connection
    global drone_address
    global proxy_drone_sec
    source_sys = 1
    # pour parler au client
    connection = mavutil.mavlink_connection(
        device=f'udpout:{conf.PROXY_ADDRESS}:{conf.PROXY_PORT}', source_system=source_sys)
    # pour drone sdk
    drone_address = f'udp://:{conf.DRONE_PORT}'
    # pour envoyer msg to proxy2
    proxy_drone_sec = mavutil.mavlink_connection(
        device=f'udpin:{conf.PROXY2_ADDRESS}:{conf.PROXY2_PORT}')

# Connection au drone


def boucle_drone():
    i = 0
    while i < 5:
        try:
            print('try connect drone')
            fonction.connect_sdk(drone_address)
            print('le drone est connecter')
            break
        except:
            print("il n'y a pas de drone")
            i += 1


# connection au proxy_drone_sec
def boucle_proxy():
    while True:
        print("envoyé heartbeat")
        proxy_drone_sec.mav.heartbeat_send(
            source_sys, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
        print('En attente dune connexion entrante du proxy2...')
        msg = proxy_drone_sec.recv_match()
        if not msg:
            time.sleep(1)
            continue
        if msg.get_type() == 'HEARTBEAT':
            print('Connexion acceptée (heartbeat) de la part de',
                  msg.get_srcSystem())
            print("envoyé heartbeat")
            proxy_drone_sec.mav.heartbeat_send(
                source_sys, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
            break


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
        msg = connection.recv_match(blocking=True,timeout=1)

        # Vérifier si le message est valide
        if not msg:
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
                    print('pas marche arm')
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
            if (str(msg.param1)) == '0.0':
                print(
                    f'Received DISARM  message from system {msg.get_srcSystem()}')
                try:
                    # EXECUTER FONCTION VERS SIMS
                    fonction.disarm_sdk(drone_address)
                    print('cbon')
                    try:
                    # RENVOYER ACK
                   
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
                    print('pas marche disarm')
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

        elif msg.get_type() == 'COMMAND_LONG' and str(msg.command) == '22':

            print(
                f'Received TAKE_OFF message from system {msg.get_srcSystem()}')
            target_comp=msg.target_component
            target_sys=msg.target_system
            try:
                # EXECUTER FONCTION VERS SIMS
                if d_takeoff:
                    msg = fonction.takeoff(proxy_drone_sec, 10)

                else:
                    fonction.takeoff_sdk(drone_address)
                print('cbon')
                # RENVOYER ACK
                if d_takeoff:
                    print('par secure')
                    if msg.result == 0:
                        
                        try:
                            ack_msg = mavutil.mavlink.MAVLink_command_ack_message(
                        msg.command,                   
                        mavutil.mavlink.MAV_RESULT_ACCEPTED,  
                        0, 0 ,      
                        target_sys,
                        target_comp          
                        )

                    # Send the message
                            connection.mav.send(ack_msg)
                        except:
                            connection.mav.command_ack_send(
                    msg.command, mavutil.mavlink.MAV_RESULT_ACCEPTED)
                       
                    else:
                        print('pas marche takeoff1\n')
                # RENVOYER ACK
                        try:
                            ack_msg = mavutil.mavlink.MAVLink_command_ack_message(
                        msg.command,                   
                        mavutil.mavlink.MAV_RESULT_FAILED,  
                        0, 0 ,      
                        target_sys,
                        target_comp           
                        )

                    # Send the message
                            connection.mav.send(ack_msg)
                            print('long\n')
                        except:
                            connection.mav.command_ack_send(
                            msg.command, mavutil.mavlink.MAV_RESULT_FAILED)
                            print('cour\n')
                else:
                    try:
                        ack_msg = mavutil.mavlink.MAVLink_command_ack_message(
                        msg.command,                   
                        mavutil.mavlink.MAV_RESULT_ACCEPTED,  
                        0, 0 ,      
                        target_sys,
                        target_comp          
                        )

                    # Send the message
                        connection.mav.send(ack_msg)
                    except:
                        connection.mav.command_ack_send(
                    msg.command, mavutil.mavlink.MAV_RESULT_ACCEPTED)
            except:
                print('pas marche takeoff2')
                # RENVOYER ACK
                try:
                    ack_msg = mavutil.mavlink.MAVLink_command_ack_message(
                        msg.command,                   
                        mavutil.mavlink.MAV_RESULT_FAILED,  
                        0, 0 ,      
                        target_sys,
                        target_comp          
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
                print('pas marche land')
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
        else:
            print(
                f'Received {msg} et {str(msg.param1)} message from system {msg.get_srcSystem()}')

        # Autres traitements de messages d'une demande de connexion


try:
    Bind_all()
    boucle_drone()
    boucle_proxy()
    boucle_att()
    boucle_sdk()

except IndexError:
    print('perreur')
