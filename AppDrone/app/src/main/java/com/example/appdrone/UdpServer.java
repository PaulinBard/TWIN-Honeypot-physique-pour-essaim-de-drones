package com.example.appdrone;

import java.net.*;

public class UdpServer {
    public static void main(String[] args) throws Exception {
        int localPort = 20001;
        byte[] receiveBuffer = new byte[1024];

        try (// Create a datagram socket
        DatagramSocket serverSocket = new DatagramSocket(localPort)) {
            System.out.println("UDP server up and listening");

            // Listen for incoming datagrams
            while(true) {
                DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
                serverSocket.receive(receivePacket);

                String message = new String(receivePacket.getData(), 0, receivePacket.getLength());
                String clientMsg = "Message from Client: " + message;
                String clientIP = "Client IP Address: " + receivePacket.getAddress().getHostAddress();

                System.out.println(clientMsg);
                System.out.println(clientIP);
            }
        }
    }
}
