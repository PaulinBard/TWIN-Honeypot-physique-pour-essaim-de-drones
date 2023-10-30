# TWIN : Honeypot physique pour essaim de drones

## Installation


```sh
# creattioon de l'environnement virtuel
python -m venv .venv

# activation de l'environnement virtuel
source .venv/bin/activate

# installation des paquets requis
pip install -r requirements.txt
```

## Utilisation

### Exemples

#### Utilisation du proxy
Le proxy peut être utilisé en UDP ou en TCP. (commenter le code correspondant)

```sh
# lancement du proxy
python server-proxy.py

# test de la connexion
# un drone doit écouter sur le port spécifié dans conf.py
python test-mavlink.py
```

