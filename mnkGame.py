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
        self.window.minsize(width=480, height=320)
        self.window.maxsize(width=480, height=320)

    def showMenu(self):
        print("Menu shown")
        self.menuFrame = Frame(self.window)
        self.menuFrame.pack(padx=5, pady=5)
        self.quickStartButton = GoodButton(self.menuFrame, text='Start a Game', command=self.quickStartGame)
        self.quickStartButton.pack(padx=5, pady=5)
        self.setUpButton = GoodButton(self.menuFrame, text='Set Up a Game', command=self.showSetUpMenu)
        self.setUpButton.pack(padx=5, pady=5)

    def showSetUpMenu(self):
        self.hideMenu()
        self.setUpFrame = Frame(self.window)
        self.setUpFrame.pack(padx=5, pady=5)
        self.spinboxFrame = Frame(self.setUpFrame)
        self.spinboxFrame.pack(padx=5, pady=5)
        self.m = IntVar() #kolom
        self.n = IntVar() #baris
        self.k = IntVar() #menang
        self.dark = IntVar()
        self.lbBaris = Label(self.spinboxFrame, text = 'Row : ', font = 'Helvetica 14')
        self.lbKolom = Label(self.spinboxFrame, text = 'Column : ', font = 'Helvetica 14')
        self.lbMenang = Label(self.spinboxFrame, text = 'Win : ', font = 'Helvetica 14')
        self.sbBaris = Spinbox(self.spinboxFrame, textvariable=self.n, font='Helvetica 14', from_=2, to=50)
        self.sbKolom = Spinbox(self.spinboxFrame, textvariable=self.m, font='Helvetica 14', from_=2, to=50)
        self.sbMenang = Spinbox(self.spinboxFrame, textvariable=self.k, font='Helvetica 14', from_=2, to=50)
        self.btDark = Checkbutton(self.setUpFrame, variable=self.dark, onvalue=1, offvalue=0,
        text = 'Dark Mode ', font='Helvetica 14')
        self.lbBaris.grid(padx=5, pady=5, row=0, column=0)
        self.sbBaris.grid(padx=5, pady=5, row=0, column=1)
        self.lbKolom.grid(padx=5, pady=5, row=1, column=0)
        self.sbKolom.grid(padx=5, pady=5, row=1, column=1)
        self.lbMenang.grid(padx=5, pady=5, row=2, column=0)
        self.sbMenang.grid(padx=5, pady=5, row=2, column=1)
        self.btDark.pack(padx=5, pady=5)
        self.btSetUpStart = GoodButton(self.setUpFrame, text='Start', command=self.setUpFinish)
        self.btSetUpStart.pack(padx=5, pady=5)

    def quickStartGame(self):
        self.startGame(5, 5, 40, 0, 5, 0)

    def setUpFinish(self):
        baris = self.n.get()
        kolom = self.m.get()
        extend = 0
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
        self.startGame(self.n.get(), self.m.get(), size, extend, self.k.get(), self.dark.get())
        self.setUpFrame.destroy()

    def startGame(self, baris, kolom, size, extend, win, dark):
        if dark == 0:
            self.board = BoardStandard(self.window, self.logic, baris, kolom, win, extend, size, onEndGame=self.endGame)
        else:
            self.board = BoardDark(self.window, self.logic, baris, kolom, win, extend, size, onEndGame=self.endGame)
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
