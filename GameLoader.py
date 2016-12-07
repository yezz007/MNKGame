'''
Bagian untuk menyimpan dan memuat game
Tidak ada class di sini, karena tidak ada rencana untuk meng-inherit GameLoader
'''
import json

def loadSettings():
    try:
        settingFile = open("saveGame.mnk", 'r')
    except:
        return {'baris':3, 'kolom':3, 'menang':3, 'theme':1, 'tileModel':2,
        'namaP1':'Player 1', 'namaP2':'Player2'} #Sebagai tanda bahwa telah gagal untuk memuat settings
    dataLines = settingFile.read().split('\n')
    gameSettings = json.loads(dataLines[0]) #Setting Game ada di baris pertama
    return gameSettings

def saveSettings(baris=3, kolom=3, menang=3, theme=1, tileModel=2, p1='Player 1', p2='Player 2'):
    try:
        readSettingFile  = open("saveGame.mnk", 'r')
        dataLines = settingFile.read().split('\n')
        readSettingFile.close()
    except:
        dataLines = [{}]
    try:
        writeSettingFile = open('saveGame.mnk', 'w')
    except:
        return False
    dataLines[0] = json.dumps({'baris':baris, 'kolom':kolom, 'menang':menang,
    'theme':theme, 'tileModel':tileModel, 'namaP1':p1, 'namaP2':p2})
    for lines in dataLines:
        writeSettingFile.write(lines + '\n')
    writeSettingFile.close()
    return True

def saveGame(baris, kolom, menang, theme, tileModel, namaP1, namaP2, tileOccupyList, giliran):
    '''
    Menyimpan permainan.
    Return False jika gagal, jika sukses return True
    '''
    try:
        appendSettingFile = open('saveGame.mnk', 'a')
    except:
        return False
    saveData = json.dumps({'baris':baris, 'kolom':kolom, 'menang':menang,
    'theme':theme, 'tileModel':tileModel, 'namaP1':namaP1, 'namaP2':namaP2,
    'tileOccupyList':tileOccupyList, 'giliran':giliran})
    appendSettingFile.write(saveData)
    appendSettingFile.close()
    return True
