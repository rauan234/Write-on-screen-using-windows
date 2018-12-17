import traceback
import tkinter
import _thread
import random
import time
import math
import sys
import os

try:
    from PIL import Image as img
except Exception:
    print('Python version: ' + sys.version)
    print()
    print('Error: ' + traceback.format_exc())
    print('Try to launch in IDE')
    input()
    sys.exit()


global ScreenSize
global FullWindowNumber
global WindowCreateDelay
global PictureDuration
global AfterDrawingDelay
global MinimalBrightness
###############
ScreenSize = 1000
FullWindowNumber = 200
WindowCreateDelay = 0.07
PictureDuration = 600
AfterDrawingDelay = True
MinimalBrightness = 600



def main():
    print('Program started')
    
    print()
    
    print('Start delay...')
    time.sleep(3)
    
    print()
    
    print('Reading picture started')
    Picture = Pictget()
    print('Reading picture finished')
    
    print()
    
    print('Processing picture started')
    Picture = Change(Picture)
    print('Processing picture finished')
    
    print()
    
    print('Compilling window list started')
    WindowList = Windowlist(Picture)
    print('Compilling window list finished')
    
    print()
    
    print('Dividing tasks started')
    TaskList = Tasklist(WindowList)
    print('Dividing tasks finished')
    
    print()
    
    print('Creating file list started')
    FileList = Filelist(TaskList)
    print('Creating file list finished')
    
    print()
    
    print('Writing and launching files started')
    Writefiles(FileList)
    print('Writing and launching files finished')
    
    print('Program finished')
    
def Change(Picture):
    return Picture
    
    
    
def Pictget():
    image = img.open('Picture.jpg')
    pixels = image.load()
    xmax, ymax = image.size
    
    out = list(map(lambda a: [None] * ymax, [None] * xmax))
     
    for x in range(xmax):  
        for y in range(ymax):
            out[x][y] = sum(pixels[x, y])
    
    return out

def Windowlist(picture):
    out = []
    
    wnumber = 0
    for x in range(len(picture)):
        for y in range(len(picture[x])):
            if(picture[x][y] <= MinimalBrightness):
                wnumber += 1
    
    rdelta = round(math.sqrt(wnumber / FullWindowNumber))
    if(rdelta == 0):
        rdelta = 1
    
    step = ScreenSize / len(picture)
    for x in range(len(picture)):
        for y in range(len(picture[x])):
            if(picture[x][y] <= MinimalBrightness):
                if((x % rdelta == 0) and (y % rdelta == 0)):
                    out.append((int(step * x), int(step * y)))
    
    return out

def Tasklist(wlist):
    return wlist

def Filelist(tlist):
    out = []
    
    for window in tlist:
        code = '''from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

import sys

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = ''
        self.left = 0
        self.top = 0
        self.width = 0
        self.height = 0

        self.move(''' + str(window[0]) + ',' + str(window[1]) + ''')
 
        self.show()

app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())

os.remove(__file__)'''
        out.append(code)
    
    return out

def Writefiles(flist):
    for file_id in range(len(flist)):
        name = 'Executor' + str(file_id) + '.pyw'
        vbs = 'Launcher' + str(file_id) + '.vbs'
        
        launcher = ''
        launcher += 'Set obj = WScript.CreateObject("WScript.Shell")' + '\n'
        launcher += 'Set fso = CreateObject("Scripting.FileSystemObject")' + '\n'
        launcher += 'obj.run '
        launcher += ('"' + '\\'.join(__file__.replace('/', '\\').split('\\')[:-1]) + '\\'+ name + '"') + '\n'
        launcher += ('fso.DeleteFile "' + ('\\'.join(__file__.replace('/', '\\').split('\\')[:-1]) + '\\'+ vbs) + '"') + '\n'
        
        open(name, 'w').write(flist[file_id])
        open(vbs, 'w').write(launcher)
        os.system('\\'.join(__file__.replace('/', '\\').split('\\')[:-1]) + '\\'+ vbs)
        
        if(AfterDrawingDelay):
            time.sleep(WindowCreateDelay)
    
    
    
    
try:
    main()
except Exception:
    print(traceback.format_exc())
    input()
