from tkinter import *
from BoardStandard import *

class BoardDark(BoardStandard):
    '''
    Tema gelap dari papan permainan
    '''
    def __init__(self, parent, logic, baris, kolom, menang, extend, squareSize=50, **kwargs):
        super().__init__(parent, logic, baris, kolom, menang, extend, squareSize, **kwargs)

    #override
    def setColors(self):
        self.borderColor = 'white'
        self.neutralColor = 'black'
        self.squareBorder = 'white'
        self.p1Color = 'yellow'
        self.p2Color = 'pink'
