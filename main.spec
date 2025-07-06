# -*- mode: python ; coding: utf-8 -*-

# WTF Modpack Launcher - PyInstaller Spec File
# Questo file contiene la configurazione per la compilazione dell'eseguibile

import os
from pathlib import Path

# Directory corrente
current_dir = Path(SPECPATH)

# Dati da includere nel build
added_files = []

# Aggiungi directory se esistono
data_dirs = ['fonts']
for dir_name in data_dirs:
    dir_path = current_dir / dir_name
    if dir_path.exists():
        added_files.append((str(dir_path), dir_name))

# Aggiungi file singoli se esistono
data_files = [
    'README.md',
    'requirements.txt',
    'icon.ico'
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
    'subprocess',
    'time',
    'os',
    'sys',
    'shutil',
    'zipfile',
    're'
]

# Analisi principale
a = Analysis(
    ['main.py'],
    pathex=[str(current_dir)],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'pandas',
        'scipy',
        'IPython',
        'jupyter'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Rimuovi duplicati
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Configurazione eseguibile
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WTF_Modpack_Launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Nasconde la console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if (current_dir / 'icon.ico').exists() else None,
    version_info={
        'version': '1.0.0',
        'description': 'WTF Modpack Launcher per Minecraft 1.20.1',
        'product_name': 'WTF Modpack Launcher',
        'product_version': '1.0.0',
        'file_version': '1.0.0',
        'company_name': 'WTF Modpack Team',
        'copyright': '2025 WTF Modpack Team'
    }
)
