# -*- mode: python -*-

import sys
sys.setrecursionlimit(5000)

block_cipher = None


a = Analysis(['photometryGUI.py'],
             pathex=['C:\\Users\\James Rig\\Documents\\GitHub\\Photometry-GUI'],
             binaries=[],
             datas=[],
             hiddenimports=['scipy._lib.messagestream'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='photometryGUI',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
