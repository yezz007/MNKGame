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
        '''
        parent = tempat widget ini diletakkan
        logic = otak permainan
        baris, kolom, menang = jumlahnya
        extend = ekstensi canvas agar teks 'giliran player 1' muat di layar
        tileModel = model tile 1:warna-warni; 2:X dan O, 3: Koin
        squareSize = ukuran tile
        **kwargs:
            eventOnEndGame: method yang akan dipanggil setelah user klik 'exit'
            eventOnSaveGame: method yang akan dipanggil setelah user klik 'save'
            p1Name: nama pemain pertama
            p2Name: nama pemain kedua
        '''
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
        if self.p1Name == '':
            self.p1Name = 'Anonymous'
        if 'p2Name' in kwargs:
            self.p2Name = kwargs['p2Name']
        if self.p2Name == '':
            self.p2Name = 'Mysterious'
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
        '''Menginstansiasi teks pembantu yang menampilkan 'Giliran player 1'''
        self.helper = self.canvas.create_text(((self.kolom*self.size)//2)+self.extend, (self.baris*self.size)+20,
        font = 'Helvetica 16', fill=self.neutralColor, text='Giliran {}'.format(self.p1Name))

    def setHelperText(self, txt):
        '''Method yang mengubah teks helper'''
        self.canvas.itemconfigure(self.helper, text=txt)

    def createButtons(self):
        '''Membuat tombol-tombol'''
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
        '''Jika ada event saveGame, panggil methodnya'''
        if self.canSaveGame:
            self.eventOnSaveGame()

    def onWin(self):
        '''Mengubah warna ikon ketika menang'''
        self.crossBitmap.config(foreground='red')
        self.saveBitmap.config(foreground='#0029ff')
        self.crossDefaultColor = 'red'
        self.crossMouseOverColor = '#ff5c00' #merah kekuningan
        self.saveDefaultColor = '#0029ff' #biru cerah
        self.saveMouseOverColor = '#31b8cd' #biru langit

    #----------6 method berikut membuat tombol menjadi warna-warni ketika didekati kursor---------

    def onEndButtonMouseClick(self, event):
        self.crossBitmap.config(foreground='#1aff0e') #hijau muda

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
        self.darkerNeutralColor = '#ececec'
        self.squareBorder = 'black'
        self.p1Color = '#1aff0e' #hijau muda
        self.p2Color = 'red'

    def onEndGame(self, event):
        '''Ketika permainan berakhir, panggil method yang sudah dipass'''
        self.tileObjList.clear()
        self.canvas.delete("all")
        if self.fireEventOnEnd:
            self.eventOnEnd()

    def populateBoard(self):
        '''Mengisi papan permainan dengan tiles'''
        x = 5+self.extend
        y = 5
        index = 0
        for i in range(self.baris):
            if i % 2 == 0:
                color1 = self.neutralColor
                color2 = self.darkerNeutralColor
            else:
                color1 = self.darkerNeutralColor
                color2 = self.neutralColor
            x = 5+self.extend
            for j in range(self.kolom):
                if j % 2 == 0:
                    tileColor = color1
                else:
                    tileColor = color2
                if self.tileModel == 1: #pilih model tile
                    self.tileObjList.append(TileStandard(self.canvas, index, x, y, self.size,
                    tileColor, self.squareBorder, self.p1Color, self.p2Color,
                    command=self.gameLogic.occupyTile))
                elif self.tileModel == 2:
                    self.tileObjList.append(TileExOu(self.canvas, index,  x, y, self.size,
                    tileColor, self.squareBorder, self.p1Color, self.p2Color,
                    command=self.gameLogic.occupyTile))
                elif self.tileModel == 3:
                    self.tileObjList.append(TileCoin(self.canvas, index,  x, y, self.size,
                    tileColor, self.squareBorder, self.p1Color, self.p2Color,
                    command=self.gameLogic.occupyTile))
                index += 1
                x += self.size
            y += self.size
        self.gameLogic.setupEvaluator(self.baris, self.kolom, self.menang, self.tileObjList,
        self.p1Name, self.p2Name, helperChanger=self.setHelperText, eventOnWin=self.onWin)
