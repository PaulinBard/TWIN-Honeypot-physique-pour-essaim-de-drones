# test_sever_client_udp
Avoir un serveur qui ouvre un port et ecoute en attendant des instruction de l'application et les transmet a une simulation.


Pour uttiliser la v1
Lancer une simulation de PX4, exemple: make px4_sitl jmavsim
    (elle ouvre automatiquement le port 14550 pour recevoir des message.)

Lancer les fichier python serverudp et client udp: python3 serverudp.py
                                                   python3 clientudp.py
# a savoir
-ignorer les print d'erreur cote server 
- relancer le clientudp pour chaque commande car il fonctionne comme un bouton



Pour la suite:
-uttiliser mavlink entre le client/serveur pour permettre l'uttilisationn de n'importe qu'elle platform d'envoie.

-Modifier le serveur pour qu'il uttilise deux simulations/drones en fonctions de la dangerosité de l'action.