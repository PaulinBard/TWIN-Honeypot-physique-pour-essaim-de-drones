package com.example.appdrone;
import android.content.DialogInterface;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.content.Intent;

import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    private void ajouterNouveauBouton(String nom, String ip, String port, LinearLayout linearLayout) {
        Button nouveauBouton = new Button(this);
        nouveauBouton.setText(nom);
        nouveauBouton.setId(View.generateViewId());
        nouveauBouton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, VueDrone.class);
                intent.putExtra("name", nom);
                intent.putExtra("ip", ip);
                intent.putExtra("port", port);
                startActivity(intent);
            }
        });
        linearLayout.addView(nouveauBouton);
    }

    private void afficherDialogueSaisieTexte(LinearLayout linearLayout) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Entrez les informations");

        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);

        final EditText adresseIPEditText = new EditText(this);
        adresseIPEditText.setHint("IP");
        layout.addView(adresseIPEditText);

        final EditText portEditText = new EditText(this);
        portEditText.setHint("Port");
        layout.addView(portEditText);

        final EditText nomEditText = new EditText(this);
        nomEditText.setHint("Nom");
        layout.addView(nomEditText);

        builder.setView(layout);

        builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                String adresseIP = adresseIPEditText.getText().toString();
                String port = portEditText.getText().toString();
                String nom = nomEditText.getText().toString();
                ajouterNouveauBouton(nom, adresseIP, port, linearLayout);
            }
        });

        builder.setNegativeButton("Annuler", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.cancel();
            }
        });

        builder.show();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        LinearLayout linearLayout = findViewById(R.id.linear_layout);

        ActionBar actionBar = getSupportActionBar();
        if (actionBar != null) {
            actionBar.setTitle("Choix du drone");
        }

        //On ajoute ce drone de base pour faire des tests
        ajouterNouveauBouton("Local", "127.0.0.1", "20001", linearLayout);


        Button ajouter = findViewById(R.id.ajouter);
        ajouter.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                afficherDialogueSaisieTexte(linearLayout);
            }
        });

    }

}