# Prérequis
- `$ git config --global credential.helper store`
- `$ git config --global user.name "Votre Nom"`
- `$ git config --global user.email prenom.nom@polymtl.ca`
- `$ pip3 install --user -r requirements.txt`
- [Outils AVR](http://www.groupes.polymtl.ca/inf1900/fichiers/)

# Comment ça marche
- Lancez le script `./grader`.
- Suivez les étapes dans l'ordre dans lequel elles sont présentées.

# Résumé des différentes étapes
- `clone` récupérera les informations des élèves (nom, prénom, équipe,
  groupe) depuis le site du cours et clonera le repo de chaque équipe.
  
- `grade` vérifiera les fichiers inutiles, compilera le code des
  élèves et écrira un fichier de notes dans chaque repo.  Il faut
  attribuer les notes manuellement, mais la majorité du travail
  répétitif est déjà automatisée.

- `assemble` créera un commit et merge sur chaque repo, puis générera un
  fichier de notes `notes-inf1900-sectionXX-nom_travail.csv`.
  
- `mail` enverra un email à Jérôme et joindra le fichier de notes `csv`.

# Notes
- Certaines informations sont redemandées entre plusieurs étapes afin
  de pouvoir corriger plusieurs travaux simultanément.

# Ce qui manque
- Utiliser clang-format et clang-tidy pour plus d'automatisations.
- Simuler le matériel pour plus d'automatisations.
