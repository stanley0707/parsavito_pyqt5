# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['./env/lib/python3.7/site-packages/PyQt5/Qt/bin', '/Users/machd/Desktop/time/property_parser/proparser'],
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
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Parser-Avito',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='Parser-Avito.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Parser-Avito')
app = BUNDLE(coll,
             name='Parser-Avito.app',
             icon='Parser-Avito.icns',
             bundle_identifier=None)
