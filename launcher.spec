# -*- mode: python ; coding: utf-8 -*-

# WTF Modpack Launcher - PyInstaller Spec File Universale
# Supporta Windows e macOS automaticamente

import os
import platform
from pathlib import Path

# Rileva il sistema operativo
current_os = platform.system()
is_windows = current_os == "Windows"
is_macos = current_os == "Darwin"

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

# File da includere (comuni)
data_files = [
    'README.md',
    'requirements.txt',
    'launcher_version.txt'
]

# Aggiungi icona specifica per OS
if is_windows and (current_dir / 'icon.ico').exists():
    data_files.append('icon.ico')
elif is_macos and (current_dir / 'icon.icns').exists():
    data_files.append('icon.icns')

for file_name in data_files:
    file_path = current_dir / file_name
    if file_path.exists():
        added_files.append((str(file_path), '.'))

# Moduli nascosti da includere (comuni)
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
    console=False,  # Nasconde console su entrambe le piattaforme
    disable_windowed_traceback=False,
    icon='icon.ico' if is_windows else None,  # Icona Windows
)

# Configurazione COLLECT (comune)
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

# Configurazione specifica per macOS - crea app bundle
if is_macos:
    app = BUNDLE(
        coll,
        name='WTF Modpack Launcher.app',
        icon='icon.icns' if (current_dir / 'icon.icns').exists() else None,
        bundle_identifier='com.wtfmodpack.launcher',
        version='1.0.0',
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSAppleScriptEnabled': False,
            'NSHighResolutionCapable': True,
            'LSUIElement': False,
            'LSBackgroundOnly': False,
            'LSRequiresNativeExecution': True,
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
