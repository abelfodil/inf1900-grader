# Polytechnique Montréal

Département de génie informatique et génie logiciel

INF1900: Projet initial de système embarqué

# Grille de correction des programmes:

Identification:
+ Travail    : __TRAVAIL_PRATIQUE__
+ Section #  : __SECTION__
+ Équipe #   : __EQUIPE_NO__
+ Correcteur : __CORRECTEUR__

# Initialisation (Points 15)
| Pénalité par erreur                                                                                     |             |
| ------------------------------------------------------------------------------------------------------- | ----------- |
| Le *baud rate* est correctement initialisé                                                              | (/1)        |
| 1er afficheur 7 segment affiche `A`                                                                     | (/1.5)      |
| 2ieme afficheur 7 segement affiche `B`                                                                  | (/1.5)      |
| 3ieme afficheur 7 segment affiche  `C`                                                                  | (/1.5)      |
| 4ieme afficheur 7 segment affiche `D`                                                                   | (/1.5)      |
| Les afficheurs affichent pendant 2 secondes                                                             | (/1)        |
| Désactiver les afficheurs lors du passage en mode détection                                             | (/1)        |
| Les 2 roues tournent à 100% en sens horaire pendant 1 sec et ensuite en sens anti-horaire pendant 1 sec | (/2)        |
| Passage en mode détection après l'initialisation                                                        | (/1)        |
| Toutes les composantes fonctionnent bien ensemble et dans l'ordre                                       | (/3)        |
| __Résultat partiel__                                                                                    | __(/15.0)__ |


# Convertisseur Analogique-Numérique (Points 30)
## Can Interne (Points 10)
| Pénalité par erreur                                               |             |
| ----------------------------------------------------------------- | ----------- |
| Lorsque j'appuie sur le bouton `I` le CAN interne est sélectionné | (/2)        |
| Les valeurs sont correctement saisie avec un ratio de 1volt = 1cm | (/6)        |
| Les valeurs saises ont une précision de &pm;0.3cm                 | (/2)        |
| __Résultat partiel__                                              | __(/10.0)__ |

## Can externe (Points 10)
| Pénalité par erreur                                               |             |
| ----------------------------------------------------------------- | ----------- |
| Lorsque j'appuie sur le bouton `E` le CAN externe est sélectionné | (/2)        |
| Les valeurs sont correctement saisie avec un ratio de 1volt = 1cm | (/6)        |
| Les valeurs saises ont une précision de &pm;1cm                   | (/2)        |
| __Résultat partiel__                                              | __(/10.0)__ |

## GP2D12 (Points 10)
| Pénalité par erreur                                                                  |             |
| ------------------------------------------------------------------------------------ | ----------- |
| Les lectures de GP2D12 se font une à la suite de l'autre à intervalles réguliers     | (/1)        |
| La fréquence par défaut est 1 fois par seconde                                       | (/1)        |
| Lorsque j'appuie sur le bouton `1` les lectures de GP2D12 se font 1 fois par seconde | (/2)        |
| Lorsque j'appuie sur le bouton `2` les lectures de GP2D12 se font 2 fois par seconde | (/3)        |
| Lorsque j'appuie sur le bouton `4` les lectures de GP2D12 se font 4 fois par seconde | (/3)        |
| __Résultat partiel__                                                                 | __(/10.0)__ |

# Terminal RS-232 (Points 25)
## Affichage lors de l'initialisation (Points 3)
| Pénalité par erreur                               |            |
| ------------------------------------------------- | ---------- |
| Le *baud Rate* s'affiche au bon moment            | (/1)       |
| L'affichage respecte le format `X bps`            | (/1)       |
| Il n'a pas de *lag* entre l'action et l'affichage | (/1)       |
| __Résultat partiel__                              | __(/3.0)__ |

## Affichage détection (Points 11)
| Pénalité par erreur                                                                   |             |
| ------------------------------------------------------------------------------------- | ----------- |
| Le mode d'affichage par défaut est *R*                                                | (/1)        |
| Les lectures de GP2D12 s'affiche selon le mode *R*                                    | (/2)        |
| Les lectures de GP2D12 s'affiche selon le mode *V*                                    | (/2)        |
| Les lectures de GP2D12 s'affiche selon le mode *C*                                    | (/2)        |
| L'affichage respecte le format `MM:SS.CC – G:GG.G C:CC.C D:DD.D – CATG|CATC|CATD (X)` | (/3)        |
| Il n'a pas de *lag* entre l'action et l'affichage                                     | (/1)        |
| __Résultat partiel__                                                                  | __(/11.0)__ |

## Affichage Clavier (Points 4)
| Pénalité par erreur                                                   |            |
| --------------------------------------------------------------------- | ---------- |
| Le bouton appuyé est affiché au bon moment                            | (/2)       |
| L'affichage respecte le format `Le bouton X du clavier a été appuyé.` | (/1)       |
| Il n'a pas de *lag* entre l'action et l'affichage de chaque élément   | (/1)       |
| __Résultat partiel__                                                  | __(/4.0)__ |

