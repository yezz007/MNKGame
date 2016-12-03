from tkinter import *
from TileStandard import *
from GameLogic import *

class BoardStandard(Frame):
    '''
    Papan permainannya. Merupakan turunan dari tkinter.Frame.
    '''
    def __init__(self, parent, logic, baris, kolom, menang, squareSize=50):
        super().__init__(parent)
        self.pack()
        self.gameLogic = logic
        self.parent = parent
        self.baris = baris
        self.kolom = kolom
        self.menang = menang
        self.size = squareSize
        self.setColors()
        self.canvas = Canvas(self, bg=self.borderColor,
        width=(self.kolom*self.size)+10, height=(self.baris*self.size)+10)
        self.canvas.pack()
        self.tileObjList = [] #list berisikan objek kotak-kotak
        self.populateBoard()
        print("Board built", self)

    def getTilesList(self):
        return self.tileObjList

    def getCanvasHandler(self):
        return self.canvas

    def setColors(self):
        self.borderColor = 'black'
        self.neutralColor = 'white'
        self.squareBorder = 'black'
        self.p1Color = 'blue'
        self.p2Color = 'red'

    def endGame(self):
        self.tileObjList.clear()
        self.canvas.delete("all")

    def populateBoard(self):
        x = 5
        y = 5
        for i in range(self.baris):
            x = 5
            for j in range(self.kolom):
                self.tileObjList.append(TileStandard(self.canvas, x, y, self.size,
                self.neutralColor, self.squareBorder, self.p1Color, self.p2Color, command=self.gameLogic.evaluate))
                x += self.size
            y += self.size
        self.gameLogic.setupEvaluator(self.baris, self.kolom, self.menang, self.tileObjList)
