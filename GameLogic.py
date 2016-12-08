from tkinter import *
from TileStandard import *

class GameLogic:
    '''
    Class yang mengatur logika permainan
    '''
    def __init__(self):
        '''
        Constructor yang hanya formalitas...
        Setidaknya disini dapat terlihat dengan jelas
        semua atribut kelas ini, bersih dari logika
        Semua diatur di method setupEvaluator
        '''
        self.baris = 1
        self.kolom = 1
        self.menang = 1
        self.tileObjList = []
        self.turn = 1 # giliran player 1
        self.hasWinner = False
        self.p1Name = 'Player 1'
        self.p2Name = 'Player 2'
        self.hasEventHelperChange = False
        self.hasEventOnWin = False
        self.winner = 0

    def setupEvaluator(self, baris, kolom, menang, tiles, p1Name, p2Name, **kwargs):
        '''
        Mengatur ulang evaluator untuk permainan yang berbeda
        '''
        self.baris = baris
        self.kolom = kolom
        self.menang = menang
        self.tileObjList = tiles
        self.p1Name = p1Name
        self.p2Name = p2Name
        self.turn = 1 # giliran player 1
        self.hasWinner = False
        self.hasEventHelperChange = False
        self.hasEventOnWin = False
        self.winner = 0
        #teks yang menunjukkan 'Giliran player 1'
        if 'helperChanger' in kwargs:
            self.hasEventHelperChange = True
            self.setHelperText = kwargs['helperChanger'] #dengan 1 argumen: text
        #memanggil method ketika permainan berakhir
        if 'eventOnWin' in kwargs:
            self.hasEventOnWin = True
            self.eventOnWin = kwargs['eventOnWin']

    def updateHelper(self):
        '''
        Jika pada set up memperbolehkan untuk memberi teks bantuan, maka teks akan diubah
        '''
        if self.hasEventHelperChange:
            if self.hasWinner:
                self.setHelperText('Permainan sudah selesai. -->')
            elif self.turn == 1:
                self.setHelperText('Giliran {}'.format(self.p1Name))
            elif self.turn == 2:
                self.setHelperText('Giliran {}'.format(self.p2Name))

    def occupyTile(self, tile):
        '''
        Method yang ditrigger oleh event yang diatur class Tile
        '''
        if not (tile.isOccupied() or self.hasWinner):
            if self.turn == 1:
                occupantId = 1
                self.turn = 2
            else:
                self.turn = 1
                occupantId = 2
            tile.occupy(occupantId)
            self.updateHelper()
            self.evaluate()
        else:
            self.updateHelper()

    def evaluate(self):
        '''
        Mengevaluasi apakah sudah ada yang menang
        '''
        #Jumlah tile yang dikuasai oleh pemain berturut-turut
        intP1Lines = 0
        intP2Lines = 0
        intNeutral = self.baris*self.kolom
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
                    intNeutral -= 1
                elif self.tileObjList[i].getOccupant() == 2:
                    intP1Lines = 0
                    intP2Lines += 1
                    intNeutral -= 1
                else:
                    intP1Lines = 0
                    intP2Lines = 0
                if intP1Lines == self.menang:
                    self.win(1, intFlag - self.menang)
                    return
                elif intP2Lines == self.menang:
                    self.win(2, intFlag - self.menang)
                    return
        if intNeutral <= 0: #Penuh
            self.hasWinner = True
            if self.hasEventOnWin:
                self.eventOnWin()
            if self.hasEventHelperChange:
                self.setHelperText('Tidak ada yang menang!')
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
            #evaluasi yang dimulai dari kolom terakhir, diagonal lain
            i = self.kolom-1 #kolom terakhir
            while (i < self.baris*self.kolom):
                if (i + ((self.menang - 1) * (self.kolom - 1))) < (self.baris*self.kolom):
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
        '''
        Menghentikan kerja evaluator jika sudah menang
        Menandai tiles yang bertanggung jawab untuk memenangkan game
        '''
        self.hasWinner = True
        if winnerId == 1:
            self.winner = 1
            if self.hasEventHelperChange:
                self.setHelperText('{} Menang!'.format(self.p1Name))
        else:
            self.winner = 2
            if self.hasEventHelperChange:
                self.setHelperText('{} Menang!'.format(self.p2Name))
        print('win')
        for tiles in self.tileObjList:
            if (tiles.getFlag() > (winnerFlag + self.menang)):
                break
            if (tiles.getFlag() >= winnerFlag):
                tiles.markWinner()
        if self.hasEventOnWin:
            self.eventOnWin()

    def getTilesOccupantList(self):
        '''
        Mereturn list yang berisikan integer yang merepresentasikan 'tile 1 diambil oleh player 1'
        Berguna untuk save game
        '''
        lisTileOccupant = []
        for tiles in self.tileObjList:
            lisTileOccupant.append(tiles.getOccupant())
        return lisTileOccupant

    def getCurrentTurn(self):
        '''
        Mengembalikan nilai variabel giliran untuk savegame
        '''
        return self.turn

    def getWinnerId(self):
        '''
        Mengembalikan variabel pemenang untuk savegame
        '''
        return self.winner

    def continueFromSavedPoint(self, tileOccupants, turn):
        '''
        Mengaktifkan tile yang sudah diambil alih setelah load game
        '''
        for i in range(len(self.tileObjList)):
            if tileOccupants[i] == 1:
                self.tileObjList[i].occupy(1)
            elif tileOccupants[i] == 2:
                self.tileObjList[i].occupy(2)
        self.turn = turn
        self.updateHelper()
        self.evaluate()
