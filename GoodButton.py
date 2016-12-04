from tkinter import *

class GoodButton(Button):
    '''
    Tombol yang lebih baik daripada tombol biasa tkinter
    '''
    def __init__(self, parent, **kwargs):
        super().__init__(parent, kwargs)
        self.config(font='Helvetica 20 bold', relief='groove')
        self.bind("<Enter>", self.onMouseOver)
        self.bind("<Leave>", self.onMouseLeave)

    def onMouseOver(self, event):
        self.config(foreground='red')

    def onMouseLeave(self, event):
        self.config(foreground='black')
