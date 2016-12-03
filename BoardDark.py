from tkinter import *
from BoardStandard import *

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
