from tkinter import *

class SquareStandard:

    staticIntTurn = 1 # a static attribute, you know what it means. 1 = P1. 2 = P2

    def __init__(self, canvas, xpos, ypos, size, neutralFill, outline, p1Color, p2Color):
        self.canvas = canvas
        self.xpos = xpos
        self.ypos = ypos
        self.size = size
        self.neutralFill = neutralFill
        self.outline = outline
        self.p1Color = p1Color
        self.p2Color = p2Color
        self.id = self.canvas.create_rectangle(self.xpos, self.ypos, self.xpos+self.size,
        self.ypos+self.size, fill=self.neutralFill, outline=self.outline)
        self.canvas.tag_bind(self.id, "<Button-1>", self.onClick)
        self.occupant = 0 # 0 Netral, 1 P1, 2 P2

    def isOccupied(self):
        return (self.occupant != 0)

    def onClick(self, event):
        print(self.id)
        if not self.isOccupied():
            if SquareStandard.staticIntTurn == 1:
                color = self.p1Color
                self.occupant = 1
                SquareStandard.staticIntTurn = 2
            else:
                color = self.p2Color
                SquareStandard.staticIntTurn = 1
                self.occupant = 2
            self.canvas.itemconfigure(self.id, fill=color)


class BoardStandard:

    def __init__(self, parent, baris, kolom, menang, squareSize=50):
        self.parent = parent #passed by reference
        self.baris = baris
        self.kolom = kolom
        self.menang = menang
        self.size = squareSize
        self.setColors()
        self.canvas = Canvas(self.parent, bg=self.borderColor,
        width=(self.kolom*self.size)+10, height=(self.baris*self.size)+10)
        self.canvas.pack(padx=5, pady=5)
        self.squareObjList = [] #list berisikan objek kotak-kotak
        self.populateBoard()
        print("Board built")

    def setColors(self):
        self.borderColor = 'black'
        self.neutralColor = 'white'
        self.squareBorder = 'black'
        self.p1Color = 'blue'
        self.p2Color = 'red'

    def endGame(self):
        self.squareObjList.clear()
        self.canvas.delete("all")

    def populateBoard(self):
        x = 5
        y = 5
        for i in range(self.baris):
            x = 5
            for j in range(self.kolom):
                self.squareObjList.append(SquareStandard(self.canvas, x, y, self.size,
                self.neutralColor, self.squareBorder, self.p1Color, self.p2Color))
                x += self.size
            y += self.size

class BoardDark(BoardStandard):

    def __init__(self, parent, baris, kolom, menang, size=50):
        super().__init__(parent, baris, kolom, menang, size)

    #override
    def setColors(self):
        self.borderColor = 'white'
        self.neutralColor = 'black'
        self.squareBorder = 'white'
        self.p1Color = 'yellow'
        self.p2Color = 'pink'


class Game:

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
        self.menuFrame = Frame(self.window)
        self.menuFrame.pack(padx=5, pady=5)
        self.startButton = Button(self.menuFrame, text='Start Game', font='Helvetica 20 bold',
        command=self.startGame)
        self.startButton.pack()

    def startGame(self):
        self.boardFrame = Frame(self.window)
        self.boardFrame.pack()
        baris = 15
        kolom = 15
        win = 15
        size = 30
        if self.count % 2 == 1:
            self.board = BoardStandard(self.boardFrame, baris, kolom, win, size)
        else:
            self.board = BoardDark(self.boardFrame, baris, kolom, win, size)
        self.window.minsize(width=(kolom*size)+100, height=(baris*size)+100)
        self.endButton = Button(self.boardFrame, text='End Game',
        font='Helvetica 16 bold', command=self.endGame)
        self.endButton.pack()
        self.count += 1
        self.hideMenu()

    def endGame(self):
        self.board.endGame()
        self.boardFrame.destroy()
        self.fixWindowSize()
        self.showMenu()

    def hideMenu(self):
        self.menuFrame.destroy()

Game()
