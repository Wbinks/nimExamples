import tkinter as tk
from tkinter import font as tkFont
import random

class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("950x900+0+0")
        self.theCanvas = tk.Canvas(self,width=800, height=900, bg="#ddddff")
        self.theCanvas.grid(row=0, column=0,rowspan=4)
        self.buttonfont = tkFont.Font(family="Consolas", weight="bold")

        self.button1 = tk.Button(self, text="Done", font=self.buttonfont, command = self.doneclicked)
        self.button1.grid(row=1, column=1,sticky="NSEW")
        self.button2 = tk.Button(self, text="Undo", font=self.buttonfont, command = self.undoclicked)
        self.button2.grid(row=2, column=1,sticky="NSEW")
        self.rowconfigure(3,weight=1)
        self.rowconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        
        self.theCanvas.bind("<Motion>", self.mouseMoved)
        self.theCanvas.bind("<Button-1>", self.mouseClicked)

        
        self.movetext=None
        self.infotext = None
        self.stonepic = tk.PhotoImage(file="stone.png")


        self.columnchosen = None
        self.numberchosen = 0
        self.gameState = 0 # 0 is human turn
        self.stonepics = []
        self.setupGame()
        self.mainloop()


    def doneclicked(self):
        print("Player move done")
        self.piles[self.columnchosen] -= self.numberchosen
        self.columnchosen = None
        self.numberchosen = 0
        self.drawBoard()
        # now Do Computer Turn!


    def undoclicked(self):
        self.columnchosen = None
        self.numberchosen = 0
        self.drawBoard()

    def mouseMoved(self,e):
        self.theCanvas.delete(self.movetext)
        self.movetext = self.theCanvas.create_text(20,20, text=f"moved to {e.x}, {e.y}", anchor="nw")

    def mouseClicked(self,e):
        column = e.x//200
        self.theCanvas.delete(self.infotext)
        self.infotext = self.theCanvas.create_text(750,20, text=f"Chose Column {column}", anchor="ne")
        if self.columnchosen is None:
            self.columnchosen = column
        if self.columnchosen != column:
            self.theCanvas.itemconfig(self.infotext,text="You can only choose one pile")
        else:
            self.theCanvas.itemconfig(self.infotext,text="OK")
            self.numberchosen +=1
            if self.piles[self.columnchosen]<self.numberchosen:
                self.numberchosen = self.piles
            self.drawBoard()

    def setupGame(self):
        self.piles = [7,5,3,1]
        self.drawBoard()

    def drawBoard(self):
        # delete all the old stone pictures
        for s in self.stonepics:
            self.theCanvas.delete(s)
        self.stonepics = []
        # draw the piles of stones
        # Go through each value in self.piles
        # draw the right number of stones in the right place

        y = 300
        x = 100
        for pilenumn in range(len(self.piles)):
            if pilenumn == self.columnchosen:
                reduction = self.numberchosen
            else:
                reduction = 0
            for stoneNum in range(self.piles[pilenumn] - reduction):
                self.stonepics.append(self.theCanvas.create_image(x,y,image=self.stonepic))
                y += 50
            x += 200
            y = 300

app = Main()
