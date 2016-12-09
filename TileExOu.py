from tkinter import *
from TileStandard import *

class TileExOu(TileStandard):
    '''
    Versi X O dari tiles
    '''
    def __init__(self, canvas, index, xpos, ypos, size, neutralFill, outline, p1Color, p2Color, **kwargs):
        super().__init__(canvas, index, xpos, ypos, size, neutralFill, outline, p1Color, p2Color, **kwargs)

    #override
    def occupy(self, intOccupantId):
        if intOccupantId == 1:
            color = self.p1Color
            self.occupant = 1
            self.canvas.create_line(self.xpos, self.ypos, self.xpos+self.size, self.ypos+self.size,
            fill = color, width=5.0)
            self.canvas.create_line(self.xpos, self.ypos+self.size, self.xpos+self.size, self.ypos,
            fill = color, width=5.0)
        elif intOccupantId == 2:
            color = self.p2Color
            self.occupant = 2
            self.canvas.create_oval(self.xpos, self.ypos, self.xpos+self.size, self.ypos+self.size,
            fill = "", width=3.0, outline=color)

    #override
    def markWinner(self):
        markSize = self.size // 3
        markX = (self.xpos + markSize)
        markY = (self.ypos + markSize)
        self.canvas.create_oval(markX, markY,
        markX + markSize, markY + markSize, fill=self.outline)
