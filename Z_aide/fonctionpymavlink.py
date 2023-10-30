from pymavlink import mavutil
import time

# Connexion au drone
master = mavutil.mavlink_connection('udp:127.0.0.1:14550')
master.wait_heartbeat()
# disable auto disarm
# set the mode to GUIDED
#mode = mavutil.mavlink.MAV_MODE_OFFBOARD # replace with your desired mode
# custom_mode = 0
# custom_sub_mode = 0
# cmd = master.mav.command_long_send(
#     0, 0,  # target system, target component
#     mavutil.mavlink.MAV_CMD_DO_SET_MODE,  # command
#     0,  # confirmation
#     220,  # mode
#     custom_mode,  # custom mode
#     custom_sub_mode,  # custom sub mode
#     0, 0, 0,0)  # parameters 4-6 (unused)

# # wait for the command to be acknowledged
# ack_msg = None
# while ack_msg is None:
#     ack_msg = master.recv_match(type='COMMAND_ACK', blocking=True)
#     time.sleep(0.1)
# Boucle principale
while True:
    # Attendre de recevoir un message
    msg = master.recv_match()

    # Vérifier si le message est valide
    if not msg:
        continue

    # Traitement des messages reçus
    if msg.get_type() == 'HEARTBEAT':
        print(msg)
        # Si le message est un heartbeat, envoyer une commande au drone
        # par exemple, commander le drone de décoller
        
# Vérification des préconditions d'armement
        master.mav.command_long_send(
            master.target_system,  # Système cible (0 pour le système par défaut)
            master.target_component,  # Composant cible (0 pour le composant par défaut)
            mavutil.mavlink.MAV_CMD_RUN_PREARM_CHECKS,  # Code de commande pour exécuter les vérifications pré-armement
            0,  # Confirmation automatique de la commande
            1,  # Exécuter les vérifications pré-armement
            0,  # Non utilisé pour les vérifications pré-armement
            0,  # Non utilisé pour les vérifications pré-armement
            0,  # Non utilisé pour les vérifications pré-armement
            0,  # Non utilisé pour les vérifications pré-armement
            0,  # Non utilisé pour les vérifications pré-armement
            0)  # Non utilisé pour les vérifications pré-armement

        # Attente de la réponse
        while True:
            msg = master.recv_match(type='COMMAND_ACK', blocking=True)
            if not msg:
                continue
            if msg.command == mavutil.mavlink.MAV_CMD_RUN_PREARM_CHECKS:
                if msg.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
                    print('Le drone est prêt à être armé.')
                    break
                else:
                    print('Les vérifications pré-armement ont échoué.')
                    

        # Envoi de la commande d'armement
        print('try armé.')
        master.mav.command_long_send(
        master.target_system,  # Système cible (0 pour le système par défaut)
        master.target_component,  # Composant cible (0 pour le composant par défaut)
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,  # Code de commande d'armement
        0,  # Confirmation automatique de la commande
        1,  # Armer le drone (0 pour désarmer)
        21196,  # Non utilisé pour l'armement
        0,  # Non utilisé pour l'armement
        0,  # Non utilisé pour l'armement
        0,  # Non utilisé pour l'armement
        0,  # Non utilisé pour l'armement
        0)  # Non utilisé pour l'armement
        master.motors_armed_wait()
        print('Armed!')
        # Commande de décollage
        print('takeoof')
        master.mav.command_long_send(
            master.target_system,   # Système cible (0 pour le système par défaut)
            master.target_component, # Composant cible (0 pour le composant par défaut)
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, # Code de commande de décollage
            1,    # Confirmation automatique de la commande
            0,    # Paramètre 1 : Hauteur du décollage en mètres
            0,    # Paramètre 2 : Latitude cible en degrés
            0,    # Paramètre 3 : Longitude cible en degrés
            5,    # Paramètre 4 : Altitude cible en mètres
            0,    # Paramètre 5 : Paramètre vide
            0,    # Paramètre 6 : Paramètre vide
            0)    # Paramètre 7 : Paramètre vide
        time.sleep(1.0)
    # Attendre un peu avant de vérifier le prochain message
    #time.sleep(0.1)


# from pymavlink import mavutil

# # Création de la connexion avec le numéro de système source = 1
# connection = mavutil.mavlink_connection(device='udp:0.0.0.0:20001', source_system=1)

# # Attente d'une demande de connexion
# print('En attente dune connexion entrante...')
# msg = connection.recv_match(type='HEARTBEAT', blocking=True)

# # Accepter la connexion
# print('Connexion acceptée de la part de', msg.get_srcSystem())
# #connection.accept()

# # Boucle principale
# while True:
#     # Attendre de recevoir un message
#     msg = connection.recv_match()

#     # Vérifier si le message est valide
#     if not msg:
#         continue
#     print(msg.get_type())
#     print(msg)
#     # Traitement des messages reçus
#     if msg.get_type() == 'GPS_RAW_INT':
#         # Si le message est un GPS_RAW_INT, afficher les données GPS
#         print('Latitude:', msg.lat)
#         print('Longitude:', msg.lon)
#         print('Altitude:', msg.alt)
#     if msg.get_type() == 'HEARTBEAT':
#         continue
#     if msg and msg.get_type() == 'PING':
#         # if a PING message is received, respond with a PING message of our own
#         print(f'Received PING message from system {msg.get_srcSystem()}')
        
#         ack_msg = connection.mav.heartbeat_encode(mavutil.mavlink.MAV_TYPE_QUADROTOR, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
#         connection.mav.send(ack_msg)
#         print("Sent ACK message in response to PING")
        
#         # print('Sent PING response')
#         # current_time = int(time.time() * 1000)

#         # # send a SYSTEM_TIME command with the current time
#         # connection.mav.command_long_send(
#         #     msg.get_srcSystem(),  # target_system
#         #     msg.get_srcComponent(),  # target_component
#         #     mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,  # command
#         #     0,  # confirmation
#         #     mavutil.mavlink.MAVLINK_MSG_ID_SYSTEM_TIME,  # param1
#         #     1000000,  # param2 (1 Hz interval)
#         #     current_time,  # param3 (current system time in milliseconds)
#         #     0,  # param4
#         #     0,  # param5
#         #     0,  # param6
#         #     0  # param7
#         # )
        
#     # Autres traitements de messages...e d'une demande de connexion



# # Envoyer une commande pour demander la position
# connection.mav.command_long_send(
#     0,                # temps en millisecondes depuis le démarrage
#     1,                # ID du système (0 pour le système actuel)
#     1,                # ID du composant (0 pour le système actuel)
#     mavutil.mavlink.MAV_CMD_GLOBAL_POSITION_INT,  # code de commande
#     0, 0, 0, 0, 0, 0, 0  # paramètres vides pour cette commande
# )

# # Attendre la réponse avec le message HOME_POSITION
# msg = connection.recv_match(type='GLOBAL_POSITION_INT')

# # Récupérer la latitude, la longitude et l'altitude relative du drone
# print(msg)

# faux
# connection.mav.acknowledge(msg.target_system,msg.target_component,msg.command,mavutil.mavlink.MAV_RESULT_ACCEPTED)