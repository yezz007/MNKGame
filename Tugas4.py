'''
Judul   : MNK Games
Nama    : Yudhistira Erlandinata
NPM     : 1606894534
Kelas   : DDP 1 B
Asisten : Kak Wira
'''

from MNKGame import *
try:
    from win32api import GetSystemMetrics
    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)
except:
    print("Cannot load win32api")
    width = 640
    heigth = 480
MNKGame(width, height)
