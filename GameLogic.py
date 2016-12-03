from tkinter import *
from BoardStandard import *
from BoardDark import *
from TileStandard import *

class GameLogic:
    def __init__(self, board):
        self.board = board
        self.tileList = board.getTilesList()
        self.canvas = board.getCanvasHandler()
        self.setupTileEvent()

    def setupTileEvent(self):
        for tiles in self.tileList:
