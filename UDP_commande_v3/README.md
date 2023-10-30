# test_sever_client_udp
comme udp commande 2 + threads

# FAIT:
2 threads qui font le renvoie et l'envoie direct des msg entre sims et client


# PROBLEME: 
## mav sdk bug
toujours un probelme pour repondre a exemple/test-mavlink.py
En recherche pour solver le probleme
## rep negative a pymavlink
sans traitement les commande mavlink ne sont pas toute accepeter d'ou l'idée du mix sdk pymav dans les versions d'avant.




# TO DO

## faire un server proxy threads

## implementer version compatible apli mavsdk    (px4)
connection sdk -> juste print ping =OK
arm ->problem dans le ack arm/ pas de rep a comm 511 = EN COURS

## tester version
-Faire des tests en générale pour assurer le bon fonctionement dans plusieur situation critiques.

## uttiliser 2 drones
-Résussir a faire fonctionner le multi-sims peut import la version -> vrai demo twin.
-Une fois le code stable , tester sur des vrais drones
## augmenter version
-Ajouter plus de fonction a l'archive existante.
-move forward up down etc


