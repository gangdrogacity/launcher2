# -*- mode: python ; coding: utf-8 -*-

# WTF Modpack Launcher - PyInstaller Spec File per macOS
# Questo file contiene la configurazione per la compilazione dell'applicazione macOS

import os
from pathlib import Path

# Directory corrente
current_dir = Path(SPECPATH)

# Dati da includere nel build
added_files = []

# Aggiungi directory se esistono
data_dirs = ['fonts', 'authlib']
for dir_name in data_dirs:
    dir_path = current_dir / dir_name
    if dir_path.exists():
        added_files.append((str(dir_path), dir_name))

# Aggiungi file singoli se esistono
data_files = [
    'README.md',
    'requirements.txt',
    'launcher_version.txt'
]

for file_name in data_files:
    file_path = current_dir / file_name
    if file_path.exists():
        added_files.append((str(file_path), '.'))

# Moduli nascosti da includere
hidden_imports = [
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'ttkbootstrap',
    'ttkbootstrap.style',
    'minecraft_launcher_lib',
    'minecraft_launcher_lib.forge',
    'minecraft_launcher_lib.command',
    'minecraft_launcher_lib.install',
    'minecraft_launcher_lib.utils',
    'requests',
    'psutil',
    'uuid',
    'platform',
    'json',
    'threading',
    'zipfile',
    'shutil',
    'time',
    'subprocess',
    'sys',
    'os',
    're'
]

# Configurazione analysis
a = Analysis(
    ['main.py'],
    pathex=[str(current_dir)],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Rimozione duplicati
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Configurazione eseguibile
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='WTF Modpack Launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Finestra console nascosta su macOS
    disable_windowed_traceback=False,
)

# Configurazione bundle per macOS
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WTF Modpack Launcher'
)

# Creazione app bundle per macOS
app = BUNDLE(
    coll,
    name='WTF Modpack Launcher.app',
    icon='icon.icns',  # Icona macOS
    bundle_identifier='com.wtfmodpack.launcher',
    version='1.0.0',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'Minecraft Profile',
                'CFBundleTypeIconFile': 'icon',
                'LSItemContentTypes': ['public.json'],
                'LSHandlerRank': 'Owner'
            }
        ]
    },
)
