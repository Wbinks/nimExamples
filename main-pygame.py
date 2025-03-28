import pygame_functions as pg

pg.screenSize(900,900,50,50)
pg.setBackgroundColour("lightgreen")
pg.setAutoUpdate(False)

# put screen elements here, so they are global
infoLabel = pg.makeLabel("Info here",40,30,30,"black","Consolas")
pg.showLabel(infoLabel)
submitbutton = pg.makeSprite("submit.png")
pg.moveSprite(submitbutton,600,100,centre=True)
pg.showSprite(submitbutton)
undo = pg.makeSprite("undo.png")
pg.moveSprite(undo,800,100,centre=True)
pg.showSprite(undo)

def drawScreen(piles,numberchosen,pilechosen):
    # code to draw the stones
    y = 300
    x = 100
    pg.clearShapes()
    for pilenum in range(len(piles)):
        if pilenum == pilechosen:
            reduction = numberchosen
        else:
            reduction = 0
        for stoneNum in range(piles[pilenum]-reduction):
            pg.drawEllipse(x,y,70,50,"blue")
            y += 50
        x += 200
        y = 300
    pg.updateDisplay()

def setupGame():
    # create the data structure for a new game
    piles = [7,5,3,1]
    return piles


def playerMove():
    # code to track mouse movements and do actions, then return their move
    moveMade = False
    pilechosen=None
    numberchosen = 0
    pg.changeLabel(infoLabel, f"Your move")
    while not moveMade:
        if pg.spriteClicked(submitbutton):
            if pilechosen is not None and numberchosen > 0:    
                return pilechosen, numberchosen
        elif pg.spriteClicked(undo):
            pg.changeLabel(infoLabel, f"Undo clicked")
            pilechosen = None
            numberchosen = 0
        elif pg.mousePressed():
            #clicked in the screen
            column = (pg.mouseX())//200
            if pilechosen is None:
                pilechosen = column
            if column == pilechosen:
                numberchosen +=1
                if piles[pilechosen]<numberchosen:
                    numberchosen = piles[pilechosen]
            else:
                pg.changeLabel(infoLabel,"You can only click one pile")
            while pg.mousePressed():
                pg.tick(50)
        drawScreen(piles, numberchosen, pilechosen)
        pg.updateDisplay()
        pg.tick(50)
    return 1

# main game
piles = setupGame()
gameRunning = True
while gameRunning:
    pilechosen, numberchosen = playerMove()
    piles[pilechosen] -= numberchosen
    drawScreen(piles,0,0)
    # now the computer makes a move!
    pg.changeLabel(infoLabel,"Computer Move")
    pg.pause(2000)
