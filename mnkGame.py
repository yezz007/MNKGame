from tkinter import *
from BoardStandard import *
from BoardDark import *
from GameLogic import *
from GoodButton import *
from tkinter import messagebox


class MNKGame:

    def __init__(self, screenWidth, screenHeight):
        self.window = Tk()
        self.window.title("MNK Game")
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.showMenu()
        self.fixWindowSize()
        self.logic = GameLogic()
        self.count = 1
        self.window.mainloop()

    def fixWindowSize(self):
        self.window.minsize(width=640, height=480)
        self.window.maxsize(width=640, height=480)

    def showMenu(self):
        print("Menu shown")
        self.menuFrame = Frame(self.window)
        self.menuFrame.pack(padx=5, pady=5)
        self.quickStartButton = GoodButton(self.menuFrame, text='Mulai Permainan', command=self.quickStartGame)
        self.quickStartButton.pack(padx=5, pady=5)
        self.setUpButton = GoodButton(self.menuFrame, text='Atur Permainan', command=self.showSetUpMenu)
        self.setUpButton.pack(padx=5, pady=5)

    def showSetUpMenu(self):
        self.hideMenu()
        self.setUpFrame = Frame(self.window)
        self.setUpFrame.pack(padx=5, pady=5)
        spinboxFrame = Frame(self.setUpFrame)
        spinboxFrame.pack(padx=5, pady=5)
        themeFrame = Frame(self.setUpFrame)
        themeFrame.pack(padx=5, pady=5)
        self.m = IntVar() #kolom
        self.n = IntVar() #baris
        self.k = IntVar() #menang
        self.theme = IntVar()
        self.tileId = IntVar()
        lbBaris = Label(spinboxFrame, text = 'Baris : ', font = 'Helvetica 14')
        lbKolom = Label(spinboxFrame, text = 'Kolom : ', font = 'Helvetica 14')
        lbMenang = Label(spinboxFrame, text = 'Menang : ', font = 'Helvetica 14')
        sbBaris = Spinbox(spinboxFrame, textvariable=self.n, font='Helvetica 14', from_=3, to=50)
        sbKolom = Spinbox(spinboxFrame, textvariable=self.m, font='Helvetica 14', from_=3, to=50)
        sbMenang = Spinbox(spinboxFrame, textvariable=self.k, font='Helvetica 14', from_=3, to=50)
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
        sbBaris.grid(padx=5, pady=5, row=0, column=1)
        lbKolom.grid(padx=5, pady=5, row=1, column=0, sticky=E)
        sbKolom.grid(padx=5, pady=5, row=1, column=1)
        lbMenang.grid(padx=5, pady=5, row=2, column=0, sticky=E)
        sbMenang.grid(padx=5, pady=5, row=2, column=1)
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
        btBright.select()
        btColor.select()

    def quickStartGame(self):
        self.startGame(5, 5, (self.screenHeight-120)//5, 0, 5, 1, 2)

    def setUpCancel(self):
        self.setUpFrame.destroy()
        self.showMenu()

    def setUpFinish(self):
        try:
            baris = self.n.get()
            kolom = self.m.get()
            menang = self.k.get()
            theme = self.theme.get()
            tile = self.tileId.get()
        except:
            messagebox.showerror("Kesalahan Input", "Periksa kembali input yang Anda berikan!")
            return
        extend = 0
        if menang <= 1 or kolom <= 1 or baris <= 1: #Pasti pemain yang mendapatkan giliran pertama yang menang
            messagebox.showerror("Peraturan Kacau", "Periksa kembali input yang Anda berikan!")
            return
        elif menang <= 2 and kolom <= 2 and baris <= 2: #Pasti pemain yang mendapatkan giliran pertama yang menang
            messagebox.showinfo("Peraturan Lemah", "Sudah pasti pemain yang mendapatkan giliran pertama yang menang")
            return
        if kolom < menang and baris < menang:
            messagebox.showerror("Peraturan Kacau", "Permainan tidak dapat dimenangkan oleh siapa pun!")
            return
        if (kolom < menang) or (baris < menang):
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
            messagebox.showerror("Screen Problem", "Your monitor cannot fit the game :(")
            return
        self.startGame(baris, kolom, size, extend, menang, theme, tile)
        self.setUpFrame.destroy()

    def startGame(self, baris, kolom, size, extend, win, theme, tileModel):
        if theme == 1:
            self.board = BoardStandard(self.window, self.logic, baris, kolom, win, extend, tileModel, size, onEndGame=self.endGame)
        else:
            self.board = BoardDark(self.window, self.logic, baris, kolom, win, extend, tileModel, size, onEndGame=self.endGame)
        self.window.minsize(width=(kolom*size)+12+extend, height=(baris*size)+42)
        self.window.maxsize(width=(kolom*size)+12+extend, height=(baris*size)+42)
        self.count += 1
        self.hideMenu()

    def endGame(self):
        self.board.destroy()
        print("Board Destroyed")
        self.fixWindowSize()
        self.showMenu()

    def hideMenu(self):
        self.menuFrame.destroy()
