'''
Judul   : MNK Games
Nama    : Yudhistira Erlandinata
NPM     : 1606894534
Kelas   : DDP 1 B
Asisten : Kak Wira
'''

from MNKGame import * #game sesungguhnya
try:
    from win32api import GetSystemMetrics
    #Mendapatkan resolusi layar
    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)
except: #bukan sistem windows
    width = 800
    height = 600
MNKGame(width, height)
