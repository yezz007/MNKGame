from tkinter import *
from TileStandard import *

class BoardStandard(Frame):
    '''
    Papan permainannya. Merupakan turunan dari tkinter.Frame.
    Logika permainannya juga ada di sini.
    '''
    def __init__(self, parent, baris, kolom, menang, squareSize=50):
        super().__init__(parent)
        self.pack()
        self.parent = parent #passed by reference
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
                self.neutralColor, self.squareBorder, self.p1Color, self.p2Color, command=self.evaluate))
                x += self.size
            y += self.size
        #self.canvas.bind("<Button-1>", self.evaluate)

    def evaluate(self):
        '''
        Mengevaluasi apakah sudah ada yang menang
        '''
        #Jumlah tile yang dikuasai oleh pemain berturut-turut
        intP1Lines = 0
        intP2Lines = 0
        #evaluasi per baris jika n >= k:
        if self.kolom >= self.menang:
            for i in range(self.baris*self.kolom):
                if i % self.kolom == 0: #mulai pada baris baru
                    intP2Lines = 0
                    intP1Lines = 0
                if self.tileObjList[i].getOccupant() == 1:
                    intP1Lines += 1
                    intP2Lines = 0
                elif self.tileObjList[i].getOccupant() == 2:
                    intP1Lines = 0
                    intP2Lines += 1
                if intP1Lines == self.menang:
                    self.win(1)
                    return
                elif intP2Lines == self.menang:
                    self.win(2)
                    return
        #evaluasi per kolom jika baris >= n:
        if self.baris >= self.menang:
            i = 0
            j = 0
            while j < self.baris:
                if i < self.kolom: #mulai pada kolom baru
                    intP2Lines = 0
                    intP1Lines = 0
                if self.tileObjList[i].getOccupant() == 1:
                    intP1Lines += 1
                    intP2Lines = 0
                elif self.tileObjList[i].getOccupant() == 2:
                    intP1Lines = 0
                    intP2Lines += 1
                if intP1Lines == self.menang:
                    self.win(1)
                    return
                elif intP2Lines == self.menang:
                    self.win(2)
                    return
                i += self.kolom
                if i >= self.baris*self.kolom:
                    j += 1
                    i = j
        #evaluasi per diagonal, algoritmanya agak ribet
        #Teorema: Jika m < k atau n < k, maka jumlah tile per diagonal pasti < k
        #Teorema tersebut sudah terbukti :)
        if not (self.baris < self.menang or self.kolom < self.menang):
            #evaluasi yang dimulai dari baris pertama
            for i in range(self.kolom):
                if (i + ((self.menang - 1) * (self.kolom + 1))) % self.kolom >= (self.menang - 1):
                    #logika untuk mengecek apa mungkin dalam satu diagonal diperoleh k tiles
                    j = i
                    intP2Lines = 0
                    intP1Lines = 0
                    while(j < self.baris*self.kolom):
                        if self.tileObjList[j].getOccupant() == 1:
                            intP1Lines += 1
                            intP2Lines = 0
                        elif self.tileObjList[j].getOccupant() == 2:
                            intP2Lines += 1
                            intP1Lines = 0
                        if intP1Lines == self.menang:
                            self.win(1)
                            return
                        elif intP2Lines == self.menang:
                            self.win(2)
                            return
                        j += self.kolom + 1
                else:
                    break
            #evaluasi yang dimulai dari kolom pertama
            i = self.kolom #0 sudah diperiksa
            while (i < self.baris*self.kolom):
                if (i + ((self.menang - 1) * (self.kolom + 1))) < (self.baris*self.kolom):
                    #logika untuk mengecek apa mungkin dalam satu diagonal diperoleh k tiles
                    j = i
                    intP2Lines = 0
                    intP1Lines = 0
                    while(j < self.baris*self.kolom):
                        if self.tileObjList[j].getOccupant() == 1:
                            intP1Lines += 1
                            intP2Lines = 0
                        elif self.tileObjList[j].getOccupant() == 2:
                            intP2Lines += 1
                            intP1Lines = 0
                        if intP1Lines == self.menang:
                            self.win(1)
                            return
                        elif intP2Lines == self.menang:
                            self.win(2)
                            return
                        j += self.kolom + 1
                else:
                    break
                #periksa baris berikutnya(kolom 1)
                i += self.kolom

    def win(self, winnerId):
        print('win')
        for tiles in self.tileObjList:
            tiles.occupy(winnerId)