## Affichage  Manoeuvre (Points 7)
| Pénalité par erreur                                                               |            |
| --------------------------------------------------------------------------------- | ---------- |
| La manoeuvre exécutée est affichée au bon moment                                  | (/1)       |
| Les distances détectées sont associées aux bonnes catégories                      | (/3)       |
| L'affichage respecte le format `Manoeuvre X` si elle est évalué                   | (/1)       |
| L'affichage respecte le format `Combinaison non évaluée` si elle n'est pas évalué | (/1)       |
| Il n'a pas de *lag* entre l'action et l'affichage                                 | (/1)       |
| __Résultat partiel__                                                              | __(/7.0)__ |


# Manœuvres (Points 30)

## Opération en lien avec les manoeuvres (Points 5)
| Pénalité par erreur                                                                                |            |
| -------------------------------------------------------------------------------------------------- | ---------- |
| Le bouton-poussoir fait bien passer en mode la manoeuvre                                           | (/1)       |
| Le robot retourne en mode détection à la fin de la manoeuvre                                       | (/1)       |
| Les pourcentages de vitesse sont correctement affichés sur les blocs 7 segments                    | (/1)       |
| Il est possible d'alterner entre les bases 10 et 16 pour l'affichage de vitesse avec le bouton `#` | (/2)       |
| __Résultat partiel__                                                                               | __(/5.0)__ |

## Manoeuvre 1 (Points 5)
| Pénalité par erreur                                                              | -1.0       |
| -------------------------------------------------------------------------------- | ---------- |
| Vitesse initiale : (-35, 35). On laisse passer 1500 ms.                          |            |
| On change la vitesse pour (35, 35) et on laisse passer 2000 ms.                  |            |
| On change la vitesse pour (35, -35) et on laisse passer 1500 ms.                 |            |
| On change la vitesse pour (35, 35) et on passe à l’étape suivante.               |            |
| La vitesse monte graduellement de (35, 35) à (95, 95) à raison de +5 par 125 ms. |            |
| On laisse passer 2000 ms.                                                        |            |
| __Résultat partiel__                                                             | __(/5.0)__ |

## Manoeuvre 2 (Points 5)
| Pénalité par erreur                                                              | -1.0       |
| -------------------------------------------------------------------------------- | ---------- |
| Vitesse initiale : (35, -35). On laisse passer 1500 ms.                          |            |
| On change la vitesse pour (35, 35) et on laisse passer 2000 ms.                  |            |
| On change la vitesse pour (-35, 35) et on laisse passer 1500 ms.                 |            |
| On change la vitesse pour (35, 35) et on passe à l’étape suivante.               |            |
| La vitesse monte graduellement de (35, 35) à (95, 95) à raison de +5 par 125 ms. |            |
| On laisse passer 2000 ms.                                                        |            |
| __Résultat partiel__                                                             | __(/5.0)__ |

## Manoeuvre 3 (Points 5)
| Pénalité par erreur                                                               | -1.0       |
| --------------------------------------------------------------------------------- | ---------- |
| Vitesse initiale : (-50, -50). On laisse passer 1000 ms.                          |            |
| On change la vitesse pour (-70, 70) et on laisse passer 1500 ms.                  |            |
| On change la vitesse pour (0, 0) et on passe à l'étape suivante.                  |            |
| La vitesse monte graduellement de (0, 0) à (99, 99) à raison de +3 par 50 ms.     |            |
| La vitesse baisse graduellement de (99, 99) à (74, 74) à raison de -5 par 500 ms. |            |
| On laisse passer 2000 ms.                                                         |            |
| __Résultat partiel__                                                              | __(/5.0)__ |

## Manoeuvre 4 (Points 5)
| Pénalité par erreur                                                                       | -1.0       |
| ----------------------------------------------------------------------------------------- | ---------- |
| Vitesse initiale : (78, 78).                                                              |            |
| La vitesse de la roue gauche descend graduellement jusqu'à 48, à raison de -2 par 250 ms. |            |
| On laisse passer 1500 ms.                                                                 |            |
| La vitesse de la roue gauche remonte graduellement jusqu'à 78, à raison de +2 par 250 ms. |            |
| On laisse passer 2000 ms.                                                                 |            |
| __Résultat partiel__                                                                      | __(/5.0)__ |

## Manoeuvre 5 (Points 5)
| Pénalité par erreur                                                                       | -1.0       |
| ----------------------------------------------------------------------------------------- | ---------- |
| Vitesse initiale : (78, 78).                                                              |            |
| La vitesse de la roue droite descend graduellement jusqu'à 48, à raison de -2 par 250 ms. |            |
| On laisse passer 1500 ms.                                                                 |            |
| La vitesse de la roue droite remonte graduellement jusqu'à 78, à raison de +2 par 250 ms. |            |
| On laisse passer 2000 ms.                                                                 |            |
| __Résultat partiel__                                                                      | __(/5.0)__ |



__Total des points: /100__

# Commentaires du correcteur:

À remplir par l'évaluateur