from tkinter import *

NbRow = 25          # nombre de colones
NbColumn = 40       # nombre de ligne

sizeCel = 20        # taille de la cellule

bombes = 100        # nombre de bombe
drapeaux = 100      # nombre de drapeau

root = Tk()
root.title("Démineur")

drapNb = IntVar()
bombeNb = IntVar()

etat_jeu = 0        # à utiliser plus tard pour eviter la varriable de la classe cellule

canvas = Canvas(root, width=800, height=500, bg="light yellow", highlightthickness=2, highlightbackground="black", bd=0)
canvas.grid(padx=25, pady=25)

