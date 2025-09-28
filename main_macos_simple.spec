# -*- mode: python ; coding: utf-8 -*-

# WTF Modpack Launcher - PyInstaller Spec File per macOS (Semplificato)

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
    'launcher_version.txt',
    'icon.icns'
]

for file_name in data_files:
    file_path = current_dir / file_name
    if file_path.exists():
        added_files.append((str(file_path), '.'))

# Configurazione analysis
a = Analysis(
    ['main.py'],
    pathex=[str(current_dir)],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'ttkbootstrap',
        'minecraft_launcher_lib',
        'requests',
        'psutil',
        'uuid',
        'platform',
        'json',
        'threading',
        'zipfile',
        'shutil'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'scipy'],  # Escludi librerie pesanti non necessarie
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Rimozione duplicati
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Configurazione eseguibile - versione onedir per debug
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
    console=False,  # Nessuna console
    disable_windowed_traceback=False,
)

# Raccolta file
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

# Creazione app bundle per macOS - semplificato
app = BUNDLE(
    coll,
    name='WTF Modpack Launcher.app',
    icon='icon.icns',
    bundle_identifier='com.wtfmodpack.launcher',
    version='1.0.0',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.14.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
    },
)
