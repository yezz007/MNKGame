'''
Bagian untuk menyimpan dan memuat game
Tidak ada class di sini, karena tidak ada rencana untuk meng-inherit GameLoader
'''

def loadSettings():
    try:
        settingFile = open("saveGame.mnk", 'r')
    except:
        #Sebagai tanda bahwa telah gagal untuk memuat settings
        return [3, 3, 3, 1, 2, 'Player 1', 'Player 2']
    dataLines = settingFile.read().split('\n')
    gameSettings = dataLines[0].split(';')
    return gameSettings

def saveSettings(baris=3, kolom=3, menang=3, theme=1, tileModel=2, p1='Player 1', p2='Player 2'):
    try:
        readSettingFile  = open("saveGame.mnk", 'r')
        dataLines = readSettingFile.read().split('\n')
        readSettingFile.close()
    except:
        dataLines = ['']
    try:
        writeSettingFile = open('saveGame.mnk', 'w')
    except:
        return False
    dataLines[0] = '{};{};{};{};{};{};{}'.format(baris, kolom, menang, theme, tileModel, p1, p2)
    for lines in dataLines:
        writeSettingFile.write(lines + '\n')
    writeSettingFile.close()
    return True

def saveGame(baris, kolom, menang, theme, tileModel, namaP1, namaP2, tileOccupyList, giliran, pemenang):
    '''
    Menyimpan permainan.
    Return False jika gagal, jika sukses return True
    '''
    try:
        appendSettingFile = open('saveGame.mnk', 'a')
    except:
        return False
    saveDataLine = '{};{};{};{};{};{};{};{};{};{}\n'.format(baris, kolom, menang,
    theme, tileModel, namaP1, namaP2, tileOccupyList, giliran, pemenang).replace('[', '').replace(']', '')
    appendSettingFile.write(saveDataLine)
    appendSettingFile.close()
    return True

def loadGame():
    '''
    Memuat Permainan
    Return False jika gagal, True jika sukses
    '''
    try:
        readSettingFile = open('saveGame.mnk', 'r')
    except:
        return False
    saveDataLines = readSettingFile.read().split('\n')
    savedGameList = []
    for line in saveDataLines:
        splitedStr = line.split(';')
        savedGameDataList = []
        for data in splitedStr:
            try:
                savedGameDataList.append(int(data))
            except ValueError:
                savedGameDataList.append(data)
        savedGameList.append(savedGameDataList)
    return savedGameList
