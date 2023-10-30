package com.example.appdrone;

import static android.app.PendingIntent.getActivity;

import android.content.Intent;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.media.MediaPlayer;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.VideoView;

import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;

import androidx.appcompat.app.AppCompatActivity;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

public class VueDrone extends AppCompatActivity
{

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        //INITIALISATION
        setContentView(R.layout.vue_drone);;
        super.onCreate(savedInstanceState);
        VideoView videoView = findViewById(R.id.video);
        TextView console = findViewById(R.id.Console);
        Intent intent = getIntent();
        String name = intent.getStringExtra("name");
        String ip = intent.getStringExtra("ip");
        String port = intent.getStringExtra("port");
        console.setText("");
        ActionBar actionBar = getSupportActionBar();
        if (actionBar != null) {
            actionBar.setTitle(name);
        }
        String videoPath = "android.resource://" + getPackageName() + "/" + R.raw.no;
        videoView.setVideoPath(videoPath);

        //CONNEXION AU DRONE
        InetAddress serverAddress = null;
        try {
            serverAddress = InetAddress.getByName(ip);
        } catch (UnknownHostException e) {
            throw new RuntimeException(e);
        }
        int serverPort = Integer.parseInt(port);

        //BOUTON LAND
        Button land = findViewById(R.id.land);
        InetAddress finalServerAddress = serverAddress;
        land.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v) {
                console.append("\nLand");
                String message = "land";
                byte[] sendData = message.getBytes();
                UdpClient udpClientTask = new UdpClient(finalServerAddress, serverPort, sendData);
                udpClientTask.executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
            }
        });

        //BOUTON TAKEOFF
        Button takeOff = findViewById(R.id.takeOff);
        takeOff.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v) {
                console.append("\ntakeOff");
                String message = "connect";
                byte[] sendData = message.getBytes();
                UdpClient udpClientTask = new UdpClient(finalServerAddress, serverPort, sendData);
                udpClientTask.execute();

                message = "arm";
                sendData = message.getBytes();
                udpClientTask = new UdpClient(finalServerAddress, serverPort, sendData);
                udpClientTask.execute();

                message = "takeoff";
                sendData = message.getBytes();
                udpClientTask = new UdpClient(finalServerAddress, serverPort, sendData);
                udpClientTask.execute();
            }
        });


        //BOUTON CAMERA
        Button camera = findViewById(R.id.Camera);
        final boolean[] on = {false};
        camera.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v) {
                if(on[0])
                {
                    on[0] = false;
                    console.append("\nCameraOff");
                    String videoPath = "android.resource://" + getPackageName() + "/" + R.raw.no;
                    videoView.setVideoPath(videoPath);
                }
                else {
                    on[0] = true;
                    console.append("\nCameraOn");
                    String videoPath = "android.resource://" + getPackageName() + "/" + R.raw.drone;
                    videoView.setVideoPath(videoPath);
                }
            }
        });
        videoView.setOnPreparedListener(new MediaPlayer.OnPreparedListener() {
            @Override
            public void onPrepared(MediaPlayer mp) {
                mp.setLooping(true);
                videoView.start();
            }
        });


        //BOUTON GPS
        Button gps = findViewById(R.id.GPS);
        gps.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v) {
                console.append("\ngps");
                String message = "position";
                byte[] sendData = message.getBytes();
                UdpClient udpClientTask = new UdpClient(finalServerAddress, serverPort, sendData);
                udpClientTask.execute();
            }
        });

    }

}
