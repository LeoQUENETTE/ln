# Projet de langage naturelle sur JeuxDeMots

## Introduction
JeuxDeMots est un site permettant l'étude des liens sémantique entre les mots en utilisant un biais ludique accessible à tous, les jeux de mots. Nous avons utilisé les données du sites avec les relations entre des mots pour déterminer la proximité des mots entre eux.

## Mise en place

Utilisation de python, et sauvegarde des données une fois la requête a JeuxDeMots effectué. Le projet est séparé entre le fichier main permettant de lier les différents composants, un fichier permettant la sauvegarde des données, et un fichier d'appel à l'API. Les fichier de stockage se trouve dans le dossier stockage, sauf pour les noeuds qui se trouve dans le dossier principal.

## Prérequis

Pour faire fonctionner ce projet il est nécessaire de posséder sur sa machine une version de python, si possible vieille de moins de 5 ans.
Pour installer python : [Installer] https://www.python.org/downloads/

## Lancement

Une fois le projet cloner déplacer vous dans le dossier du projet :

`cd ln`

Ensuite lancer la commande suivante : 

``python main.py``

ou en cas d'erreur

``py main.py``

Cela lancera le calcul de toutes les requêtes demandé pour le projet d'un seul coup.
Si vous voulez modifier les requêtes il vous sera nécessaire de modifier directement le code en rajoutant un appel à une commande dans le fichier main.py, dans le if principal ligne 149.

