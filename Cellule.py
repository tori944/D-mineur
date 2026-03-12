from initCanva import *
from random import *

class Cellule :
    global NbColumn, NbRow, bombes, etat_jeu

    listeCellules = []

    versLaVictoire = 0

    etat_jeu_Cel = 0

    drapeaux = bombes
    
    def __init__(self, coA, coB, row, column):
        Cellule.listeCellules.append(self)

        self.id = Cellule.listeCellules.index(self)

        self.row = row
        self.column = column

        self.coA = coA
        self.coB = coB

        self.etat = 0       # 0 -> Caché / 1 -> Découverte(clicG)
        self.type = 0       # 0 -> Neutre / 1 -> Bombe
        self.drapeau = 0    # 0 -> pas de Drapeau / 1 -> a un Drapeau (seulement pour un état de 0) (clicD)


        self.rec = canvas.create_rectangle(coA+1, coB+1, coA+sizeCel+1, coB+sizeCel+1, fill='black', outline="gray")

        canvas.tag_bind(self.rec, "<Button-1>", self.clicG)
        canvas.tag_bind(self.rec, "<Button-3>", self.clicD)

    def get_id (self):
        return self.id 
    
    def get_etat (self):
        return self.etat

    def get_row (self):
        return self.row
    
    def get_column (self):
        return self.column
    
    def get_type (self):
        return self.type

    def get_drapeau (self):
        return self.drapeau


    def set_etat (self, etat):  
        self.etat = etat
        if self.get_etat() == 1:  
            if self.get_type() == 0:                                        # pas de bombe
                canvas.itemconfig(self.rec, fill="green", outline="")

    
    def set_drapeau (self, nb):  
        self.drapeau = nb
        if self.get_drapeau() == 1:
            canvas.itemconfig(self.rec, fill="orange", outline="")
        elif self.get_drapeau() == 0:
            canvas.itemconfig(self.rec, fill="black", outline="gray")

    def set_type (self, nb):
        self.type = nb


    def voisinesID (self): # liste des id des voisines (trouvé une meilleure manière de faire cette fonction)

        myId = self.get_id()
        myRow = self.get_row()
        myColumn = self.get_column()
        
        idVoisines = [NbColumn-1, NbColumn, NbColumn+1, -1, 1, (-NbColumn)-1, (-NbColumn), (-NbColumn)+1]

        if myColumn == NbColumn-1 : 
            del idVoisines[7]
            del idVoisines[4]
            del idVoisines[2]
        
        if myColumn == 0 :
            del idVoisines[5]
            del idVoisines[3]
            del idVoisines[0]

        listeVoisinesID = []

        for i in (idVoisines):
            if 0 <= myId + i < len(Cellule.listeCellules):

                listeVoisinesID.append(myId+i)

        return listeVoisinesID

    
    def indice_Bombe (self):    # indice de bombe (si il y en a à coté)
        NbVoisineB = 0

        for j in (self.voisinesID()):
                cel = Cellule.listeCellules[j]
                if cel.get_type() == 1:
                   NbVoisineB += 1
        
        return NbVoisineB


    def decouvert (self):
        global etat_jeu, NbColumn, NbRow, bombes

        if self.get_etat() != 1 and self.get_drapeau() == 0:    # si l'état est different de découvert (donc caché) et sans drapeau
            self.set_etat(1)                                    # devient découvert

            if self.get_type() == 0:                            # il n'y a pas de bombe
                Cellule.versLaVictoire += 1                     # compteur du nombre de cases saines découvertes 
                
                if self.indice_Bombe() != 0:                    # si il y a des voisines bombes (indice != 0)
                    canvas.create_text(self.coA+10, self.coB+10, text=self.indice_Bombe(), fill="white", tags="LesIndices")  # indiquer l'indice sur la cellule
                
                # dévoilé les cases qui n'ont pas de bombe autour (indice = 0)
                # dévoilé les incdices de bombe des cases saines     

                elif self.indice_Bombe() == 0:                  # si indice de bombe null -> découvrir les voisines car aucune n'a de bombe
                    for celID in self.voisinesID():             # on parcourt la liste des id des voisines
                        cel = Cellule.listeCellules[celID]      # cel est l'objet cellule du tableau des cellules en fonction de son ID 
                        cel.decouvert()

                if Cellule.versLaVictoire == (NbRow*NbColumn)-bombes : # si on a découvert toutes les cellules saines
                    canvas.create_text(400, 250, text="c'est gagné BG", fill="pink", font=("", 70), tags="LesIndices")

            else:                                               # Oups, il y a une bombe
                Cellule.etat_jeu_Cel = 2
                canvas.create_text(400, 250, text="Perdu !", fill="pink", font=("", 70), tags="LesIndices")
                
                for cel in Cellule.listeCellules:

                    if cel.get_type() == 1:
                        canvas.itemconfig(cel.rec, fill="red", outline="gray")
            
    
    def determine_bombe (self):                         # selectionne puis initialises les cellules qui sont bombes

        newListeCel = []                                # liste sans celle qui a été cliqué
        
        for cell in Cellule.listeCellules:
            if cell != self:
                newListeCel.append(cell)

        for i in range (bombes):  
            cel = choice(newListeCel)
            cel.set_type(1)                             # cellule selectionné pour être une bombe
            newListeCel.remove(cel)

        drapNb.set(Cellule.drapeaux)                            # lignes pas ouf 
        bombeNb.set(bombes)                             # pour les varriables affiché


    def clicG (self, event):
        
        global etat_jeu
        
        if Cellule.etat_jeu_Cel != 2:                   # etat_jeu = 2 lorsque c'est perdu
            
            if Cellule.etat_jeu_Cel == 0:               # le tout premier clic 
                self.determine_bombe()                  # placé les bombes
                Cellule.etat_jeu_Cel = 1
                
            self.decouvert()


    def clicD (self, event):
        global etat_jeu
        if Cellule.etat_jeu_Cel != 2:                   # etat_jeu = 2 lorsque c'est perdu
            if self.get_etat() == 0:                    # si pas découverte

                if self.get_drapeau() == 0 :            # pas de drapeau
                    self.set_drapeau(1)                 # mettre un drapeau
                    Cellule.drapeaux -= 1                       # nombre de drapeau -1
                    drapNb.set(Cellule.drapeaux)                # drapNb (Drapeau Nombre) varriable affiché
                    
                else:                                   # retirer le drapeau
                    self.set_drapeau(0)
                    Cellule.drapeaux += 1
                    drapNb.set(Cellule.drapeaux)


# toujours en construction mais au moins ça fonctionne ! 