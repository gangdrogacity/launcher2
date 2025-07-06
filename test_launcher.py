#!/usr/bin/env python3
"""
Test script per il WTF Modpack Launcher
Verifica che tutti i componenti funzionino correttamente prima della compilazione
"""

import sys
import os
import traceback
from pathlib import Path

def test_imports():
    """Testa l'importazione di tutti i moduli necessari"""
    print("🔍 Test importazioni moduli...")
    
    modules_to_test = [
        ('tkinter', 'GUI principale'),
        ('tkinter.ttk', 'Componenti GUI avanzati'),
        ('tkinter.messagebox', 'Finestre di dialogo'),
        ('ttkbootstrap', 'Tema GUI moderno'),
        ('minecraft_launcher_lib', 'Libreria Minecraft'),
        ('minecraft_launcher_lib.forge', 'Supporto Forge'),
        ('requests', 'Richieste HTTP'),
        ('psutil', 'Informazioni sistema'),
        ('tkvideo', 'Riproduzione video in Tkinter'),
        ('numpy', 'Libreria numerica (per tkvideo)'),
        ('imageio', 'Gestione immagini/video'),
        ('uuid', 'Generazione UUID'),
        ('platform', 'Informazioni piattaforma'),
        ('json', 'Gestione JSON'),
        ('threading', 'Multi-threading'),
        ('subprocess', 'Esecuzione processi'),
        ('time', 'Gestione tempo'),
        ('shutil', 'Operazioni file'),
        ('zipfile', 'Gestione archivi'),
        ('re', 'Espressioni regolari')
    ]
    
    failed_imports = []
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name:25} - {description}")
        except ImportError as e:
            print(f"❌ {module_name:25} - ERRORE: {e}")
            failed_imports.append(module_name)
        except Exception as e:
            print(f"⚠️ {module_name:25} - WARNING: {e}")
    
    return failed_imports

def test_files():
    """Verifica che tutti i file necessari esistano"""
    print("\n📁 Test file necessari...")
    
    current_dir = Path(__file__).parent
    
    required_files = [
        ('wtf_launcher.py', 'Script principale'),
        ('icon.ico', 'Icona launcher (opzionale)'),
        ('README_WTF.md', 'README del progetto (opzionale)'),
        ('requirements_wtf.txt', 'Dipendenze Python (opzionale)')
    ]
    
    optional_files = [
        ('wtf_modpack_config.json', 'Configurazione modpack'),
        ('start_wtf_launcher.bat', 'Script di avvio batch')
    ]
    
    missing_files = []
    
    print("📄 File richiesti:")
    for file_name, description in required_files:
        file_path = current_dir / file_name
        if file_path.exists():
            print(f"✅ {file_name:25} - {description}")
        else:
            if 'opzionale' in description:
                print(f"⚠️ {file_name:25} - {description} (MANCANTE)")
            else:
                print(f"❌ {file_name:25} - {description} (RICHIESTO)")
                missing_files.append(file_name)
    
    print("\n📄 File opzionali:")
    for file_name, description in optional_files:
        file_path = current_dir / file_name
        if file_path.exists():
            print(f"✅ {file_name:25} - {description}")
        else:
            print(f"⚠️ {file_name:25} - {description} (MANCANTE)")
    
    return missing_files

def test_directories():
    """Verifica le directory opzionali"""
    print("\n📁 Test directory opzionali...")
    
    current_dir = Path(__file__).parent
    
    optional_dirs = [
        ('img', 'Immagini e risorse grafiche'),
        ('fonts', 'Font personalizzati'),
        ('config', 'File di configurazione'),
        ('logs', 'Log del launcher'),
        ('mods', 'Mod esistenti (se presenti)')
    ]
    
    for dir_name, description in optional_dirs:
        dir_path = current_dir / dir_name
        if dir_path.exists() and dir_path.is_dir():
            file_count = len(list(dir_path.iterdir()))
            print(f"✅ {dir_name:15} - {description} ({file_count} file)")
        else:
            print(f"⚠️ {dir_name:15} - {description} (MANCANTE)")

def test_launcher_syntax():
    """Testa la sintassi del launcher principale"""
    print("\n🐍 Test sintassi wtf_launcher.py...")
    
    try:
        current_dir = Path(__file__).parent
        launcher_path = current_dir / "wtf_launcher.py"
        
        if not launcher_path.exists():
            print("❌ File wtf_launcher.py non trovato!")
            return False
        
        # Compila il file per verificare la sintassi
        with open(launcher_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        compile(source_code, str(launcher_path), 'exec')
        print("✅ Sintassi corretta")
        
        # Verifica alcune funzioni chiave
        if 'class WTFModpackLauncher' in source_code:
            print("✅ Classe principale trovata")
        else:
            print("❌ Classe principale non trovata")
            return False
        
        if 'def setup_ui' in source_code:
            print("✅ Metodo setup_ui trovato")
        else:
            print("❌ Metodo setup_ui non trovato")
            return False
        
        if 'def launch_minecraft' in source_code:
            print("✅ Metodo launch_minecraft trovato")
        else:
            print("❌ Metodo launch_minecraft non trovato")
            return False
        
        return True
        
    except SyntaxError as e:
        print(f"❌ Errore di sintassi: {e}")
        print(f"   Linea {e.lineno}: {e.text}")
        return False
    except Exception as e:
        print(f"❌ Errore durante la verifica: {e}")
        return False

def test_pyinstaller():
    """Verifica che PyInstaller sia installato e funzionante"""
    print("\n🔨 Test PyInstaller...")
    
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__} installato")
        return True
    except ImportError:
        print("❌ PyInstaller non installato")
        print("💡 Installa con: pip install pyinstaller")
        return False

def run_all_tests():
    """Esegue tutti i test"""
    print("🧪 WTF MODPACK LAUNCHER - TEST SUITE")
    print("=" * 50)
    
    all_passed = True
    
    # Test importazioni
    failed_imports = test_imports()
    if failed_imports:
        print(f"\n❌ Moduli mancanti: {', '.join(failed_imports)}")
        print("💡 Installa con: pip install -r requirements_wtf.txt")
        all_passed = False
    
    # Test file
    missing_files = test_files()
    if missing_files:
        print(f"\n❌ File richiesti mancanti: {', '.join(missing_files)}")
        all_passed = False
    
    # Test directory
    test_directories()
    
    # Test sintassi
    if not test_launcher_syntax():
        all_passed = False
    
    # Test PyInstaller
    if not test_pyinstaller():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 TUTTI I TEST SUPERATI!")
        print("✅ Il launcher è pronto per la compilazione")
        print("\n🚀 Per compilare esegui:")
        print("   • compile_launcher.bat (Windows)")
        print("   • python build_launcher.py (Cross-platform)")
    else:
        print("❌ ALCUNI TEST FALLITI!")
        print("🔧 Risolvi i problemi sopra elencati prima di compilare")
    
    return all_passed

def main():
    """Funzione principale"""
    try:
        success = run_all_tests()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrotto dall'utente")
        return 1
    except Exception as e:
        print(f"\n❌ Errore imprevisto: {e}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    print(f"\nPremi Invio per chiudere...")
    input()
    sys.exit(exit_code)
