#!/usr/bin/env python3

"""Sends a UDP packet for each line read from stdin and prints the messages received.

Sends each line read from stdin to the proxy and prints the messages received.
An empty line closes the connection.

Usage:
    python echo.py
"""

import sys
import socket
import conf

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((conf.PROXY_ADDRESS, conf.PROXY_PORT))

while True:
    line = sys.stdin.readline()
    if line == '\n':
        print('closing connection')
        s.close()
        break
    s.send(line.encode(encoding='utf-8'))

    data = s.recv(1500)
    print(data.decode(encoding='utf-8'), end='')

