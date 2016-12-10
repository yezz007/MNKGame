from tkinter import *
from TileStandard import *

class GameLogic:
    '''
    Class yang mengatur logika permainan
    '''
    def __init__(self):
        '''
        hanya memberitahu ada atribut apa saja pada class ini,
        Semua diatur di method setupEvaluator
        '''
        self.baris = 1
        self.kolom = 1
        self.menang = 1
        self.tileObjList = [] #list tile
        self.turn = 1 # giliran player 1 duluan
        self.hasWinner = False #sudah ada yang menang atau belum
        self.p1Name = 'Player 1' #nama default player 1
        self.p2Name = 'Player 2' #nama default player 2
        self.hasEventHelperChange = False #apakah bisa mengubah teks 'giliran player 1'
        self.hasEventOnWin = False #apakah perlu memanggil method ketika sudah ada yang menang
        self.winner = 0 #id pemenang: -1: seri ; 1: player 1 ; 2: player 2
        self.lastOccupiedTileIndex = 0 #index tile yang terakhir kali diambil alih
        self.countOccupied = 0 #menghitung sudah ada berapa tile yang sudah terambil alih

    def setupEvaluator(self, baris, kolom, menang, tiles, p1Name, p2Name, **kwargs):
        '''
        Mengatur ulang evaluator untuk permainan yang berbeda
        baris, kolom, menang = jumlahnya
        tiles = list tiles
        p1Name, p2Name = nama pemain
        **kwargs:
            helperChanger: method untuk mengubah teks
            eventOnWin: method yang dipanggil ketika permainan sudah dimenangkan atau seri
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
        self.countOccupied = 0
        #teks yang menunjukkan 'Giliran player 1'
        if 'helperChanger' in kwargs:
            self.hasEventHelperChange = True
            self.setHelperText = kwargs['helperChanger'] #dengan 1 argumen: text
        #memanggil method ketika permainan berakhir
        if 'eventOnWin' in kwargs:
            self.hasEventOnWin = True
            self.eventOnWin = kwargs['eventOnWin']

    def updateHelper(self):
        '''Jika pada set up memperbolehkan untuk memberi teks bantuan, maka teks akan diubah'''
        if self.hasEventHelperChange:
            if self.hasWinner:
                self.setHelperText('Permainan sudah selesai. -->')
            elif self.turn == 1:
                self.setHelperText('Giliran {}'.format(self.p1Name))
            elif self.turn == 2:
                self.setHelperText('Giliran {}'.format(self.p2Name))

    def occupyTile(self, tileIndex):
        '''Method yang ditrigger oleh event yang diatur class Tile ketika tile diklik
        tileIndex = index tile pada tileObjList'''
        if not (self.tileObjList[tileIndex].isOccupied() or self.hasWinner):
            if self.turn == 1:
                occupantId = 1
                self.turn = 2
            else:
                self.turn = 1
                occupantId = 2
            self.tileObjList[tileIndex].occupy(occupantId)
            self.updateHelper()
            self.countOccupied += 1
            self.evaluate(tileIndex)
            self.lastOccupiedTileIndex = tileIndex
        else:
            self.updateHelper()

    def evaluate(self, index):
        '''Mengiterasi per kotak untuk mengecek apakah permainan sudah berakhir atau belum'''
        currentOccupant = self.tileObjList[index].getOccupant() #pemain yang mengambil alih
        winnerList = [index] #untuk menandai tile yang membantu menang
        #==============ke kiri===============#
        idx = index - 1
        count = 1
        while((idx >= self.kolom*(index//self.kolom)) and
        count < self.menang):
            if self.tileObjList[idx].getOccupant() != currentOccupant:
                break
            count += 1
            winnerList.append(idx)
            idx -= 1
        #==============ke kanan===============#
        idx = index + 1
        while((idx < (self.kolom*(index//self.kolom) + self.kolom)) and
        count < self.menang):
            if self.tileObjList[idx].getOccupant() != currentOccupant:
                break
            count += 1
            winnerList.append(idx)
            idx += 1
        if count >= self.menang:
            self.win(currentOccupant, winnerList)
            return
        winnerList = [index] #untuk menandai tile yang membantu menang
        #==============ke atas===============#
        idx = index - self.kolom
        count = 1
        while((idx >= 0) and count < self.menang):
            if self.tileObjList[idx].getOccupant() != currentOccupant:
                break
            count += 1
            winnerList.append(idx)
            idx -= self.kolom
        #==============ke kanan===============#
        idx = index + self.kolom
        while((idx < (self.kolom*self.baris)) and
        count < self.menang):
            if self.tileObjList[idx].getOccupant() != currentOccupant:
                break
            count += 1
            winnerList.append(idx)
            idx += self.kolom
        if count >= self.menang:
            self.win(currentOccupant, winnerList)
            return
        winnerList = [index] #untuk menandai tile yang membantu menang
        #==============diagonal kiri ke atas===============#
        idx = index - self.kolom - 1
        count = 1
        while((idx % self.kolom < index % self.kolom) and count < self.menang and idx >= 0):
            if self.tileObjList[idx].getOccupant() != currentOccupant:
                break
            count += 1
            winnerList.append(idx)
            idx -= (self.kolom + 1)
        #==============diagonal kanan ke bawah===============#
        idx = index + self.kolom + 1
        while((idx % self.kolom > index % self.kolom) and count < self.menang and idx < (self.kolom*self.baris)):
            if self.tileObjList[idx].getOccupant() != currentOccupant:
                break
            count += 1
            winnerList.append(idx)
            idx += self.kolom + 1
        if count >= self.menang:
            self.win(currentOccupant, winnerList)
            return
        winnerList = [index] #untuk menandai tile yang membantu menang
        #==============diagonal kanan ke atas===============#
        idx = index - self.kolom + 1
        count = 1
        while((idx % self.kolom > index % self.kolom) and count < self.menang and idx >= 0):
            if self.tileObjList[idx].getOccupant() != currentOccupant:
                break
            count += 1
            winnerList.append(idx)
            idx = idx - self.kolom + 1
        #==============diagonal kiri ke bawah===============#
        idx = index + self.kolom - 1
        while((idx % self.kolom < index % self.kolom) and count < self.menang and idx < (self.kolom*self.baris)):
            if self.tileObjList[idx].getOccupant() != currentOccupant:
                break
            count += 1
            winnerList.append(idx)
            idx = idx + self.kolom - 1
        if count >= self.menang:
            self.win(currentOccupant, winnerList)
            return
        if self.countOccupied >= self.baris * self.kolom: #tidak ada pemenang
            self.hasWinner = True
            self.winner = -1
            self.setHelperText('Tidak ada yang menang!')
            if self.hasEventOnWin:
                self.eventOnWin()

    def win(self, winnerId, winnerList):
        '''Menghentikan kerja evaluator jika sudah menang
        Menandai tiles yang bertanggung jawab untuk memenangkan game'''
        self.hasWinner = True
        self.winner = winnerId
        if winnerId == 1:
            winnerName = self.p1Name
        else:
            winnerName = self.p2Name
        if self.hasEventHelperChange:
            self.setHelperText('{} Menang!'.format(winnerName))
        for index in winnerList:
            self.tileObjList[index].markWinner()
        if self.hasEventOnWin:
            self.eventOnWin()

    def getTilesOccupantList(self):
        '''Mereturn list yang berisikan integer yang merepresentasikan 'tile 1 diambil oleh player 1'
        Berguna untuk save game'''
        lisTileOccupant = []
        for tiles in self.tileObjList:
            lisTileOccupant.append(tiles.getOccupant())
        return lisTileOccupant

    def getCurrentTurn(self):
        '''Mengembalikan nilai variabel giliran untuk savegame'''
        return self.turn

    def getWinnerId(self):
        '''Mengembalikan kode pemenang untuk savegame; 0:belum ada; 1:player1; 2:player2; -1:seri'''
        return self.winner

    def getLastOccupiedTile(self):
        '''Mengembalikan index tile yang terakhir kali diambil alih, berguna untuk savegame'''
        return self.lastOccupiedTileIndex

    def continueFromSavedPoint(self, tileOccupants, turn, lastOccupiedTileIndex, winner):
        '''Mengaktifkan tile yang sudah diambil alih setelah load game'''
        for i in range(len(self.tileObjList)):
            if tileOccupants[i] == 1:
                self.tileObjList[i].occupy(1)
            elif tileOccupants[i] == 2:
                self.tileObjList[i].occupy(2)
        self.turn = turn
        if winner == -1:
            self.hasWinner = True
            self.setHelperText('Tidak ada yang menang!')
            if self.hasEventOnWin:
                self.eventOnWin()
        else:
            self.updateHelper()
            self.evaluate(lastOccupiedTileIndex)
