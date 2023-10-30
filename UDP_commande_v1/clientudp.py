#!/usr/bin/env python3
import socket
from enum import Enum
"""
basic client/server udp pour créer server un intermédiaire
 entre le drone et l'uttilisateur

Pour aller plus loins:
    -A executer depuis l'application mobile
    -uttiliser mavlink protocole des l'application et rendre le server passerelle 
    compatible avec n'importe qu'elle outils uttlissant mavlink
"""
class Command(Enum):
    connect = 1
    arm = 2
    disarm = 3
    takeoff = 4
    land = 5
    position = 6

print("Voici les commandes :\n [1]:connect \n [2]:arm\n [3]:disarm\n [4]:takeoff \n [5]:land\n [6]:position\n")
print("Exemple pour executer [1]: 1 ")
commanduser =int(input("Choisir la commande: "))
print("Vous avez choisi "+ Command(commanduser).name)

msgFromClient       = Command(commanduser).name

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("127.0.0.1", 20001)

bufferSize          = 1024

 

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 

# Send to server using created UDP socket

UDPClientSocket.sendto(bytesToSend, serverAddressPort)

 

msgFromServer = UDPClientSocket.recvfrom(bufferSize)

 

msg = "Message from Server :{}".format(msgFromServer[0].decode())

print(msg)