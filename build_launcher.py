#!/usr/bin/env python3
"""
Script per creare l'eseguibile del WTF Modpack Launcher
Richiede PyInstaller: pip install pyinstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_executable():
    """Crea l'eseguibile del launcher"""
    print("🚀 Compilazione WTF Modpack Launcher in corso...")
    
    # Directory corrente
    current_dir = Path(__file__).parent
    
    # File principale
    main_script = current_dir / "wtf_launcher.py"
    if not main_script.exists():
        print("❌ File wtf_launcher.py non trovato!")
        return False
    
    # Directory di output
    dist_dir = current_dir / "dist"
    build_dir = current_dir / "build"
    
    # Pulisci directory precedenti
    if dist_dir.exists():
        print("🧹 Pulizia directory dist...")
        shutil.rmtree(dist_dir)
    
    if build_dir.exists():
        print("🧹 Pulizia directory build...")
        shutil.rmtree(build_dir)
    
    # Comando PyInstaller
    command = [
        "pyinstaller",
        "--onefile",                    # Un singolo file eseguibile
        "--windowed",                   # Nasconde la console
        "--name=WTF_Modpack_Launcher",  # Nome dell'eseguibile
        "--add-data=img;img",           # Includi cartella immagini
        "--add-data=fonts;fonts",       # Includi cartella font
        "--add-data=config;config",     # Includi cartella config
        "--add-data=README_WTF.md;.",   # Includi README
        "--add-data=requirements_wtf.txt;.",  # Includi requirements
        "--add-data=icon.ico;.",        # Includi icona nel bundle
        "--hidden-import=tkinter",
        "--hidden-import=ttkbootstrap",
        "--hidden-import=minecraft_launcher_lib",
        "--hidden-import=requests",
        "--hidden-import=psutil",
        "--hidden-import=tkvideo",
        "--collect-all=ttkbootstrap",
        "--collect-all=minecraft_launcher_lib",
        str(main_script)
    ]
    
    # Aggiungi icona se esiste
    icon_path = current_dir / "icon.ico"
    if icon_path.exists():
        command.extend(["--icon", str(icon_path)])
        print("🎨 Icona trovata e aggiunta")
    
    try:
        print("⚙️ Avvio PyInstaller...")
        print(f"📋 Comando: {' '.join(command)}")
        
        result = subprocess.run(command, cwd=current_dir, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Compilazione completata con successo!")
            
            # Verifica che l'eseguibile sia stato creato
            exe_path = dist_dir / "WTF_Modpack_Launcher.exe"
            if exe_path.exists():
                file_size = exe_path.stat().st_size / (1024 * 1024)  # MB
                print(f"📦 Eseguibile creato: {exe_path}")
                print(f"📊 Dimensione: {file_size:.1f} MB")
                
                # Crea una directory di distribuzione
                release_dir = current_dir / "WTF_Modpack_Launcher_Release"
                if release_dir.exists():
                    shutil.rmtree(release_dir)
                release_dir.mkdir()
                
                # Copia l'eseguibile
                shutil.copy2(exe_path, release_dir / "WTF_Modpack_Launcher.exe")
                
                # Copia file di supporto se esistono
                support_files = [
                    "README_WTF.md",
                    "requirements_wtf.txt", 
                    "wtf_modpack_config.json",
                    "start_wtf_launcher.bat"
                ]
                
                for file_name in support_files:
                    file_path = current_dir / file_name
                    if file_path.exists():
                        shutil.copy2(file_path, release_dir)
                        print(f"📄 Copiato: {file_name}")
                
                # Copia directory di supporto
                support_dirs = ["img", "fonts", "config"]
                for dir_name in support_dirs:
                    dir_path = current_dir / dir_name
                    if dir_path.exists():
                        shutil.copytree(dir_path, release_dir / dir_name)
                        print(f"📁 Copiata directory: {dir_name}")
                
                # Crea file di avvio
                launcher_script = release_dir / "Avvia_WTF_Modpack_Launcher.bat"
                with open(launcher_script, "w", encoding="utf-8") as f:
                    f.write("@echo off\n")
                    f.write("title WTF Modpack Launcher\n")
                    f.write("echo 🚀 Avvio WTF Modpack Launcher...\n")
                    f.write("WTF_Modpack_Launcher.exe\n")
                    f.write("pause\n")
                
                print(f"🎉 Release creata in: {release_dir}")
                print("📋 Contenuto della release:")
                for item in release_dir.iterdir():
                    print(f"   📄 {item.name}")
                
                return True
            else:
                print("❌ Eseguibile non trovato dopo la compilazione")
                return False
                
        else:
            print("❌ Errore durante la compilazione:")
            print(result.stderr)
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Errore PyInstaller: {e}")
        return False
    except Exception as e:
        print(f"❌ Errore imprevisto: {e}")
        return False

def check_dependencies():
    """Verifica che le dipendenze siano installate"""
    print("🔍 Verifica dipendenze...")
    
    try:
        import PyInstaller
        print("✅ PyInstaller trovato")
    except ImportError:
        print("❌ PyInstaller non trovato!")
        print("💡 Installa con: pip install pyinstaller")
        return False
    
    # Verifica altre dipendenze
    required_modules = [
        "tkinter",
        "ttkbootstrap", 
        "minecraft_launcher_lib",
        "requests",
        "psutil"
    ]
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} non trovato!")
            return False
    
    return True

def main():
    """Funzione principale"""
    print("🎮 WTF Modpack Launcher - Build Script")
    print("=" * 50)
    
    if not check_dependencies():
        print("\n❌ Dipendenze mancanti. Installa tutti i moduli richiesti.")
        input("Premi Invio per chiudere...")
        return
    
    print("\n🔨 Avvio compilazione...")
    success = build_executable()
    
    if success:
        print("\n🎉 Compilazione completata con successo!")
        print("📦 L'eseguibile è pronto per la distribuzione.")
    else:
        print("\n❌ Compilazione fallita.")
    
    input("\nPremi Invio per chiudere...")

if __name__ == "__main__":
    main()
