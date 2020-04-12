# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['__init__.py'],
             pathex=['D:\\Documents\\Documents\\UdM\\sms\\dev\\workplaces\\WBiBler\\BiBler-git\\src\\bibler'],
             binaries=[('utils\\resources\\*.ico', 'utils\\resources'), ('utils\\resources\\*.jpg', 'utils\\resources'), ('utils\\resources\\*.png', 'utils\\resources')],
             datas=[('utils\\resources\\*.html', 'utils\\resources'), ('utils\\resources\\*.md', 'utils\\resources'), ('external', 'external')],
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
          name='bibler',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='utils\\resources\\bibler.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='bibler')
