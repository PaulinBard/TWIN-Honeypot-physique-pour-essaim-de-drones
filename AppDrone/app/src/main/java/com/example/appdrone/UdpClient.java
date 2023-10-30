package com.example.appdrone;

import android.os.AsyncTask;
import android.util.Log;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

public class UdpClient extends AsyncTask<Void, Void, Void>
{
    private InetAddress serverAddress;
    private int serverPort;
    private byte[] sendData;

    private DatagramSocket clientSocket = null;

    public UdpClient(InetAddress address, int port, byte[] sendData) {
        this.serverAddress = address;
        this.serverPort = port;
        this.sendData = sendData;
    }

    protected Void doInBackground(Void... voids) {
        Log.d("ip", serverAddress.toString());
        Log.d("port", String.valueOf(serverPort));
        Log.d("data", sendData.toString());
        DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, serverAddress, serverPort);
        try {
            clientSocket = new DatagramSocket();
        } catch (SocketException e) {
            throw new RuntimeException(e);
        }
        try {
            clientSocket.send(sendPacket);
        } catch (IOException e) {
            Log.d("erreur", "paquet non envoyé");
            throw new RuntimeException(e);
        }
        return null;
    }

    protected void onPostExecute(Void result) {
        clientSocket.close();
    }

}
