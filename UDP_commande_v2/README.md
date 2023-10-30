# test_sever_client_udp
comme udp commande 1

# FAIT:
INCOMPLET
application.py lance des commande au proxy
2 proxy font des echange et parle a la sim
demo video sur mon cremi :
https://paulin-bardon.emi.u-bordeaux.fr/

## partie mavlink cote sim - proxy:

boucle semi pymavlink semi mav sdk actuelle marche  
Tester sur un seul drone 


boucle only pymavlink -> pas fait mais marcherai sous ardupilot pymavlink
boucle only mavsdk -> obliger de comprendre les echange demander a la connection et d'autres commandes surcouche complexes .

# PROBLEME: 
## beacoup d'erreur dans terminal en traitement 
les commandes du module mavsdk sont asynchrones et  uttlisent future et threads . Ce ne sont pas des vrai threads dans le module donc il plante et print des code error mais le programme marche bien .
pour lancer sans le spam erreur:
python3 proxy_drone_pilote.py 2>/dev/null

## fonction takeoff pymavlink marche mais pas comme il faut:
crash du drone problem soit de parametre soit il faut setup le gps ou dautre truc avant avec d'autre focntion.
Donc on uttilise mavsdk pour les commande entre sim et proxy.
Sous ardupilot commande marche
Donc on peut faire une version sans mavsdk si on uttilise ardupilot au lieu de px4.
Exemple dans Z_aide/takeoff.py

## multi sims px4
-sur jmavsim si on lance 2 drones avec la doc, on ne peut pas les controler avec les ports.
-sur gazebo il semble etre fonctionnel, Qgroudncontrol permet de les bouger mais la sims crash rapidement sur mon pc , ce qui m'empeche de faire plus de test.

# TO DO
## implementer version compatible apli mavsdk    (px4)
connection sdk -> juste print ping =OK
arm ->problem dans le ack arm/ pas de rep a comm 511 = EN COURS
Obligation de passer a une version threads ? (beaucoup plus propre)
## améliorer version
-Faire des tests en générale pour assurer le bon fonctionement dans plusieur situation critiques.
-Résussir a faire fonctionner le multi-sims peut import la version -> vrai demo twin.
-Une fois le code stable , tester sur des vrais drones
## augmenter version
-Ajouter plus de fonction a l'archive existante.
-move forward up down etc



## implementer version full pymavlink (ardupilot) 
+commande bas niveaux  mavlink comprise 
- pas de multi sims?

## implementer version full mavsdk    (px4)
+ multi sims en cours de travail
+ api simple d'uttilisation
- complexité des traitement dans le proxy pour repondre a l'api mavsdk

