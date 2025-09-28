#!/usr/bin/env python3

"""
WTF Modpack Launcher - Build Script Universale
Supporta Windows e macOS automaticamente
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, shell=False):
    """Esegue un comando e ritorna il risultato"""
    try:
        result = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def detect_python():
    """Rileva il comando Python corretto"""
    python_commands = ['python', 'python3', 'py']
    
    for cmd in python_commands:
        success, stdout, _ = run_command([cmd, '--version'])
        if success and 'Python 3.' in stdout:
            return cmd
    
    return None

def setup_environment():
    """Configura l'ambiente di sviluppo"""
    current_os = platform.system()
    print(f"🖥️ Sistema operativo rilevato: {current_os}")
    
    # Rileva Python
    python_cmd = detect_python()
    if not python_cmd:
        print("❌ Python 3 non trovato!")
        return False
    
    print(f"🐍 Python trovato: {python_cmd}")
    
    # Crea ambiente virtuale se non esiste
    venv_path = Path('launcher_env')
    if not venv_path.exists():
        print("📦 Creazione ambiente virtuale...")
        success, _, error = run_command([python_cmd, '-m', 'venv', 'launcher_env'])
        if not success:
            print(f"❌ Errore creazione ambiente virtuale: {error}")
            return False
    
    # Attiva ambiente virtuale e installa dipendenze
    if current_os == "Windows":
        pip_cmd = str(venv_path / 'Scripts' / 'pip')
        python_venv = str(venv_path / 'Scripts' / 'python')
    else:
        pip_cmd = str(venv_path / 'bin' / 'pip')
        python_venv = str(venv_path / 'bin' / 'python')
    
    print("📥 Installazione dipendenze...")
    success, _, error = run_command([pip_cmd, 'install', '-r', 'requirements.txt'])
    if not success:
        print(f"❌ Errore installazione dipendenze: {error}")
        return False
    
    print("📥 Installazione PyInstaller...")
    success, _, error = run_command([pip_cmd, 'install', 'pyinstaller'])
    if not success:
        print(f"❌ Errore installazione PyInstaller: {error}")
        return False
    
    return python_venv

def build_application(python_cmd):
    """Compila l'applicazione"""
    current_os = platform.system()
    
    # Pulisci build precedenti
    print("🧹 Pulizia build precedenti...")
    for dir_name in ['build', 'dist']:
        if Path(dir_name).exists():
            try:
                shutil.rmtree(dir_name)
            except OSError:
                # Su macOS a volte dist è bloccato, forza la rimozione
                import subprocess
                subprocess.run(['rm', '-rf', dir_name], check=False)
    
    # Compila con PyInstaller
    print("⚙️ Compilazione in corso...")
    success, stdout, stderr = run_command([python_cmd, '-m', 'PyInstaller', 'launcher.spec'])
    
    if not success:
        print(f"❌ Compilazione fallita!")
        print(f"Errore: {stderr}")
        return False
    
    # Verifica risultato
    if current_os == "Darwin":  # macOS
        app_path = Path('dist') / 'WTF Modpack Launcher.app'
        if app_path.exists():
            print("✅ Applicazione macOS creata con successo!")
            # Applica fix per macOS
            apply_macos_fixes(app_path)
            return str(app_path)
    else:  # Windows/Linux
        exe_path = Path('dist') / 'WTF Modpack Launcher'
        if current_os == "Windows":
            exe_path = exe_path.with_suffix('.exe')
        
        if exe_path.exists():
            print(f"✅ Eseguibile {current_os} creato con successo!")
            return str(exe_path)
    
    print("❌ File di output non trovato!")
    return False

def apply_macos_fixes(app_path):
    """Applica fix specifici per macOS"""
    print("🔧 Applicazione fix macOS...")
    
    try:
        # Rimuovi attributi quarantena
        run_command(['xattr', '-cr', str(app_path)])
        
        # Firma applicazione
        run_command(['codesign', '--force', '--sign', '-', '--deep', str(app_path)])
        
        print("✅ Fix macOS applicati!")
    except Exception as e:
        print(f"⚠️ Warning fix macOS: {e}")

def main():
    print("🚀 WTF Modpack Launcher - Build Universale")
    print("=" * 50)
    
    # Setup ambiente
    python_cmd = setup_environment()
    if not python_cmd:
        sys.exit(1)
    
    # Build applicazione
    result = build_application(python_cmd)
    if not result:
        sys.exit(1)
    
    print("\n🎉 Build completato con successo!")
    print(f"📱 Applicazione: {result}")
    print("\n🎯 Per testare l'applicazione:")
    
    if platform.system() == "Darwin":
        print(f"   open '{result}'")
    elif platform.system() == "Windows":
        print(f"   {result}")
    else:
        print(f"   ./{result}")

if __name__ == "__main__":
    main()
