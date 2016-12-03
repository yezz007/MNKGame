from tkinter import *

class TileStandard:

    staticIntTurn = 1 # a static attribute, you know what it means. 1 = P1. 2 = P2

    def __init__(self, canvas, xpos, ypos, size, neutralFill, outline, p1Color, p2Color, **kwargs):
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
        #fungsi yang akan dipanggil jika tile diklik
        self.hasCommand = False
        if 'command' in kwargs:
            self.hasCommand = True
            self.command = kwargs['command']


    def getId(self):
        return self.id

    def getOccupant(self):
        return self.occupant

    def isOccupied(self):
        return (self.occupant != 0)

    def occupy(self, intOccupantId):
        if intOccupantId == 1:
            color = self.p1Color
            self.occupant = 1
        elif intOccupantId == 2:
            color = self.p2Color
            self.occupant = 2
        self.canvas.itemconfigure(self.id, fill=color)

    def onClick(self, event):
        print(self.id)
        if not self.isOccupied():
            if TileStandard.staticIntTurn == 1:
                occupantId = 1
                TileStandard.staticIntTurn = 2
            else:
                TileStandard.staticIntTurn = 1
                occupantId = 2
            self.occupy(occupantId)
            self.eventOnClick()

    def eventOnClick(self):
        if self.hasCommand:
            self.command()
