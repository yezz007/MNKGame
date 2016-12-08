from tkinter import *
from BoardStandard import *
from BoardDark import *
from GameLogic import *
from GoodButton import *
from tkinter import messagebox
import GameLoader

class MNKGame:
    '''
    Kelas yang mengatur menu utama, save dan load game, instansiasi objek logika permainan
    '''

    def __init__(self, screenWidth, screenHeight):
        '''
        Constructor
        Semua atribut kelas terlihat di sini
        '''
        self.window = Tk()
        self.window.title("MNK Game")
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.fixWindowSize()
        self.m = IntVar() #kolom
        self.n = IntVar() #baris
        self.k = IntVar() #menang
        self.theme = IntVar()
        self.tileId = IntVar()
        self.namaP1 = StringVar()
        self.namaP2 = StringVar()
        self.namaP1.set("Player 1")
        self.namaP2.set("Player 2")
        self.loadSettings()
        self.showMenu()
        self.logic = GameLogic()
        self.window.mainloop()

    def loadSettings(self):
        '''
        Memuat settings sebelumnya, supaya user tidak perlu repot-repot lagi :)
        '''
        dataList = GameLoader.loadSettings()
        self.n.set(dataList[0])
        self.m.set(dataList[1])
        self.k.set(dataList[2])
        self.theme.set(dataList[3])
        self.tileId.set(dataList[4])
        self.namaP1.set(dataList[5])
        self.namaP2.set(dataList[6])


    def fixWindowSize(self):
        '''
        Mengatur ukuran window
        '''
        self.window.minsize(width=800, height=600)
        self.window.maxsize(width=800, height=600)

    def showMenu(self):
        '''
        Menampilkan menu utama
        '''
        print("Menu shown")
        self.menuFrame = Frame(self.window)
        self.menuFrame.pack(padx=5, pady=100)
        self.loadGameButton = GoodButton(self.menuFrame, text='Lanjutkan Permainan', command=self.showLoadGameMenu)
        self.loadGameButton.pack(padx=5, pady=5)
        self.quickStartButton = GoodButton(self.menuFrame, text='Mulai Permainan Baru', command=self.quickStartGame)
        self.quickStartButton.pack(padx=5, pady=5)
        self.setUpButton = GoodButton(self.menuFrame, text='Atur Permainan Baru', command=self.showSetUpMenu)
        self.setUpButton.pack(padx=5, pady=5)

    def showLoadGameMenu(self):
        self.games = []
        self.chooseGame = IntVar()
        savedGameList = GameLoader.loadGame()
        self.hideMenu()
        self.loadFrame = Frame(self.window)
        self.loadFrame.pack(padx=5, pady=5)
        savedGames = 0
        print(len(savedGameList))
        for i in range(len(savedGameList)-1, 0, -1):
            if savedGames >= 10:
                messagebox.showinfo("Terlalu Banyak Permainan Tersimpan", "Kami Hanya Menampilkan 10 Permainan Terkini")
                break
            if len(savedGameList[i]) == 10:
                self.games.append(savedGameList[i])
                p1Name = savedGameList[i][5]
                p2Name = savedGameList[i][6]
                pemenang = 'Belum Ada'
                if savedGameList[i][9] == 1:
                    pemenang = p1Name
                elif savedGameList[i][9] == 2:
                    pemenang = p2Name
                Radiobutton(self.loadFrame, font='Helvetica 16', value=savedGames,
                variable=self.chooseGame, text='{} vs {} - Pemenang = {}'.format(p1Name, p2Name, pemenang)).pack(padx=5, pady=5, anchor=W)
                savedGames += 1
            else:
                print('Not a valid game data')
        GoodButton(self.loadFrame, text='Lanjutkan Permainan', command=self.playSavedGame).pack(padx=5, pady=5)
        GoodButton(self.loadFrame, text='Kembali', command=self.hideLoadGameMenu).pack(padx=5, pady=5)

    def hideLoadGameMenu(self):
        self.loadFrame.destroy()
        self.showMenu()

    def playSavedGame(self):
        self.loadFrame.destroy()
        print(self.games)
        gameId = self.chooseGame.get()
        baris = self.games[gameId][0]
        kolom = self.games[gameId][1]
        menang = self.games[gameId][2]
        theme = self.games[gameId][3]
        tileModel = self.games[gameId][4]
        namaP1 = self.games[gameId][5]
        namaP2 = self.games[gameId][6]
        size1 = (self.screenHeight - 120) // baris
        size2 = (self.screenWidth - 120) // kolom
        extend = 0 #blank space canvas, supaya tulisan muat
        if size1 > size2:
            size = size2
        else:
            size = size1
        if size*kolom < 200:
            extend = 200
        self.startGame(baris, kolom, size, extend, menang, theme, tileModel, namaP1, namaP2)
        tileOccupantStr = self.games[gameId][7].split(',')
        tileOccupantList = []
        turn = self.games[gameId][-2]
        for char in tileOccupantStr:
            tileOccupantList.append(int(char))
        self.logic.continueFromSavedPoint(tileOccupantList, turn)
        self.n.set(baris)
        self.m.set(kolom)
        self.theme.set(theme)
        self.k.set(menang)
        self.tileId.set(tileModel)
        self.namaP1.set(namaP1)
        self.namaP2.set(namaP2)


    def quickStartGame(self):
        '''
        Langsung memulai permainan,
        User tidak perlu repot-repot klik ini itu, LANGSUNG main
        *Menggunakan settings sebelumnya untuk pengalaman user yang lebih baik
        '''
        size1 = (self.screenHeight - 120) // (self.n.get())
        size2 = (self.screenWidth - 120) // (self.m.get())
        extend = 0 #blank space canvas, supaya tulisan muat
        if size1 > size2:
            size = size2
        else:
            size = size1
        if size*self.m.get() < 200:
            extend = 200
        if len(self.namaP1.get()) >= 10:
            self.namaP1.set("Player 1")
        if len(self.namaP2.get()) >= 10:
            self.namaP2.set("Player 1")
        self.hideMenu()
        self.startGame(self.n.get(), self.m.get(), size, extend, self.k.get(),
        self.theme.get(), self.tileId.get(), self.namaP1.get(), self.namaP2.get())

    def showSetUpMenu(self):
        '''
        Menampilkan menu untuk mengatur banyaknya baris dan kolom serta nilai 'k' untuk menang
        '''
        self.hideMenu()
        self.setUpFrame = Frame(self.window)
        self.setUpFrame.pack(padx=5, pady=5)
        spinboxFrame = Frame(self.setUpFrame)
        spinboxFrame.pack(padx=5, pady=5)
        themeFrame = Frame(self.setUpFrame)
        themeFrame.pack(padx=5, pady=5)
        lbBaris = Label(spinboxFrame, text = 'Baris : ', font = 'Helvetica 14')
        lbKolom = Label(spinboxFrame, text = 'Kolom : ', font = 'Helvetica 14')
        lbMenang = Label(spinboxFrame, text = 'Menang : ', font = 'Helvetica 14')
        lbNamaP1 = Label(spinboxFrame, text = 'Nama P1 : ', font = 'Helvetica 14')
        lbNamaP2 = Label(spinboxFrame, text = 'Nama P2 : ', font = 'Helvetica 14')
        sbBaris = Spinbox(spinboxFrame, textvariable=self.n, font='Helvetica 14', from_=3, to=50)
        sbKolom = Spinbox(spinboxFrame, textvariable=self.m, font='Helvetica 14', from_=3, to=50)
        sbMenang = Spinbox(spinboxFrame, textvariable=self.k, font='Helvetica 14', from_=3, to=50)
        enNamaP1 = Entry(spinboxFrame, textvariable=self.namaP1, font='Helvetica 14')
        enNamaP2 = Entry(spinboxFrame, textvariable=self.namaP2, font='Helvetica 14')
        lbTemaPapan = Label(themeFrame, text='Tema Papan', font='Helvetica 14')
        lbTileModel = Label(themeFrame, text='Model Kotak Kecil', font='Helvetica 14')
        btBright = Radiobutton(themeFrame, variable=self.theme, value=1,
        text = 'Papan Cerah ', font='Helvetica 12', cursor='hand2')
        btDark = Radiobutton(themeFrame, variable=self.theme, value=2,
        text = 'Papan Gelap ', font='Helvetica 12', cursor='hand2')
        btColor = Radiobutton(themeFrame, variable=self.tileId, value=1,
        text = 'Warna Solid ', font='Helvetica 12', cursor='hand2')
        btExOu = Radiobutton(themeFrame, variable=self.tileId, value=2,
        text = 'X dan O ', font='Helvetica 12', cursor='hand2')
        btCoin = Radiobutton(themeFrame, variable=self.tileId, value=3,
        text = 'Koin ', font='Helvetica 12', cursor='hand2')
        lbBaris.grid(padx=5, pady=5, row=0, column=0, sticky=E)
        sbBaris.grid(padx=5, pady=5, row=0, column=1, sticky=W)
        lbKolom.grid(padx=5, pady=5, row=1, column=0, sticky=E)
        sbKolom.grid(padx=5, pady=5, row=1, column=1, sticky=W)
        lbMenang.grid(padx=5, pady=5, row=2, column=0, sticky=E)
        sbMenang.grid(padx=5, pady=5, row=2, column=1, sticky=W)
        lbNamaP1.grid(padx=5, pady=5, row=3, column=0, sticky=E)
        enNamaP1.grid(padx=5, pady=5, row=3, column=1, sticky=W)
        lbNamaP2.grid(padx=5, pady=5, row=4, column=0, sticky=E)
        enNamaP2.grid(padx=5, pady=5, row=4, column=1, sticky=W)
        lbTemaPapan.grid(padx=5, pady=5, row=0, column=0, sticky=E)
        btBright.grid(padx=5, pady=5, row=1, column=0, sticky=W)
        btDark.grid(padx=5, pady=5, row=2, column=0, sticky=W)
        lbTileModel.grid(padx=5, pady=5, row=0, column=1, sticky=W)
        btColor.grid(padx=5, pady=5, row=1, column=1, sticky=W)
        btExOu.grid(padx=5, pady=5, row=2, column=1, sticky=W)
        btCoin.grid(padx=5, pady=5, row=3, column=1, sticky=W)
        btSetUpStart = GoodButton(self.setUpFrame, text='Mulai Permainan', command=self.setUpFinish)
        btBack = GoodButton(self.setUpFrame, text='Kembali', command=self.setUpCancel)
        btSetUpStart.pack(padx=5, pady=5)
        btBack.pack(padx=5, pady=3)
        if self.theme.get() == 1:
            btBright.select()
        else:
            btDark.select()
        if self.tileId.get() == 1:
            btColor.select()
        elif self.tileId.get() == 2:
            btExOu.select()
        else:
            btCoin.select()

    def setUpCancel(self):
        '''
        Membatalkan set up game dan kembali ke menu utama
        '''
        self.setUpFrame.destroy()
        self.showMenu()

    def setUpFinish(self):
        '''
        Memproses input sebelum memulai permainan
        Ada kasus dimana input user Kacau
        Ada juga kasus dimana jumlah baris dan kolom terlalu besar sehingga layar tidak muat
        Di sini kasus-kasus yang tidak diinginkan ditangani terlebih dahulu
        '''
        try:
            baris = self.n.get()
            kolom = self.m.get()
            menang = self.k.get()
            theme = self.theme.get()
            tile = self.tileId.get()
            namaP1 = self.namaP1.get()
            namaP2 = self.namaP2.get()
        except:
            messagebox.showerror("Kesalahan Input", "Periksa kembali input yang Anda berikan!")
            return
        extend = 0 #blank space canvas, supaya tulisan muat
        if menang <= 1 or kolom <= 1 or baris <= 1: #Input aneh
            messagebox.showerror("Peraturan Kacau", "Periksa kembali input yang Anda berikan!")
            return
        elif menang <= 2 and kolom <= 2 and baris <= 2: #Pasti pemain yang mendapatkan giliran pertama yang menang
            messagebox.showinfo("Peraturan Lemah", "Sudah pasti pemain yang mendapatkan giliran pertama yang menang")
            return
        if kolom < menang and baris < menang: #Ini yang paling kacau, tidak perlu main kalau begini
            messagebox.showerror("Peraturan Kacau", "Permainan tidak dapat dimenangkan oleh siapa pun!")
            return
        if (kolom < menang) or (baris < menang): #hanya Mengingatkan user
            messagebox.showwarning("Hanya Mengingatkan", "Permainan tidak mungkin dimenangkan dengan cara menguasai kotak-kotak secara diagonal.")
        size1 = (self.screenHeight - 120) // (baris)
        size2 = (self.screenWidth - 120) // (kolom)
        if size1 > size2:
            size = size2
        else:
            size = size1
        if size*kolom < 200:
            extend = 200
        if size < 25:
            messagebox.showerror("Layar Tidak Muat", "Layar monitor kamu tidak muat untuk memainkan game dengan setting ini :(")
            return
        #validasi nama
        if (len(namaP1) > 10) or (len(namaP2) > 10):
            messagebox.showerror("Layar Tidak Muat", "Layar monitor kamu tidak muat untuk memunculkan nama yang kamu masukkan :(")
            return
        self.startGame(baris, kolom, size, extend, menang, theme, tile, namaP1, namaP2)
        self.setUpFrame.destroy()
        self.saveSettings(baris, kolom, menang, theme, tile, namaP1, namaP2)

    def saveSettings(self, baris, kolom, menang, theme, tileModel, namaP1, namaP2):
        '''
        Menyimpan settings agar kedepannya user tidak perlu banyak klik
        '''
        GameLoader.saveSettings(baris, kolom, menang, theme, tileModel, namaP1, namaP2)

    def startGame(self, baris, kolom, size, extend, win, theme, tileModel, namaP1, namaP2):
        '''
        Mulai permainannya di sini, memilih papan juga di sini
        '''
        #memastikan window ada di paling atas
        self.window.geometry("{}x{}+{}+{}".format(self.screenWidth, self.screenHeight, 0, 0))
        if theme == 1:
            self.board = BoardStandard(self.window, self.logic, baris, kolom, win, extend,
            tileModel, size, eventOnEndGame=self.endGame, p1Name=namaP1, p2Name=namaP2, eventOnSaveGame=self.onSaveGame)
        else:
            self.board = BoardDark(self.window, self.logic, baris, kolom, win, extend,
            tileModel, size, eventOnEndGame=self.endGame, p1Name=namaP1, p2Name=namaP2, eventOnSaveGame=self.onSaveGame)
        self.window.minsize(width=(kolom*size)+12+extend, height=(baris*size)+42)
        self.window.maxsize(width=(kolom*size)+12+extend, height=(baris*size)+42)

    def onSaveGame(self):
        tileList = self.logic.getTilesOccupantList()
        turn = self.logic.getCurrentTurn()
        pemenang = self.logic.getWinnerId()
        isSaveSuccess = GameLoader.saveGame(self.n.get(), self.m.get(), self.k.get(),
        self.theme.get(), self.tileId.get(), self.namaP1.get(), self.namaP2.get(), tileList, turn, pemenang)
        if isSaveSuccess:
            messagebox.showinfo("Permainan Berhasil Disimpan", "Permainan ini telah berhasil disimpan")
        else:
            messagebox.showinfo("Permainan Gagal Disimpan", "Kami tidak bisa menyimpan permainan ini :(")

    def endGame(self):
        '''
        Akhir permainan dipicu oleh event yang diatur oleh kelas papan permainan
        '''
        self.board.destroy()
        print("Board Destroyed")
        self.fixWindowSize()
        self.showMenu()

    def hideMenu(self):
        '''
        Menyembunyikan menu utama
        '''
        self.menuFrame.destroy()
