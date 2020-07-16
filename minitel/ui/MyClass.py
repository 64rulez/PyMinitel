#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from .UI import UI
from ..Sequence import Sequence
from ..constantes import ENTREE, MAJ_ENTREE, SUITE, RETOUR, ANNULATION

class MyClass(UI):
    def __init__(self, minitel, posx, posy, largeur, hauteur, couleur = None,
                 fond = None, pagevtx = None):
        assert isinstance(posx, int)
        assert isinstance(posy, int)
        assert isinstance(largeur, int)
        assert isinstance(hauteur, int)
        assert isinstance(couleur, (str, int)) or couleur == None
        assert isinstance(fond, (str, int)) or fond == None
        assert isinstance(pagevtx, str) or pagevtx == None

        # Initialisation des attributs
        self.elements = []
        self.element_actif = None
        self.fond = fond
        self.pagevtx = pagevtx
        self.sequence = None

        UI.__init__(self, minitel, posx, posy, largeur, hauteur, couleur)

    def gere_touche(self, sequence):
        assert isinstance(sequence, Sequence)

        self.sequence = sequence
        
        # Aucun élement actif ? Donc rien à faire
        if self.element_actif == None:
            return False

        # Fait suivre la séquence à l’élément actif
        touche_geree = self.element_actif.gere_touche(sequence)

        # Si l’élément actif a traité la séquence, c’est fini
        if touche_geree:
            return True

        # Si l’élément actif n’a pas traité la séquence, regarde si le
        # conteneur peut la traiter

        # La touche [entrée] ou Suite permet de passer au champ suivant
        if sequence.egale(ENTREE) or sequence.egale(SUITE):
            self.element_actif.gere_depart()
            self.suivant()
            self.element_actif.gere_arrivee()
            return True

        # La combinaison [Majuscule + entrée] ou Retour permet de passer au champ précédent
        if sequence.egale(MAJ_ENTREE) or sequence.egale(RETOUR):
            self.element_actif.gere_depart()
            self.precedent()
            self.element_actif.gere_arrivee()
            return True
            
        # La combinaison Annulation permet d'éffacer le champ courant
        if self.sequence.egale(ANNULATION):
                self.element_actif.valeur=""
                self.element_actif.decalage=0
                self.element_actif.curseur_x=0
                self.element_actif.affiche()
                self.element_actif.gere_arrivee()
                return True


        print ( "InMyClass[{}]".format(sequence) )
        print ( "Longueur" )
        print (sequence.longueur )
        print ( "Valeurs" )
        for element in sequence.valeurs:
            print ( element )

        return False
            
    def affiche(self):
        # Colorie le fond du conteneur si une couleur de fond a été définie
        print ( "Page {}".format(self.pagevtx) )
        if self.fond != None:
            for posy in range(self.posy, self.posy + self.hauteur):
                self.minitel.position(self.posx, posy)
                self.minitel.couleur(fond = self.fond)
                self.minitel.repeter(' ', self.largeur)

        # Demande à chaque élément de s’afficher
        for element in self.elements:
            element.affiche()

        # Si un élément actif a été défini, on lui donne la main
        if self.element_actif != None:
            self.element_actif.gere_arrivee()

    def ajoute(self, element):
        assert isinstance(element, UI)
        assert element not in self.elements

        # Attribue la couleur du conteneur à l’élément par défaut
        if element.couleur == None:
            element.couleur = self.couleur

        # Ajoute l’élément à la liste d’éléments du conteneur
        self.elements.append(element)

        if self.element_actif == None and element.activable == True:
            self.element_actif = element

    def suivant(self):
        # S’il n’y a pas d’éléments, il ne peut pas y avoir d’élément actif
        if len(self.elements) == 0:
            return False

        # Récupère l’index de l’élément actif
        if self.element_actif == None:
            index = -1
        else:
            index = self.elements.index(self.element_actif)

        # Recherche l’élément suivant qui soit activable
        while index < len(self.elements) - 1:
            index += 1
            if self.elements[index].activable == True:
                self.element_actif = self.elements[index]
                return True

        return False

    def precedent(self):
        # S’il n’y a pas d’éléments, il ne peut pas y avoir d’élément actif
        if len(self.elements) == 0:
            return False

        # Récupère l’index de l’élément actif
        if self.element_actif == None:
            index = len(self.elements)
        else:
            index = self.elements.index(self.element_actif)

        # Recherche l’élément suivant qui soit activable
        while index > 0:
            index -= 1
            if self.elements[index].activable == True:
                self.element_actif = self.elements[index]
                return True

        return False
#
