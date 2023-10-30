#!/usr/bin/env python3
""" UDP server that forwards the UDP packets it receives.

This server forwards the UDP packets it receives from the client to the drone
and sends back the response to the client.

Usage:
    python server-proxy.py
"""

from pymavlink import mavutil
import socket
import conf
from utils import space_hex


drone_addr = (conf.DRONE_ADDRESS, conf.DRONE_PORT)


# socket used to forward the packets received
# UDP
# s_drone = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s_drone.connect(('', conf.DRONE_PORT))
# s_drone.bind(drone_addr)

# TCP
s_drone = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s_drone.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_drone.connect(('', conf.DRONE_PORT))
# s_drone.listen(1)


s_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_client.bind(('', conf.PROXY_PORT))

# creates a UDP server receiving mavlink packets
# master = mavutil.mavlink_connection(f'udpin:localhost:{conf.PROXY_PORT}')

while True:
    # using mavutil
    # client_msg = master.recv()
    # if not client_msg:
    #     continue

    # client_addr = list(master.clients)[0]
    client_msg, client_addr = s_client.recvfrom(1500);
    print(f"↓ c {client_addr} : {space_hex(client_msg.hex())}")

    # send the packet to the drone
    ret = s_drone.send(client_msg)
    print(f"↑ d {drone_addr} : {space_hex(client_msg.hex())} --- {ret}\n")

    # get the response from the drone
    drone_msg = s_drone.recv(1500)
    print(f"↓ d {drone_addr} : {space_hex(drone_msg.hex())}")

    ret = s_client.sendto(drone_msg, client_addr)
    print(f"↑ c {client_addr} : {space_hex(drone_msg.hex())} --- {ret}\n")

