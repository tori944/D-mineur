from initCanva import *
from random import *

class Cellule :
    global NbColumn, NbRow, bombes, drapeaux, etat_jeu

    listeCellules = []

    versLaVictoire = 0

    etat_jeu_Cel = 0

    
    def __init__(self, coA, coB, row, column):
        Cellule.listeCellules.append(self)

        self.id = Cellule.listeCellules.index(self)

        self.row = row
        self.column = column

        self.coA = coA
        self.coB = coB

        self.etat = 0       # 0 -> Caché / 1 -> Découverte(clic)
        self.type = 0       # 0 -> Neutre / 1 -> Bombe
        self.drapeau = 0    # 0 -> pas de Drapeau / 1 -> a un Drapeau (seulement pour un état de 0) 


        self.rec = canvas.create_rectangle(coA+1, coB+1, coA+sizeCel+1, coB+sizeCel+1, fill='black', outline="gray") # outline=""
        # canvas.create_text(self.coA+10, self.coB+10, text=self.type, fill="white")
        

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
            # else:                                                           # une bombe
            #     canvas.itemconfig(self.rec, fill="red", outline="")

    
    def set_drapeau (self, nb):  
        self.drapeau = nb
        if self.get_drapeau() == 1:
            canvas.itemconfig(self.rec, fill="orange", outline="")
        elif self.get_drapeau() == 0:
            canvas.itemconfig(self.rec, fill="black", outline="gray")

    def set_type (self, nb):
        self.type = nb


    def voisinesID (self): # liste des id des voisines

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

    
    def indice_Bombe (self): # indice de bombe
        NbVoisineB = 0

        for j in (self.voisinesID()):
                cel = Cellule.listeCellules[j]
                if cel.get_type() == 1:
                   NbVoisineB += 1
        
        return NbVoisineB
    
    def config_color(self):
        canvas.itemconfig(self.rec, fill="pink")

    

    def decouvert (self):
        global etat_jeu, NbColumn, NbRow, bombes

        if self.get_etat() != 1 and self.get_drapeau() == 0:  # si l'état est different de découvert (donc caché ou caché avec indice) et sans drapeau
            # self.etat = 1

            self.set_etat(1)

            if self.get_type() == 0: # il n'y a pas de bombe
                Cellule.versLaVictoire += 1
                print("vers la victoire", Cellule.versLaVictoire)
                if self.indice_Bombe() != 0:
                    canvas.create_text(self.coA+10, self.coB+10, text=self.indice_Bombe(), fill="white", tags="LesIndices")
                # self.aUnIndice = 1
                # canvas.itemconfig(self.rec, fill="green")
                
                # dévoilé les cases qui n'ont pas de bombe autour
                # dévoilé les incdices de bombe des cases saines     

                elif self.indice_Bombe() == 0:                # si indice de bombe null -> découvrir les voisines qui n'ont pas de bombes
                    for celID in self.voisinesID():         # on parcourt la liste des id des voisines
                        cel = Cellule.listeCellules[celID]  # cel est l'objet cellule du tableau des cellules en fonction de son ID
                        # cel.config_color()  <- ça fonctionne 
                        cel.decouvert()

                if Cellule.versLaVictoire == (NbRow*NbColumn)-bombes : # revoir cette valeur pr ce que je n'ai pas compris
                    print("Vous avez gagné yhouhou !")
                    canvas.create_text(400, 250, text="c'est gagné bg", fill="pink", font=("", 70), tags="LesIndices")

            else:               # il y a une bombe
                #etat_jeu = 2  # pour ne plus pouvoir clic
                Cellule.etat_jeu_Cel = 2
                canvas.create_text(400, 250, text="Perdu !", fill="pink", font=("", 70), tags="LesIndices")
                
                for cel in Cellule.listeCellules:

                    if cel.get_type() == 1:
                        canvas.itemconfig(cel.rec, fill="red", outline="gray")
            
    
    def determine_bombe (self):
        
                  # boucle de nombre de bombe

        newListeCel = []                # liste sans celle qui a été cliqué
        
        for cell in Cellule.listeCellules:
            if cell != self:
                newListeCel.append(cell)

        for i in range (bombes):  
            cel = choice(newListeCel)

            cel.set_type(1)       # cellule selectionné pour être une bombe
            canvas.create_text(cel.coA+10, cel.coB+10, text=cel.get_type(), fill="white", tags="LesIndices")
            # del newListeCel[cel.get_id]
            newListeCel.remove(cel)
            # labelType = canvas.create_text(cel.coA+10, cel.coB+10, text=cel.get_type(), fill="white", tags="LesIndices")
        # Cellule.nombreDrapeau = bombes  # le nombre de drapeau est égale à celui des bombes
        drapNb.set(drapeaux)        # lignes pas ouf 
        bombeNb.set(bombes)         # pour les varriables affiché
        print("il faut : ", (NbRow*NbColumn)-bombes)
        print("il y a ", bombes, "bombes")


    def clicG (self, event):
        
        global etat_jeu
        #print("etat de jeu", Cellule.etat_jeu_Cel)
        
        if Cellule.etat_jeu_Cel != 2:                       # etat_jeu = 2 lorsque c'est perdu
            
            if Cellule.etat_jeu_Cel == 0:  
                #print("on va ùetre les Bombes", Cellule.etat_jeu_Cel)               # le tout premier clic 
                self.determine_bombe()                  # placé les bombes
                Cellule.etat_jeu_Cel = 1
                #print("on a mis les bombes ", Cellule.etat_jeu_Cel)
            
            self.decouvert()


    def clicD (self, event):
        global etat_jeu, drapeaux
        if Cellule.etat_jeu_Cel != 2:                               # etat_jeu = 2 lorsque c'est perdu
            if self.get_etat() == 0:                    # si pas découverte

                if self.get_drapeau() == 0 :            # pas de drapeau
                    self.set_drapeau(1)                 # mettre un drapeau
                    drapeaux -= 1                       # nombre de drapeau -1
                    drapNb.set(drapeaux)                # drapNb (Drapeau Nombre) varriable affiché
                    
                else:                                   # retirer le drapeau
                    self.set_drapeau(0)
                    drapeaux += 1
                    drapNb.set(drapeaux)


# toujours en construction mais au moins ça fonctionne ! 