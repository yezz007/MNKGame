from tkinter import *

class TileStandard:
    '''
    Class yang mengendalikan kotak-kotak kecil di papan
    '''

    def __init__(self, canvas, xpos, ypos, size, neutralFill, outline, p1Color, p2Color, **kwargs):
        '''
        canvas = canvas tempat kotaknya
        xpos = koordinat x
        ypos = koordinat y
        size = ukuran kotaknya
        neutralFill = warna kotak ketika Netral
        outline = Garis pinggir
        p1Color = warna marker p1
        p2Color = warna marker p2
        **kwargs yang berlaku => command = method yang dipanggil ketika kotak diklik
        '''
        self.canvas = canvas
        self.xpos = xpos
        self.ypos = ypos
        self.size = size
        self.neutralFill = neutralFill
        print(neutralFill)
        self.outline = outline
        self.p1Color = p1Color
        self.p2Color = p2Color
        self.id = self.canvas.create_rectangle(self.xpos, self.ypos, self.xpos+self.size,
        self.ypos+self.size, fill=self.neutralFill, outline=self.outline, width=2.0)
        self.canvas.tag_bind(self.id, "<Button-1>", self.onClick)
        self.occupant = 0 # 0 Netral, 1 P1, 2 P2
        #fungsi yang akan dipanggil jika tile diklik
        self.hasCommand = False
        if 'command' in kwargs:
            self.hasCommand = True
            self.command = kwargs['command']
        self.flag = 99999999 #untuk menandai tile mana yang memenangkan permainan

    def getFlag(self):
        '''
        Mengambil nilai penanda
        Untuk menandai pemenang gunanya
        '''
        return self.flag

    def setFlag(self, intFlag):
        '''
        Memberi nilai flag
        '''
        self.flag = intFlag

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

    def markWinner(self):
        markSize = self.size // 3
        markX = (self.xpos + markSize)
        markY = (self.ypos + markSize)
        self.canvas.create_oval(markX, markY,
        markX + markSize, markY + markSize, fill=self.neutralFill)

    def onClick(self, event):
        if self.hasCommand:
            self.command(self)
