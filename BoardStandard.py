from tkinter import *
from TileStandard import *
from GameLogic import *

class BoardStandard(Frame):
    '''
    Papan permainannya. Merupakan turunan dari tkinter.Frame.
    '''
    def __init__(self, parent, logic, baris, kolom, menang, extend, squareSize=50, **kwargs):
        super().__init__(parent)
        self.pack()
        self.gameLogic = logic
        self.parent = parent
        self.baris = baris
        self.kolom = kolom
        self.extend = extend // 2
        self.menang = menang
        self.size = squareSize
        self.setColors()
        self.canvas = Canvas(self, bg=self.borderColor,
        width=(self.kolom*self.size)+10+extend, height=(self.baris*self.size)+40)
        self.canvas.pack()
        self.tileObjList = [] #list berisikan objek kotak-kotak
        self.createHelper()
        self.populateBoard()
        self.fireEventOnEnd = False
        if 'onEndGame' in kwargs:
            self.fireEventOnEnd = True
            self.eventOnEnd = kwargs['onEndGame']
        self.createEndButton()
        self.canvas.bind("<Leave>", self.onMouseLeaveCanvas)
        self.userUnderStandHowToQuit = False
        print("Board built", self)

    def createHelper(self):
        self.helper = self.canvas.create_text(((self.kolom*self.size)//2)+self.extend, (self.baris*self.size)+20,
        font = 'Helvetica 16', fill=self.neutralColor, text='Player 1 Turn')

    def onMouseLeaveCanvas(self, event):
        if not self.userUnderStandHowToQuit:
            self.canvas.itemconfigure(self.helper, text='Click that to quit ->')

    def createEndButton(self):
        self.crossBitmap = BitmapImage(file='cross.xbm', foreground='red')
        self.endButton = self.canvas.create_image((self.kolom*self.size)-10+(self.extend*2), (self.baris*self.size)+20,
        image=self.crossBitmap)
        self.canvas.tag_bind(self.endButton, "<Enter>", self.onEndButtonMouseEnter)
        self.canvas.tag_bind(self.endButton, "<Leave>", self.onEndButtonMouseLeave)
        self.canvas.tag_bind(self.endButton, "<ButtonRelease-1>", self.onEndGame)
        self.canvas.tag_bind(self.endButton, "<Button-1>", self.onEndButtonMouseClick)

    def onEndButtonMouseClick(self, event):
        self.crossBitmap.config(foreground='#d200d0')

    def onEndButtonMouseEnter(self, event):
        self.userUnderStandHowToQuit = True
        self.crossBitmap.config(foreground='green')

    def onEndButtonMouseLeave(self, event):
        self.crossBitmap.config(foreground='red')

    def setColors(self):
        self.borderColor = 'black'
        self.neutralColor = 'white'
        self.squareBorder = 'black'
        self.p1Color = 'blue'
        self.p2Color = 'red'

    def onEndGame(self, event):
        self.tileObjList.clear()
        self.canvas.delete("all")
        if self.fireEventOnEnd:
            self.eventOnEnd()

    def populateBoard(self):
        x = 5+self.extend
        y = 5
        for i in range(self.baris):
            x = 5+self.extend
            for j in range(self.kolom):
                self.tileObjList.append(TileStandard(self.canvas, x, y, self.size,
                self.neutralColor, self.squareBorder, self.p1Color, self.p2Color,
                command=self.gameLogic.evaluate))
                x += self.size
            y += self.size
        TileStandard.staticIntTurn = 1
        TileStandard.staticBoolWin = False
        self.gameLogic.setupEvaluator(self.canvas, self.baris, self.kolom, self.menang, self.tileObjList, self.helper)
