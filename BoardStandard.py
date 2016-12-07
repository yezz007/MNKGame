from tkinter import *
from TileStandard import *
from TileExOu import *
from TileCoin import *
from GameLogic import *

class BoardStandard(Frame):
    '''
    Papan permainannya. Merupakan turunan dari tkinter.Frame.
    Versi standarnya. Kalau mau menambah versi lain, turunkan dari kelas ini.
    '''
    def __init__(self, parent, logic, baris, kolom, menang, extend, tileModel, squareSize=50, **kwargs):
        super().__init__(parent)
        self.pack()
        self.gameLogic = logic
        self.parent = parent
        self.baris = baris
        self.kolom = kolom
        self.extend = extend // 2
        self.menang = menang
        self.size = squareSize
        self.p1Name = 'Player 1'
        self.p2Name = 'Player 2'
        self.tileModel = tileModel
        self.fireEventOnEnd = False
        self.tileObjList = [] #list berisikan objek kotak-kotak
        self.canSaveGame = False
        if 'eventOnEndGame' in kwargs:
            self.fireEventOnEnd = True
            self.eventOnEnd = kwargs['eventOnEndGame']
        if 'p1Name' in kwargs:
            self.p1Name = kwargs['p1Name']
        if 'p2Name' in kwargs:
            self.p2Name = kwargs['p2Name']
        if 'eventOnSaveGame' in kwargs:
            self.canSaveGame = True
            self.eventOnSaveGame = kwargs['eventOnSaveGame']
        #Semua atribut sudah terdaftar, memanggil method-method yang diperlukan
        self.setColors()
        self.canvas = Canvas(self, bg=self.borderColor,
        width=(self.kolom*self.size)+10+extend, height=(self.baris*self.size)+40)
        self.canvas.pack()
        self.populateBoard()
        self.createButtons()
        self.createHelper()
        print("Board built", self)

    def createHelper(self):
        self.helper = self.canvas.create_text(((self.kolom*self.size)//2)+self.extend, (self.baris*self.size)+20,
        font = 'Helvetica 16', fill=self.neutralColor, text='Giliran {}'.format(self.p1Name))

    def setHelperText(self, txt):
        self.canvas.itemconfigure(self.helper, text=txt)

    def createButtons(self):
        self.crossDefaultColor = self.neutralColor
        self.crossMouseOverColor = 'red'
        self.saveDefaultColor = self.neutralColor
        self.saveMouseOverColor = '#0029ff' #biru cerah
        self.crossBitmap = BitmapImage(file='cross.xbm', foreground=self.crossDefaultColor)
        self.saveBitmap = BitmapImage(file='save.xbm', foreground=self.saveDefaultColor)
        self.endButton = self.canvas.create_image((self.kolom*self.size)-10+(self.extend*2), (self.baris*self.size)+20,
        image=self.crossBitmap)
        self.saveButton = self.canvas.create_image((self.kolom*self.size)-40+(self.extend*2), (self.baris*self.size)+20,
        image=self.saveBitmap)
        self.canvas.tag_bind(self.endButton, "<Enter>", self.onEndButtonMouseEnter)
        self.canvas.tag_bind(self.endButton, "<Leave>", self.onEndButtonMouseLeave)
        self.canvas.tag_bind(self.endButton, "<ButtonRelease-1>", self.onEndGame)
        self.canvas.tag_bind(self.endButton, "<Button-1>", self.onEndButtonMouseClick)
        self.canvas.tag_bind(self.saveButton, "<Enter>", self.onSaveButtonMouseEnter)
        self.canvas.tag_bind(self.saveButton, "<Leave>", self.onSaveButtonMouseLeave)
        self.canvas.tag_bind(self.saveButton, "<ButtonRelease-1>", self.onSaveGame)
        self.canvas.tag_bind(self.saveButton, "<Button-1>", self.onSaveButtonMouseClick)

    def onSaveGame(self, event):
        if self.canSaveGame:
            self.eventOnSaveGame()

    def onEndButtonMouseClick(self, event):
        self.crossBitmap.config(foreground='#1aff0e') #hijau muda

    def onWin(self):
        self.crossBitmap.config(foreground='red')
        self.saveBitmap.config(foreground='#0029ff')
        self.crossDefaultColor = 'red'
        self.crossMouseOverColor = '#ff5c00' #merah kekuningan
        self.saveDefaultColor = '#0029ff' #biru cerah
        self.saveMouseOverColor = '#31b8cd' #biru langit

    def onEndButtonMouseEnter(self, event):
        self.crossBitmap.config(foreground=self.crossMouseOverColor)

    def onEndButtonMouseLeave(self, event):
        self.crossBitmap.config(foreground=self.crossDefaultColor)

    def onSaveButtonMouseClick(self, event):
        self.saveBitmap.config(foreground='#1aff0e') #hijau muda

    def onSaveButtonMouseEnter(self, event):
        self.saveBitmap.config(foreground=self.saveMouseOverColor) #Biru cerah

    def onSaveButtonMouseLeave(self, event):
        self.saveBitmap.config(foreground=self.saveDefaultColor)

    def setColors(self):
        '''
        Mengatur warna papan.
        Untuk class turunan, sebaiknya neutralColor kontras dengan borderColor, begitu
        juga untuk p1 dan p2 color
        '''
        self.borderColor = 'black'
        self.neutralColor = 'white'
        self.squareBorder = 'black'
        self.p1Color = '#1aff0e' #hijau muda
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
                if self.tileModel == 1:
                    self.tileObjList.append(TileStandard(self.canvas, x, y, self.size,
                    self.neutralColor, self.squareBorder, self.p1Color, self.p2Color,
                    command=self.gameLogic.occupyTile))
                elif self.tileModel == 2:
                    self.tileObjList.append(TileExOu(self.canvas, x, y, self.size,
                    self.neutralColor, self.squareBorder, self.p1Color, self.p2Color,
                    command=self.gameLogic.occupyTile))
                elif self.tileModel == 3:
                    self.tileObjList.append(TileCoin(self.canvas, x, y, self.size,
                    self.neutralColor, self.squareBorder, self.p1Color, self.p2Color,
                    command=self.gameLogic.occupyTile))
                x += self.size
            y += self.size
        self.gameLogic.setupEvaluator(self.baris, self.kolom, self.menang, self.tileObjList,
        self.p1Name, self.p2Name, helperChanger=self.setHelperText, eventOnWin=self.onWin)
