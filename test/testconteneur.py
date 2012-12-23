#!/usr/bin/env python
# -*- coding: utf-8 -*-

from minitel.Minitel import Minitel
from minitel.ui.ChampTexte import ChampTexte
from minitel.ui.Conteneur import Conteneur
from minitel.ui.Label import Label

minitel = Minitel()

minitel.deviner_vitesse()
minitel.identifier()
minitel.definir_vitesse(1200)
minitel.definir_mode('VIDEOTEX')
minitel.configurer_clavier(etendu = True, curseur = False, minuscule = True)
minitel.echo(False)
minitel.efface()
minitel.curseur(False)

conteneur = Conteneur(minitel, 1, 1, 40, 24)

labelNom = Label(minitel, 1, 10, u"Nom")
champNom = ChampTexte(minitel, 10, 10, 20, 60)
labelPrenom = Label(minitel, 1, 12, u"Prénom")
champPrenom = ChampTexte(minitel, 10, 12, 20, 60)

conteneur.ajoute(labelNom)
conteneur.ajoute(champNom)
conteneur.ajoute(labelPrenom)
conteneur.ajoute(champPrenom)
conteneur.affiche()

conteneur.executer()

minitel.close()

