"""
Test specifico per simulare l'aggiornamento dall'exe compilato
"""

import os
import sys
import time
import shutil
from updater import LauncherUpdater

def simulate_exe_environment():
    """Simula l'ambiente di esecuzione di un exe compilato"""
    print("🎭 Simulazione ambiente exe compilato...")
    
    # Simula sys.frozen per PyInstaller
    sys.frozen = True
    sys._MEIPASS = True
    
    # Cambia sys.executable per simulare l'exe
    original_executable = sys.executable
    launcher_exe_path = os.path.join(os.path.dirname(__file__), 'dist', 'WTF_Modpack_Launcher.exe')
    
    if os.path.exists(launcher_exe_path):
        sys.executable = launcher_exe_path
        print(f"✅ Simulazione exe: {sys.executable}")
    else:
        print(f"⚠️ File exe non trovato: {launcher_exe_path}")
        print("💡 Assicurati di aver compilato il launcher con compile.bat")
    
    return original_executable

def restore_environment(original_executable):
    """Ripristina l'ambiente originale"""
    sys.executable = original_executable
    if hasattr(sys, 'frozen'):
        delattr(sys, 'frozen')
    if hasattr(sys, '_MEIPASS'):
        delattr(sys, '_MEIPASS')

def test_update_from_exe():
    """Test dell'aggiornamento simulando l'esecuzione dall'exe"""
    print("=== TEST AGGIORNAMENTO DA EXE SIMULATO ===")
    
    original_executable = simulate_exe_environment()
    
    try:
        # Crea l'updater
        updater = LauncherUpdater()
        
        print(f"🔍 Versione corrente: {updater.current_version}")
        
        # Test identificazione eseguibile in ambiente simulato
        print("\n=== TEST IDENTIFICAZIONE ESEGUIBILE ===")
        exe_path = updater.get_current_executable()
        print(f"✅ Eseguibile identificato: {exe_path}")
        
        if not exe_path:
            print("❌ Impossibile identificare l'eseguibile!")
            return False
        
        # Test controllo aggiornamenti
        print("\n=== TEST CONTROLLO AGGIORNAMENTI ===")
        update_info = updater.check_for_updates()
        
        if not update_info['available']:
            print("ℹ️ Nessun aggiornamento disponibile per il test")
            
            # Forza un aggiornamento per test (simula una versione più vecchia)
            print("🔧 Forzatura test: simulo versione vecchia...")
            updater.current_version = "v0.9.0-test"
            update_info = updater.check_for_updates()
        
        if update_info['available']:
            print(f"🎉 Aggiornamento disponibile: {update_info['version']}")
            
            # Test download (senza installare)
            def progress_callback(progress):
                if int(progress) % 10 == 0:  # Mostra solo ogni 10%
                    print(f"📥 Download: {progress:.0f}%")
            
            try:
                print("\n=== TEST DOWNLOAD AGGIORNAMENTO ===")
                download_url = update_info['download_url']
                if download_url:
                    update_file = updater.download_update(download_url, progress_callback)
                    print(f"✅ Download completato: {update_file}")
                    
                    # Test creazione script di aggiornamento
                    print("\n=== TEST CREAZIONE SCRIPT AGGIORNAMENTO ===")
                    update_script = updater.create_exe_update_script(update_file, exe_path, update_info['version'])
                    print(f"✅ Script creato: {update_script}")
                    
                    # Mostra il contenuto dello script per debug
                    if os.path.exists(update_script):
                        print(f"\n📄 Contenuto script (prime 20 righe):")
                        with open(update_script, 'r', encoding='utf-8') as f:
                            lines = f.readlines()[:20]
                            for i, line in enumerate(lines, 1):
                                print(f"{i:2d}: {line.rstrip()}")
                        print("   ... (resto del file troncato)")
                    
                    print("\n✅ Test completato con successo!")
                    print("💡 Lo script è pronto, ma non viene eseguito in modalità test")
                    
                else:
                    print("❌ URL di download non disponibile")
                    return False
                    
            except Exception as e:
                print(f"❌ Errore durante il test: {e}")
                return False
                
        else:
            print("ℹ️ Nessun aggiornamento disponibile")
        
        return True
        
    finally:
        restore_environment(original_executable)

def test_restart_script():
    """Test dello script di riavvio separato"""
    print("\n=== TEST SCRIPT RIAVVIO ===")
    
    updater = LauncherUpdater()
    exe_path = os.path.join(updater.launcher_dir, 'dist', 'WTF_Modpack_Launcher.exe')
    
    if os.path.exists(exe_path):
        restart_script = updater.create_restart_script(exe_path)
        if restart_script:
            print(f"✅ Script di riavvio creato: {restart_script}")
            
            # Mostra il contenuto
            with open(restart_script, 'r', encoding='utf-8') as f:
                print("📄 Contenuto script di riavvio:")
                print(f.read())
            
            return True
        else:
            print("❌ Impossibile creare script di riavvio")
            return False
    else:
        print(f"❌ Exe non trovato: {exe_path}")
        return False

if __name__ == "__main__":
    print("🧪 Test aggiornamento da ambiente exe simulato\n")
    
    success = test_update_from_exe()
    
    if success:
        test_restart_script()
        print("\n🎉 Tutti i test completati!")
    else:
        print("\n❌ Test falliti!")
