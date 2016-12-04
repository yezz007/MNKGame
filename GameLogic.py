from tkinter import *
from TileStandard import *

class GameLogic:
    '''
    Class yang mengatur logika permainan
    '''
    def __init__(self):
        self.baris = 1
        self.kolom = 1
        self.menang = 1
        self.tileObjList = []

    def setupEvaluator(self, canvas, baris, kolom, menang, tiles, helper):
        self.canvas = canvas
        self.baris = baris
        self.kolom = kolom
        self.menang = menang
        self.helperText = helper
        self.tileObjList = tiles

    def updateHelper(self):
        if TileStandard.staticIntTurn == 1:
            self.canvas.itemconfigure(self.helperText, text='Player 1 Turn')
        elif TileStandard.staticIntTurn == 2:
            self.canvas.itemconfigure(self.helperText, text='Player 2 Turn')

    def evaluate(self):
        '''
        Mengevaluasi apakah sudah ada yang menang
        '''
        self.updateHelper()
        #Jumlah tile yang dikuasai oleh pemain berturut-turut
        intP1Lines = 0
        intP2Lines = 0
        intFlag = 0
        #evaluasi per baris jika n >= k:
        if self.kolom >= self.menang:
            for i in range(self.baris*self.kolom):
                self.tileObjList[i].setFlag(intFlag)
                intFlag += 1
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
                    self.win(1, intFlag - self.menang)
                    return
                elif intP2Lines == self.menang:
                    self.win(2, intFlag - self.menang)
                    return
        #evaluasi per kolom jika baris >= n:
        if self.baris >= self.menang:
            i = 0
            j = 0
            while j < self.baris:
                self.tileObjList[i].setFlag(intFlag)
                intFlag += 1
                if i < self.kolom: #mulai pada kolom baru
                    intP2Lines = 0
                    intP1Lines = 0
                if self.tileObjList[i].getOccupant() == 1:
                    intP1Lines += 1
                    intP2Lines = 0
                elif self.tileObjList[i].getOccupant() == 2:
                    intP1Lines = 0
                    intP2Lines += 1
                else:
                    intP1Lines = 0
                    intP2Lines = 0
                if intP1Lines == self.menang:
                    self.win(1, intFlag - self.menang)
                    return
                elif intP2Lines == self.menang:
                    self.win(2, intFlag - self.menang)
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
                        self.tileObjList[j].setFlag(intFlag)
                        intFlag += 1
                        if self.tileObjList[j].getOccupant() == 1:
                            intP1Lines += 1
                            intP2Lines = 0
                        elif self.tileObjList[j].getOccupant() == 2:
                            intP2Lines += 1
                            intP1Lines = 0
                        else:
                            intP1Lines = 0
                            intP2Lines = 0
                        if intP1Lines == self.menang:
                            self.win(1, intFlag - self.menang)
                            return
                        elif intP2Lines == self.menang:
                            self.win(2, intFlag - self.menang)
                            return
                        j += self.kolom + 1
                else:
                    break
            #evaluasi yang dimulai dari baris pertama, diagonal lain
            for i in range(self.kolom-1, -1, -1):
                if ((i-1) + ((self.menang - 1) * (self.kolom - 1))) % self.kolom < (self.kolom - self.menang):
                    #logika untuk mengecek apa mungkin dalam satu diagonal diperoleh k tiles
                    j = i
                    intP2Lines = 0
                    intP1Lines = 0
                    while(j < self.baris*self.kolom):
                        self.tileObjList[j].setFlag(intFlag)
                        intFlag += 1
                        if self.tileObjList[j].getOccupant() == 1:
                            intP1Lines += 1
                            intP2Lines = 0
                        elif self.tileObjList[j].getOccupant() == 2:
                            intP2Lines += 1
                            intP1Lines = 0
                        else:
                            intP1Lines = 0
                            intP2Lines = 0
                        if intP1Lines == self.menang:
                            self.win(1, intFlag - self.menang)
                            return
                        elif intP2Lines == self.menang:
                            self.win(2, intFlag - self.menang)
                            return
                        j += self.kolom - 1
                else:
                    print("({} + ({}-1 * {}-1)) % {} ? {} {}".format(i, self.menang, self.kolom,
                    self.kolom, self.kolom, self.menang))
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
                        self.tileObjList[j].setFlag(intFlag)
                        intFlag += 1
                        if self.tileObjList[j].getOccupant() == 1:
                            intP1Lines += 1
                            intP2Lines = 0
                        elif self.tileObjList[j].getOccupant() == 2:
                            intP2Lines += 1
                            intP1Lines = 0
                        else:
                            intP1Lines = 0
                            intP2Lines = 0
                        if intP1Lines == self.menang:
                            self.win(1, intFlag - self.menang)
                            return
                        elif intP2Lines == self.menang:
                            self.win(2, intFlag - self.menang)
                            return
                        j += self.kolom + 1
                else:
                    break
                #periksa baris berikutnya(kolom 1)
                i += self.kolom
            #evaluasi yang dimulai dari kolom pertama, diagonal lain
            i = self.kolom-1 #0 sudah diperiksa
            while (i < self.baris*self.kolom):
                if (i + ((self.menang - 1) * (self.kolom + 1))) < (self.baris*self.kolom):
                    #logika untuk mengecek apa mungkin dalam satu diagonal diperoleh k tiles
                    j = i
                    intP2Lines = 0
                    intP1Lines = 0
                    while(j < self.baris*self.kolom):
                        self.tileObjList[j].setFlag(intFlag)
                        intFlag += 1
                        if self.tileObjList[j].getOccupant() == 1:
                            intP1Lines += 1
                            intP2Lines = 0
                        elif self.tileObjList[j].getOccupant() == 2:
                            intP2Lines += 1
                            intP1Lines = 0
                        else:
                            intP1Lines = 0
                            intP2Lines = 0
                        if intP1Lines == self.menang:
                            self.win(1, intFlag - self.menang)
                            return
                        elif intP2Lines == self.menang:
                            self.win(2, intFlag - self.menang)
                            return
                        j += self.kolom - 1
                else:
                    break
                #periksa baris berikutnya(kolom 1)
                i += self.kolom

    def win(self, winnerId, winnerFlag):
        TileStandard.staticBoolWin = True
        if winnerId == 1:
            self.canvas.itemconfigure(self.helperText, text='Player 1 Win!')
        else:
            self.canvas.itemconfigure(self.helperText, text='Player 2 Win!')
        print('win')
        for tiles in self.tileObjList:
            if (tiles.getFlag() > (winnerFlag + self.menang)):
                break
            if (tiles.getFlag() >= winnerFlag):
                tiles.markWinner()
