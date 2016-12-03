from tkinter import *
from BoardStandard import *
from BoardDark import *

class MNKGame:

    def __init__(self):
        self.window = Tk()
        self.window.title("MNK Game")
        self.showMenu()
        self.fixWindowSize()
        #test
        self.count = 1
        self.window.mainloop()

    def fixWindowSize(self):
        self.window.minsize(width=480, height=320)
        self.window.maxsize(width=480, height=320)

    def showMenu(self):
        print("Menu shown")
        self.menuFrame = Frame(self.window)
        self.menuFrame.pack(padx=5, pady=5)
        self.startButton = Button(self.menuFrame, text='Start Game', font='Helvetica 20 bold',
        command=self.startGame)
        self.startButton.pack()

    def startGame(self):
        baris = 7
        kolom = 7
        win = 5
        size = 40
        if self.count % 2 == 1:
            self.board = BoardStandard(self.window, baris, kolom, win, size)
        else:
            self.board = BoardDark(self.window, baris, kolom, win, size)
        self.window.minsize(width=(kolom*size)+10, height=(baris*size)+10)
        self.endButton = Button(self.board, text='End Game',
        font='Helvetica 16 bold', command=self.endGame)
        self.endButton.pack(padx=5, pady=5)
        self.count += 1
        self.hideMenu()

    def endGame(self):
        self.board.endGame()
        self.board.destroy()
        print("Board Destroyed")
        self.fixWindowSize()
        self.showMenu()

    def hideMenu(self):
        self.menuFrame.destroy()
