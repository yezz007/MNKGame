from tkinter import *

class TileStandard:
    '''
    Class yang mengatur kotak-kotak kecil di papan
    '''

    def __init__(self, canvas, index, xpos, ypos, size, neutralFill, outline, p1Color, p2Color, **kwargs):
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
        self.index = index
        self.xpos = xpos
        self.ypos = ypos
        self.size = size
        self.neutralFill = neutralFill
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

    def getOccupant(self):
        '''Mengembalikan kode pemain yang mengambil alih tile'''
        return self.occupant

    def isOccupied(self):
        '''Mendeteksi apakah tile ini sudah diambil alih atau belum'''
        return (self.occupant != 0)

    def occupy(self, occupantId):
        '''Mengambil alih tile ini oleh occupantId'''
        if occupantId == 1:
            color = self.p1Color
            self.occupant = 1
        elif occupantId == 2:
            color = self.p2Color
            self.occupant = 2
        self.canvas.itemconfigure(self.id, fill=color)

    def markWinner(self):
        '''Menandai bahwa tile ini lah yang memenangkan permainan'''
        markSize = self.size // 3
        markX = (self.xpos + markSize)
        markY = (self.ypos + markSize)
        self.canvas.create_oval(markX, markY,
        markX + markSize, markY + markSize, fill=self.neutralFill)

    def onClick(self, event):
        '''Memanggil method yang sudah dipass ketika tile diklik'''
        if self.hasCommand:
            self.command(self.index)
