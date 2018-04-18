To make into executable

Open Anaconda prompt as admin (using pyinstaller 3.3.1 and python 3.6.4)

if not already installed, install pyinstaller (pip install pyinstaller)

Make spec file with required options

pyi-makespec --onefile photometryGUI.py

Edit .spec file to include:

(at beginning, after # -*- mode: python -*-)
import sys
sys.setrecursionlimit(5000)

and
    
(under a = Analysis...)

hiddenimports=['scipy._lib.messagestream']

make .exe file using:
    pyinstaller photometryGUI.spec
    
    
to add icon at later date, make .ico file and add this option to pyi-makespec command

    --icon=lickcalc-Icon.ico
