#!/usr/bin/env python3
import socket
from allCommand import *

"""
basic client/server udp pour créer server un intermédiaire
 entre le drone et l'uttilisateur

Pour aller plus loins:
    -A executer depuis l'application mobile
    -uttiliser mavlink protocole des l'application et rendre le server passerelle 
    compatible avec n'importe qu'elle outils uttlissant mavlink
"""
def serverudp():


    localIP = "127.0.0.1"

    localPort = 20001

    bufferSize = 1024

    # Create a datagram socket

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


    # Bind to address and ip

    UDPServerSocket.bind((localIP, localPort))


    print("UDP server up and listening")


    # Listen for incoming datagrams

    while(True):

        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

        message = bytesAddressPair[0]

        address = bytesAddressPair[1]

        clientMsg = "Message from Client:{}".format(message)
        clientIP = "Client IP Address:{}".format(address)
        clientDrone= message.decode()
        print(clientMsg)
        print(clientIP)
        print(clientDrone)
        if(clientDrone == "connect"):
        
            asyncio.run(connect())
            msg = "drone connect"
            bytesToSend = str.encode(msg)
             #message back
            UDPServerSocket.sendto(bytesToSend, address)
        if(clientDrone == "arm"):
        
            asyncio.run(arm())
            msg = "drone arm"
            bytesToSend = str.encode(msg)
             #message back
            UDPServerSocket.sendto(bytesToSend, address)
        if(clientDrone == "disarm"):
        
            asyncio.run(disarm())
            msg = "drone disarm"
            bytesToSend = str.encode(msg)
            #message back
            UDPServerSocket.sendto(bytesToSend, address)
        if(clientDrone == "takeoff"):
        
            asyncio.run(takeoff())
            msg = "drone takeoff"
            bytesToSend = str.encode(msg)
            #message back
            UDPServerSocket.sendto(bytesToSend, address)
        if(clientDrone == "land"):
            asyncio.run(land())
            msg = "drone land"
            bytesToSend = str.encode(msg)
            #message back
            UDPServerSocket.sendto(bytesToSend, address)
        if(clientDrone == "position"):
            pos= str(asyncio.run(position()))
            msg = "drone position :\n"+pos
            bytesToSend = str.encode(msg)
            #message back
            UDPServerSocket.sendto(bytesToSend, address)




serverudp()
