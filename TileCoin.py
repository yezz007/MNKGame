from tkinter import *
from TileStandard import *

class TileCoin(TileStandard):
    '''
    Versi X O dari tiles
    '''
    def __init__(self, canvas, index,  xpos, ypos, size, neutralFill, outline, p1Color, p2Color, **kwargs):
        super().__init__(canvas, index, xpos, ypos, size, neutralFill, outline, p1Color, p2Color, **kwargs)

    #override
    def occupy(self, intOccupantId):
        coinSize = self.size // 2
        coinX = (self.xpos + (coinSize // 2))
        coinY = (self.ypos + (coinSize // 2))
        if intOccupantId == 1:
            self.occupant = 1
            self.canvas.create_oval(coinX, coinY,
            coinX + coinSize, coinY + coinSize, fill=self.p1Color, outline=self.outline, width=5.0)
        elif intOccupantId == 2:
            self.occupant = 2
            self.canvas.create_oval(coinX, coinY,
            coinX + coinSize, coinY + coinSize, fill=self.p2Color, outline=self.outline, width=5.0)
