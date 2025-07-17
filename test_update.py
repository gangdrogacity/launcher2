#!/usr/bin/env python3
"""
Script di test per verificare il processo di aggiornamento del launcher
"""

import sys
import os

# Aggiungi la directory corrente al path per importare i moduli
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from updater import LauncherUpdater

def test_update_detection():
    """Test per verificare l'identificazione dell'eseguibile e il controllo aggiornamenti"""
    print("="*60)
    print("TEST AGGIORNAMENTO LAUNCHER")
    print("="*60)
    
    # Crea un'istanza dell'updater
    updater = LauncherUpdater()
    
    # Test identificazione eseguibile
    print("\n1. Test identificazione eseguibile:")
    detected_exe = updater.debug_executable_detection()
    
    # Test controllo aggiornamenti
    print("\n2. Test controllo aggiornamenti:")
    try:
        update_info = updater.check_for_updates()
        print(f"✅ Risultato controllo:")
        for key, value in update_info.items():
            print(f"   - {key}: {value}")
    except Exception as e:
        print(f"❌ Errore nel controllo: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("Test completato!")
    print("="*60)

if __name__ == "__main__":
    test_update_detection()
