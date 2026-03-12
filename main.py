from Cellule import *

for i in range (NbRow):
    for j in range (NbColumn):
        Cellule(j*sizeCel, i*sizeCel, i, j)
    

def rejouer ():
    global etat_jeu, drapeaux
    for cel in Cellule.listeCellules:
        cel.set_type(0)
        cel.set_etat(0)
        cel.set_drapeau(0)

    #etat_jeu = 0
    Cellule.etat_jeu_Cel = 0
    Cellule.versLaVictoire = 0
    Cellule.drapeaux = bombes

    # drapeaux = bombes

    drapNb.set(0)
    bombeNb.set(0)
    
    canvas.delete("LesIndices")


frame = Frame(root)
frame.grid(sticky=EW, padx=10, pady=10)

frame.columnconfigure([0, 1, 2], weight=1)

frame2 = Frame(frame)
frame2.grid(column=0, row=0, pady=10)

frame3 = Frame(frame)
frame3.grid(column=1, row=0, pady=10)

LabelAa = Label(frame2, text="Nombre de bombes :", font=("",15))
LabelAa.grid()
labelAb = Label(frame2, textvariable=bombeNb, font=("",15))
labelAb. grid()

labelA = Label(frame3, text="Nombre de drapeau : ", font=("",15))
labelA. grid()
labelAb = Label(frame3, textvariable=drapNb, font=("",15))
labelAb. grid()

btn = Button(frame, text="rejouer", command=rejouer, font=("",15))
btn.grid(column=2, row=0, pady=10)


root.mainloop()