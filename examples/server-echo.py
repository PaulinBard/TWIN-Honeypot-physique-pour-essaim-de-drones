#!/usr/bin/env python3
"""UDP server that prints the messages it receives and sends them back.

Usage:
    python server-echo.py
"""

import socket
import conf

s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
s.bind(('', conf.PROXY_PORT))

while True:
    bytes, address = s.recvfrom(1500)
    print('received data :')
    h = bytes.hex()
    s.sendto(bytes, address)
    print(f"{address} : {' '.join(h[i:i+2] for i in range(0, len(h), 2))}")

print ("closing connection")
s.close()