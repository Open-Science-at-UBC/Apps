# -*- mode: python -*-

block_cipher = None


a = Analysis(['LinkChecker.py'],
             pathex=['C:\\Users\\sharo\\eclipse-workspace\\Tkinter'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
             
             
a.datas += [ ('brokenChain.gif', '.\\brokenChain.gif', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='LinkChecker',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='brokenLink.ico')
