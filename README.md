# Simulation de Chemins de Désir

Ce projet a pour objectif de reproduire la mécanique des chemins de désir à l'aide d'une simulation utilisant des agents qui explorent un environnement. Les agents tentent de trouver des trajectoires optimales entre différents points d'intérêt à l'aide d'un algorithme inspiré de l'évolution.

## 🧠 Qu'est-ce qu'un chemin de désir ?

Un chemin de désir est un sentier tracé de manière spontanée par les déplacements répétés des individus. Ces chemins émergent lorsqu'une route alternative plus directe ou plus pratique est empruntée au lieu des voies prévues (ex. : un raccourci à travers une pelouse).

## 📊 Fonctionnalités principales

* Simulation de déplacements d'agents dans un environnement 2D.

* Évaluation des trajectoires en fonction de la proximité à la destination.

* Algorithme évolutif avec sélection, croisement et mutation.

* Visualisation des agents et des points d'intérêt via Pygame.

## 🛠️ Installation

* Assurez-vous d'avoir Python 3 installé sur votre machine.

* Clonez ce dépôt :

```
git clone https://github.com/Romain-Fournet/Desire-Paths.git  
cd Desire-Paths
```

* Créez un environnement virtuel (optionnel mais recommandé) :
```
python -m venv venv
source venv/bin/activate
```
* Installez les dépendances :
```
pip install -r requirements.txt
```


## ▶️ Utilisation

Lancez la simulation avec :
```
python main.py
```
## 🔍 Paramètres principaux :

POP_SIZE : Taille de la population d'agents (par défaut 1000).

MAX_STEPS : Nombre maximum de pas qu'un agent peut effectuer.

GENERATION : Nombre de générations de l'algorithme évolutif.

MUTATION_RATE : Taux de mutation (probabilité qu'un mouvement soit modifié).

## 📊 Comportement des agents :

Les agents se déplacent aléatoirement au début.

Les trajectoires sont évaluées selon leur proximité à la destination.

Les meilleurs agents sont sélectionnés et leurs mouvements sont croisés et mutés.

Le score favorise les chemins plus courts et plus directs.

## 📌 Améliorations possibles

Optimisation de l'algorithme de sélection et de mutation.

Ajouter des obstacles pour simuler des environnements plus complexes.

Exporter les trajectoires finales pour analyse.

Personnaliser la carte et les points d'intérêt.

