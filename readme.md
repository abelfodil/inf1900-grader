# Dépendances
- Python 3.6+
- bs4
- html5lib
- GitPython

# Prérequis
- `git config --global user.name "Votre Nom"`

# Comment ça marche
- Lancez le script `./start.py`.
- Suivez les étapes linéairement (clone, puis grade, puis compile).
- Après avoir lancé l'option `grade`, il faut attribuer les notes manuellement, mais la majorité du travail 
répétitif est déjà automatisée.
- L'option `compile` fera un commit et merge sur chaque repo, puis générera un fichier de notes `grades.csv`.
- Il est possible de corriger plusieurs travaux simultanément.

# Ce qui manque
- Enregistrement de quelques informations pour ne pas avoir à les fournir à chaque reprise.
- Installation automatique des dépendances.
- Input sanitization pour ne pas faire crash l'outil.
- Envoi du fichier de notes par email à Jérôme.
- Ajouter clang-format pour lint le code.

# Contributeurs
- Anes Belfodil
- Philippe Carphin