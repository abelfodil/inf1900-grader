# Dépendances
- Python 3
- bs4
- GitPython

# Comment ça marche
- Lancez le script `./start.py`.
- Suivez les étapes linéairement (clone, puis grade, puis compile).
- Après avoir lancé l'option `grade`, il faut attribuer les notes manuellement, mais la majorité du travail 
répétitif est déjà automatisée.
- L'option `compile` enverra les notes automatiquement aux élèves et générera un fichier de notes 
`grades.csv` automatiquement.

# Notes importantes
- Vous ne devez pas corriger plusieurs TP ou groupes en même temps, car cela risque d'écraser le fichier 
`students.json` qui est autogénéré et qui sert à compiler les notes des étudiants.

# Ce qui manque
- Enregistrement de quelques informations pour ne pas avoir à les fournir à chaque reprise.
- Installation automatique des dépendances.
- Input sanitization pour ne pas faire crash l'outil.

# Credits
- Anes Belfodil (pythonification)
- Philippe Carphin (idée originale https://github.com/PhilippeCarphin/git-teacher-tools)