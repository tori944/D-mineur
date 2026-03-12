from tkinter import *

NbRow = 25
NbColumn = 40

sizeCel = 20

bombes = 110
drapeaux = 110

root = Tk()
root.title("Démineur")

drapNb = IntVar()
bombeNb = IntVar()

etat_jeu = 0

canvas = Canvas(root, width=800, height=500, bg="light yellow", highlightthickness=2, highlightbackground="black", bd=0)
canvas.grid(padx=25, pady=25)

