# Installation des Dépendances
Pour installer les dépendances, il suffit d'utiliser __pip__ pour
installer la liste des dépendances, globalement ou localement.

Voici la liste des étapes à suivre:

1. `$ virtualenv -p python3.6 my_environment`
2. `$ source ./my_environment/bin/activate`
3. `$ pip install -r requirements.txt`
4. `$ deactivate`

La première étape est faite une seule fois après avoir cloné.  Elle
permet de créer un environnement virtuel pour python.

La seconde étape permet d'activer l'environnement virtuel.  Cela doit
être fait à chaque fois que l'on souhaite travailler sur le projet.  

La troisième étape permet d'installer la liste des dépendances.  Cela
est fait uniquement la première fois.

La dernière étape vous permet de quitter l'environnement virtuel
lorsque vous avez terminé de travailler.

Notez que vous n'êtes pas obligé d'utiliser un environnement virtuel.
Vous pouvez simplement installer les dépendances globalement sur votre
système.  Pour ce faire, simplement faire l'étape 3 après avoir cloné.

Si vous souhaitez utiliser un environnement virtuel (recommander),
vous devez installer le programme __virtualenv__.

# Prérequis
- `git config --global user.name "Votre Nom"`

# Comment ça marche
- Lancez le script `./start.py`.
- Suivez les étapes linéairement (`clone`, puis `grade`, puis `assemble`).

# Résumé des différentes étapes
- `clone` récupérera les informations des élèves (nom, prénom, équipe,
  groupe) depuis le site du cours et clonera le repo de chaque équipe.
  
- `grade` vérifiera les fichiers inutiles, compilera le code des
  élèves et écrira un fichier de notes dans chaque repo.  Il faut
  attribuer les notes manuellement, mais la majorité du travail
  répétitif est déjà automatisée.

- `assemble` fera un commit et merge sur chaque repo, puis générera un
  fichier de notes `grades.csv`.

# Notes
- Certaines informations sont redemandées entre plusieurs étapes afin
  de pouvoir corriger plusieurs travaux simultanément.

# Ce qui manque
- Installation automatique des dépendances.
- Ajouter clang-format pour lint le code.
- Envoi du fichier de notes par email à Jérôme.

# Contributeurs
- Anes Belfodil
- Philippe Carphin
