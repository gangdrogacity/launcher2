"""
WTF Modpack Launcher Auto-Updater
Gestisce l'autoaggiornamento del launcher dalle release GitHub
"""

import os
import sys
import json
import requests
import platform
import subprocess
import shutil
from zipfile import ZipFile
from tkinter import messagebox
import threading
import time

class LauncherUpdater:
    def __init__(self):
        self.repo_url = "https://github.com/gangdrogacity/launcher2"
        self.api_url = "https://api.github.com/repos/gangdrogacity/launcher2/releases/latest"
        self.current_version = self.get_current_version()
        self.launcher_dir = os.path.dirname(os.path.abspath(__file__))
        self._update_in_progress = False  # Flag per prevenire ricorsioni
        self._exe_detection_cache = None  # Cache per l'identificazione exe
        self._safe_gui_mode = True  # Modalità GUI sicura attivata di default
        
    def get_current_version(self):
        """Ottiene la versione corrente del launcher dal file launcher_version.txt"""
        try:
            version_file = os.path.join(os.path.dirname(__file__), "launcher_version.txt")
            if os.path.exists(version_file):
                with open(version_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            else:
                return "v1.0.0"  # Versione di fallback
        except Exception as e:
            print(f"Errore nel leggere la versione corrente: {e}")
            return "v1.0.0"
    
    def check_for_updates(self):
        """Controlla se ci sono aggiornamenti disponibili"""
        try:
            print("🔍 Controllo aggiornamenti del launcher...")
            response = requests.get(self.api_url, timeout=10)
            
            if response.status_code == 200:
                release_data = response.json()
                latest_version = release_data['tag_name']
                
                print(f"📋 Versione corrente: {self.current_version}")
                print(f"📋 Versione disponibile: {latest_version}")
                
                if self.is_newer_version(latest_version, self.current_version):
                    return {
                        'available': True,
                        'version': latest_version,
                        'download_url': self.get_download_url(release_data),
                        'changelog': release_data.get('body', 'Nessun changelog disponibile'),
                        'published_at': release_data.get('published_at'),
                        'size': self.get_asset_size(release_data)
                    }
                else:
                    print("✅ Il launcher è già aggiornato!")
                    return {'available': False}
            else:
                print(f"❌ Errore nel controllo aggiornamenti: HTTP {response.status_code}")
                return {'available': False, 'error': f"HTTP {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Errore di connessione: {e}")
            return {'available': False, 'error': str(e)}
        except Exception as e:
            print(f"❌ Errore generico: {e}")
            return {'available': False, 'error': str(e)}
    
    def is_newer_version(self, latest, current):
        """Confronta le versioni per determinare se c'è un aggiornamento"""
        try:
            # Rimuove il prefisso 'v' se presente
            latest_clean = latest.replace('v', '')
            current_clean = current.replace('v', '')
            
            # Converte le versioni in tuple di numeri per il confronto
            latest_parts = tuple(map(int, latest_clean.split('.')))
            current_parts = tuple(map(int, current_clean.split('.')))
            
            return latest_parts > current_parts
        except ValueError:
            # Se non riesce a parsare le versioni, considera l'aggiornamento disponibile
            return latest != current
    
    def get_download_url(self, release_data):
        """Ottiene l'URL di download appropriato per il sistema operativo"""
        os_type = platform.system().lower()
        
        for asset in release_data['assets']:
            asset_name = asset['name'].lower()
            
            # Cerca il file appropriato per il sistema operativo
            if os_type == 'windows':
                # Priorità ai file .exe per Windows
                if asset_name.endswith('.exe'):
                    return asset['browser_download_url']
            elif os_type == 'linux':
                if 'linux' in asset_name or asset_name.endswith('.tar.gz'):
                    return asset['browser_download_url']
            elif os_type == 'darwin':  # macOS
                if 'mac' in asset_name or 'darwin' in asset_name or asset_name.endswith('.dmg'):
                    return asset['browser_download_url']
        
        # Fallback per Windows: cerca file con 'windows' nel nome
        if os_type == 'windows':
            for asset in release_data['assets']:
                if 'windows' in asset['name'].lower():
                    return asset['browser_download_url']
        
        # Ultimo fallback: primo asset disponibile
        if release_data['assets']:
            return release_data['assets'][0]['browser_download_url']
        
        return None
    
    def get_asset_size(self, release_data):
        """Ottiene la dimensione del file di aggiornamento"""
        download_url = self.get_download_url(release_data)
        if download_url:
            for asset in release_data['assets']:
                if asset['browser_download_url'] == download_url:
                    return asset.get('size', 0)
        return 0
    
    def format_size(self, size_bytes):
        """Formatta la dimensione in bytes in formato leggibile"""
        if size_bytes == 0:
            return "Sconosciuta"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def download_update(self, download_url, progress_callback=None):
        """Scarica l'aggiornamento"""
        try:
            print(f"📥 Scaricamento aggiornamento da: {download_url}")
            
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            
            # Determina il nome del file
            filename = download_url.split('/')[-1]
            if not filename or filename == 'latest':
                # Per file .exe, usa un nome specifico
                if download_url.endswith('.exe') or 'exe' in download_url:
                    filename = f"WTF_Modpack_Launcher_update.exe"
                else:
                    filename = f"launcher_update_{int(time.time())}.zip"
            
            # Salva direttamente nella cartella del launcher invece che nella temp
            file_path = os.path.join(self.launcher_dir, filename)
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            print(f"📦 Dimensione file: {self.format_size(total_size)}")
            print(f"💾 Salvando in: {file_path}")
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback and total_size > 0:
                            try:
                                progress = (downloaded / total_size) * 100
                                progress_callback(progress)
                            except Exception as callback_error:
                                # Ignora errori del callback (problemi GUI)
                                print(f"⚠️ Errore callback progresso (ignorato): {callback_error}")
                                progress_callback = None  # Disabilita callback per evitare errori futuri
                        elif total_size > 0:
                            # Se non c'è callback, mostra comunque il progresso in console
                            progress = (downloaded / total_size) * 100
                            if int(progress) % 10 == 0:  # Ogni 10%
                                print(f"📥 Download: {progress:.0f}%")
            
            print(f"✅ Download completato: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"❌ Errore durante il download: {e}")
            raise
    
    def install_update(self, update_file, new_version=None):
        """Installa l'aggiornamento sostituendo l'eseguibile corrente"""
        try:
            print("🔄 Installazione aggiornamento...")
            
            # Determina il nome dell'eseguibile corrente
            current_exe = self.get_current_executable()
            if not current_exe:
                print("❌ Impossibile determinare l'eseguibile corrente")
                print("🔍 Tentativo di debug:")
                print(f"   - Directory launcher: {self.launcher_dir}")
                print(f"   - sys.frozen: {hasattr(sys, 'frozen')}")
                print(f"   - sys.executable: {sys.executable}")
                print(f"   - sys.argv[0]: {sys.argv[0]}")
                
                # Prova a determinare dove dovrebbe essere l'eseguibile
                preferred_locations = [
                    os.path.join(self.launcher_dir, 'WTF_Modpack_Launcher.exe'),
                    os.path.join(self.launcher_dir, 'dist', 'WTF_Modpack_Launcher.exe'),
                    os.path.join(self.launcher_dir, 'main.exe')
                ]
                
                print("� Tentativo di posizionamento automatico dell'aggiornamento...")
                for target_path in preferred_locations:
                    target_dir = os.path.dirname(target_path)
                    
                    # Crea la directory se non esiste
                    if not os.path.exists(target_dir):
                        print(f"📁 Creazione directory: {target_dir}")
                        os.makedirs(target_dir, exist_ok=True)
                    
                    print(f"📦 Posizionamento dell'aggiornamento in: {target_path}")
                    
                    try:
                        # Copia il file di aggiornamento nella posizione target
                        shutil.copy2(update_file, target_path)
                        print(f"✅ Aggiornamento posizionato con successo: {target_path}")
                        
                        # Aggiorna il file di versione
                        if new_version:
                            self.update_version_file(new_version)
                        
                        print("🎉 Aggiornamento installato!")
                        print(f"💡 Puoi ora eseguire: {target_path}")
                        return True
                        
                    except Exception as copy_error:
                        print(f"⚠️ Errore nel posizionamento in {target_path}: {copy_error}")
                        continue
                
                # Se tutti i tentativi falliscono
                raise Exception("Impossibile posizionare l'aggiornamento in nessuna location")
            
            print(f"📝 Eseguibile corrente: {current_exe}")
            print(f"📦 Nuovo eseguibile: {update_file}")
            
            # Verifica che il file di aggiornamento esista
            if not os.path.exists(update_file):
                raise Exception(f"File di aggiornamento non trovato: {update_file}")
            
            # Verifica che il file di aggiornamento non sia corrotto
            file_size = os.path.getsize(update_file)
            if file_size < 1024:  # Meno di 1KB, probabilmente corrotto
                raise Exception(f"File di aggiornamento sospetto (troppo piccolo): {file_size} bytes")
            
            print(f"✅ File di aggiornamento valido: {file_size} bytes")
            
            # Crea uno script di aggiornamento per sostituire l'eseguibile
            update_script = self.create_exe_update_script(update_file, current_exe, new_version)
            
            print("🚀 Avvio processo di aggiornamento...")
            print(f"📝 Script di aggiornamento: {update_script}")
            
            # Esegue lo script di aggiornamento e chiude il launcher
            if platform.system() == 'Windows':
                print("🔄 Avvio script batch per Windows...")
                process = subprocess.Popen([update_script], shell=True, 
                                         creationflags=subprocess.CREATE_NEW_CONSOLE)
                print(f"✅ Script avviato con PID: {process.pid}")
            else:
                print("🔄 Avvio script bash per Linux/macOS...")
                process = subprocess.Popen(['bash', update_script])
                print(f"✅ Script avviato con PID: {process.pid}")
            
            return True
            
        except Exception as e:
            print(f"❌ Errore durante l'installazione: {e}")
            print(f"📍 Traceback completo:")
            import traceback
            traceback.print_exc()
            raise
    
    def get_current_executable(self):
        """Determina il percorso dell'eseguibile corrente"""
        # Usa cache per evitare ricorsioni
        if self._exe_detection_cache is not None:
            return self._exe_detection_cache
        
        try:
            print(f"🔍 Determinando l'eseguibile corrente...")
            
            # Se stiamo eseguendo un file .exe compilato con PyInstaller
            if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
                print(f"✅ Eseguibile PyInstaller rilevato: {sys.executable}")
                self._exe_detection_cache = sys.executable
                return sys.executable
            
            print(f"🔍 Cercando eseguibili nella directory: {self.launcher_dir}")
            
            # Lista di possibili nomi e posizioni
            possible_locations = [
                # Directory del launcher
                (self.launcher_dir, [
                    'WTF_Modpack_Launcher.exe',
                    'main.exe', 
                    'launcher.exe'
                ]),
                # Directory dist (dopo compilazione)
                (os.path.join(self.launcher_dir, 'dist'), [
                    'WTF_Modpack_Launcher.exe',
                    'main.exe',
                    'launcher.exe'
                ]),
                # Directory corrente
                (os.getcwd(), [
                    'WTF_Modpack_Launcher.exe',
                    'main.exe',
                    'launcher.exe'
                ])
            ]
            
            for directory, names in possible_locations:
                print(f"🔍 Cercando in: {directory}")
                if os.path.exists(directory):
                    for name in names:
                        exe_path = os.path.join(directory, name)
                        print(f"🔍 Controllo esistenza: {exe_path}")
                        if os.path.exists(exe_path):
                            print(f"✅ Trovato eseguibile: {exe_path}")
                            self._exe_detection_cache = exe_path
                            return exe_path
                else:
                    print(f"⚠️ Directory non esistente: {directory}")
            
            # Se non trova nessun eseguibile, suggerisce la compilazione
            print(f"❌ Nessun eseguibile trovato")
            print(f"💡 Suggerimento: Compila il launcher con 'compile.bat' per creare l'eseguibile")
            print(f"💡 Oppure posiziona il file WTF_Modpack_Launcher.exe nella directory del launcher")
            
            self._exe_detection_cache = None
            return None
            
        except Exception as e:
            print(f"❌ Errore nel determinare l'eseguibile corrente: {e}")
            self._exe_detection_cache = None
            return None
    
    def create_restart_script(self, executable_path):
        """Crea uno script separato solo per riavviare il launcher"""
        try:
            restart_script_path = os.path.join(self.launcher_dir, "restart_launcher.bat")
            
            restart_content = f"""@echo off
echo Riavvio del launcher in corso...
timeout /t 2 /nobreak > nul

REM Prova diversi metodi per riavviare il launcher
echo Tentativo 1: start con directory di lavoro
cd /d "{os.path.dirname(executable_path)}"
start "" "{executable_path}"
if %errorlevel% equ 0 goto success

echo Tentativo 2: start senza directory
start "" "{executable_path}"
if %errorlevel% equ 0 goto success

echo Tentativo 3: esecuzione diretta
"{executable_path}"
if %errorlevel% equ 0 goto success

echo Tentativo 4: explorer
explorer "{executable_path}"
if %errorlevel% equ 0 goto success

echo ❌ Impossibile riavviare automaticamente
echo 💡 Apri manualmente: {executable_path}
pause
goto end

:success
echo ✅ Launcher riavviato con successo!

:end
REM Rimuove questo script con metodo più robusto
timeout /t 2 /nobreak > nul
(goto) 2>nul & del "%~f0"
"""
            
            with open(restart_script_path, 'w', encoding='utf-8') as f:
                f.write(restart_content)
            
            return restart_script_path
            
        except Exception as e:
            print(f"❌ Errore nella creazione dello script di riavvio: {e}")
            return None

    def create_exe_update_script(self, new_exe_path, current_exe_path, new_version=None):
        """Crea uno script per sostituire l'eseguibile corrente"""
        if platform.system() == 'Windows':
            script_path = os.path.join(self.launcher_dir, "update_launcher.bat")
            
            # Crea il nome del backup
            backup_exe = current_exe_path + ".backup"
            version_file = os.path.join(self.launcher_dir, "launcher_version.txt")
            
            # Crea uno script di riavvio separato
            restart_script = self.create_restart_script(current_exe_path)
            restart_cmd = ""
            if restart_script:
                restart_cmd = f'start "" "{restart_script}"'
            else:
                restart_cmd = f'start "" "{current_exe_path}"'
            
            version_update_cmd = ""
            if new_version:
                version_update_cmd = f'echo {new_version}> "{version_file}"'
            
            script_content = f"""@echo off
echo ========================================
echo WTF Modpack Launcher Auto-Update
echo ========================================
echo Aggiornamento in corso...
echo Data: %DATE% %TIME%
echo.

timeout /t 2 /nobreak > nul

echo Terminando processi del launcher...
REM Termina eventuali processi del launcher
taskkill /f /im "{os.path.basename(current_exe_path)}" 2>nul
taskkill /f /im "WTF_Modpack_Launcher.exe" 2>nul
taskkill /f /im "main.exe" 2>nul
taskkill /f /im "python.exe" 2>nul

echo Attendo chiusura processi...
timeout /t 5 /nobreak > nul

echo Creando backup dell'eseguibile corrente...
REM Crea backup dell'eseguibile corrente
if exist "{current_exe_path}" (
    copy "{current_exe_path}" "{backup_exe}" >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Backup creato: {backup_exe}
    ) else (
        echo ⚠️ Errore nella creazione del backup
    )
) else (
    echo ⚠️ File corrente non trovato: {current_exe_path}
)

echo Sostituendo l'eseguibile...
REM Sostituisce l'eseguibile
copy "{new_exe_path}" "{current_exe_path}" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Errore nella sostituzione del file!
    echo Tentativo di ripristino backup...
    if exist "{backup_exe}" (
        copy "{backup_exe}" "{current_exe_path}" >nul 2>&1
        if %errorlevel% equ 0 (
            echo ✅ Backup ripristinato
        ) else (
            echo ❌ Errore nel ripristino backup
        )
    )
    echo.
    echo Premere un tasto per continuare...
    pause
    exit /b 1
) else (
    echo ✅ Eseguibile aggiornato con successo
)

REM Aggiorna il file di versione
echo Aggiornando file di versione...
{version_update_cmd}
if %errorlevel% equ 0 (
    echo ✅ File versione aggiornato
) else (
    echo ⚠️ Errore nell'aggiornamento del file versione
)

echo.
echo ========================================
echo Aggiornamento completato con successo!
echo ========================================
echo.

echo Riavviando il launcher...
REM Usa lo script di riavvio separato se disponibile
{restart_cmd}
if %errorlevel% equ 0 (
    echo ✅ Script di riavvio avviato
    goto cleanup
)

:cleanup
echo Pulizia file temporanei...
timeout /t 3 /nobreak > nul

REM Pulisce i file temporanei
if exist "{backup_exe}" (
    del "{backup_exe}" >nul 2>&1
    echo ✅ Backup rimosso
)

REM Rimuove il file di aggiornamento nella cartella del launcher
if exist "{new_exe_path}" (
    del "{new_exe_path}" >nul 2>&1
    echo ✅ File di aggiornamento rimosso
)

REM Rimuove lo script di riavvio dopo un breve ritardo
timeout /t 5 /nobreak > nul
if exist "{os.path.join(self.launcher_dir, 'restart_launcher.bat')}" (
    del "{os.path.join(self.launcher_dir, 'restart_launcher.bat')}" >nul 2>&1
)

echo.
echo Aggiornamento completato!
echo Il launcher dovrebbe essere riavviato.
echo.
timeout /t 2 /nobreak > nul

REM Rimuove lo script stesso con metodo più robusto
(goto) 2>nul & del "%~f0"
"""
        else:
            script_path = os.path.join(self.launcher_dir, "update_launcher.sh")
            backup_exe = current_exe_path + ".backup"
            version_file = os.path.join(self.launcher_dir, "launcher_version.txt")
            
            version_update_cmd = ""
            if new_version:
                version_update_cmd = f'echo "{new_version}" > "{version_file}"'
            
            script_content = f"""#!/bin/bash
echo "Aggiornamento WTF Modpack Launcher in corso..."
sleep 3

# Termina eventuali processi del launcher
pkill -f "{os.path.basename(current_exe_path)}" 2>/dev/null
pkill -f "WTF_Modpack_Launcher" 2>/dev/null

# Attende che i processi si chiudano
sleep 3

# Crea backup dell'eseguibile corrente
if [ -f "{current_exe_path}" ]; then
    cp "{current_exe_path}" "{backup_exe}"
    echo "Backup creato: {backup_exe}"
fi

# Sostituisce l'eseguibile
cp "{new_exe_path}" "{current_exe_path}"
if [ $? -ne 0 ]; then
    echo "Errore nella sostituzione del file!"
    if [ -f "{backup_exe}" ]; then
        cp "{backup_exe}" "{current_exe_path}"
        echo "Backup ripristinato"
    fi
    exit 1
fi

# Rende eseguibile il nuovo file
chmod +x "{current_exe_path}"

# Aggiorna il file di versione
{version_update_cmd}

echo "Aggiornamento completato con successo!"

# Riavvia il launcher
"{current_exe_path}" &

# Pulisce i file di aggiornamento
sleep 5
if [ -f "{backup_exe}" ]; then
    rm "{backup_exe}"
fi
if [ -f "{new_exe_path}" ]; then
    rm "{new_exe_path}"
fi

# Rimuove lo script di riavvio se esiste
if [ -f "{os.path.join(self.launcher_dir, 'restart_launcher.sh')}" ]; then
    rm "{os.path.join(self.launcher_dir, 'restart_launcher.sh')}" 2>/dev/null
fi

echo "Aggiornamento completato!"
rm "$0"
"""
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Rende eseguibile lo script su sistemi Unix
        if platform.system() != 'Windows':
            os.chmod(script_path, 0o755)
        
        return script_path
    
    def prompt_for_update(self, update_info):
        """Mostra un prompt per chiedere all'utente se vuole aggiornare"""
        try:
            # Verifica se siamo in un ambiente sicuro per mostrare messagebox
            if hasattr(sys, 'frozen') or not hasattr(self, '_safe_gui_mode'):
                print("⚠️ Modalità automatica: prompt saltato")
                return True  # In modalità automatica, procedi sempre
            
            version = update_info['version']
            size = self.format_size(update_info.get('size', 0))
            changelog = update_info.get('changelog', 'Nessun changelog disponibile')
            
            # Limita la lunghezza del changelog
            if len(changelog) > 300:
                changelog = changelog[:300] + "..."
            
            message = f"""🚀 Nuovo aggiornamento disponibile!

📋 Versione corrente: {self.current_version}
📋 Nuova versione: {version}
📦 Dimensione: {size}

📝 Novità:
{changelog}

Vuoi scaricare e installare l'aggiornamento ora?

⚠️ Il launcher verrà riavviato automaticamente dopo l'aggiornamento."""
            
            result = messagebox.askyesno(
                "Aggiornamento Disponibile",
                message,
                icon='question'
            )
            
            return result
            
        except Exception as e:
            print(f"Errore nel mostrare il prompt di aggiornamento: {e}")
            print("🔄 Procedendo automaticamente con l'aggiornamento...")
            return True  # Se fallisce il prompt, procedi comunque
    
    def compile_launcher_if_needed(self):
        """Compila il launcher se non trova l'eseguibile e esiste compile.bat"""
        try:
            # Prevenzione ricorsione
            if hasattr(self, '_compiling') and self._compiling:
                print("⚠️ Compilazione già in corso, evitando ricorsione")
                return True
            
            # Controlla se esiste già un eseguibile (usa cache)
            if self.get_current_executable():
                return True
            
            self._compiling = True
            
            print("🔍 Nessun eseguibile trovato, controllo se posso compilarlo...")
            
            # Controlla se esiste compile.bat
            compile_script = os.path.join(self.launcher_dir, 'compile.bat')
            if not os.path.exists(compile_script):
                print("❌ compile.bat non trovato, impossibile compilare automaticamente")
                return False
            
            # Controlla se esiste main.py o main.spec
            main_py = os.path.join(self.launcher_dir, 'main.py')
            main_spec = os.path.join(self.launcher_dir, 'main.spec')
            
            if not os.path.exists(main_py) and not os.path.exists(main_spec):
                print("❌ main.py o main.spec non trovati, impossibile compilare")
                return False
            
            print("🛠️ Tentativo di compilazione automatica del launcher...")
            print("⚠️ Questo potrebbe richiedere alcuni minuti...")
            
            # Esegue compile.bat
            result = subprocess.run([compile_script], 
                                  shell=True, 
                                  cwd=self.launcher_dir,
                                  capture_output=True, 
                                  text=True, 
                                  timeout=300)  # Timeout di 5 minuti
            
            if result.returncode == 0:
                print("✅ Compilazione completata con successo!")
                
                # Resetta cache e controlla se ora esiste l'eseguibile
                self._exe_detection_cache = None
                exe_path = self.get_current_executable()
                if exe_path:
                    print(f"✅ Eseguibile creato: {exe_path}")
                    return True
                else:
                    print("⚠️ Compilazione completata ma eseguibile non trovato")
                    return False
            else:
                print(f"❌ Errore durante la compilazione:")
                print(f"Exit code: {result.returncode}")
                if result.stdout:
                    print(f"Output: {result.stdout}")
                if result.stderr:
                    print(f"Errori: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Timeout durante la compilazione (> 5 minuti)")
            return False
        except Exception as e:
            print(f"❌ Errore durante la compilazione automatica: {e}")
            return False
        finally:
            self._compiling = False

    def update_launcher(self, progress_callback=None, auto_mode=True):
        """Processo completo di aggiornamento del launcher"""
        # Prevenzione ricorsione
        if self._update_in_progress:
            print("⚠️ Aggiornamento già in corso, evitando ricorsione")
            return False
        
        self._update_in_progress = True
        
        # Imposta modalità GUI sicura solo se non siamo in modalità automatica e non in un exe
        self.set_safe_gui_mode(not auto_mode and not hasattr(sys, 'frozen'))
        
        try:
            # Prima tenta di compilare il launcher se necessario (solo in modalità manuale E se non siamo in un exe)
            if not auto_mode and not hasattr(sys, 'frozen'):
                print("🔧 Controllo se il launcher deve essere compilato...")
                self.compile_launcher_if_needed()
            
            # Controlla aggiornamenti
            update_info = self.check_for_updates()
            
            if not update_info['available']:
                if 'error' in update_info and not auto_mode:
                    self.safe_messagebox(
                        messagebox.showerror,
                        "Errore",
                        f"Impossibile controllare gli aggiornamenti:\n{update_info['error']}"
                    )
                return False
            
            # In modalità automatica, salta la richiesta di conferma
            if not auto_mode:
                # Chiede conferma all'utente solo in modalità manuale
                if not self.prompt_for_update(update_info):
                    print("Aggiornamento annullato dall'utente")
                    return False
            else:
                print(f"🚀 Aggiornamento automatico del launcher alla versione {update_info['version']}")
                print("⚠️ L'aggiornamento proseguirà automaticamente senza richiesta di conferma")
            
            # Preparazione per chiusura controllata
            self.graceful_close_launcher()
            
            # Scarica l'aggiornamento
            download_url = update_info['download_url']
            if not download_url:
                if not auto_mode:
                    self.safe_messagebox(
                        messagebox.showerror,
                        "Errore",
                        "Impossibile trovare il file di aggiornamento per il tuo sistema operativo."
                    )
                return False
            
            # Crea un callback di progresso sicuro
            safe_progress_callback = self.create_safe_progress_callback(progress_callback)
            
            update_file = self.download_update(download_url, safe_progress_callback)
            
            # Installa l'aggiornamento (gestisce sia .exe che .zip)
            if update_file.lower().endswith('.exe'):
                self.install_update(update_file, update_info['version'])
            else:
                # Fallback per file zip (mantiene la compatibilità)
                self.extract_and_install_zip(update_file)
            
            # In modalità automatica, non mostra messaggi
            if not auto_mode:
                self.safe_messagebox(
                    messagebox.showinfo,
                    "Aggiornamento",
                    "Aggiornamento scaricato! Il launcher verrà riavviato..."
                )
            
            return True
            
        except Exception as e:
            print(f"❌ Errore durante l'aggiornamento: {e}")
            import traceback
            print(f"📍 Traceback completo:")
            traceback.print_exc()
            
            if not auto_mode:
                self.safe_messagebox(
                    messagebox.showerror,
                    "Errore Aggiornamento",
                    f"Si è verificato un errore durante l'aggiornamento:\n{str(e)}"
                )
            return False
        finally:
            # Nota: i file di aggiornamento ora vengono gestiti negli script di update
            self._update_in_progress = False
            self.set_safe_gui_mode(False)  # Disabilita modalità GUI alla fine
    
    def check_updates_async(self, callback=None):
        """Controlla gli aggiornamenti in modo asincrono"""
        def check_thread():
            try:
                update_info = self.check_for_updates()
                if callback:
                    callback(update_info)
            except Exception as e:
                print(f"Errore nel controllo asincrono degli aggiornamenti: {e}")
                if callback:
                    callback({'available': False, 'error': str(e)})
        
        thread = threading.Thread(target=check_thread, daemon=True)
        thread.start()
        return thread

    def extract_and_install_zip(self, update_file):
        """Estrae e installa l'aggiornamento da un file zip (fallback)"""
        try:
            print("📦 Estrazione aggiornamento da file zip...")
            
            # Crea una directory per l'estrazione nella cartella del launcher
            extract_dir = os.path.join(self.launcher_dir, "update_extract")
            os.makedirs(extract_dir, exist_ok=True)
            
            # Estrae il file
            with ZipFile(update_file, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            print("🔄 Installazione aggiornamento...")
            
            # Cerca l'eseguibile principale nel contenuto estratto
            main_exe = None
            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    if file.lower() in ['wtf_modpack_launcher.exe', 'main.exe', 'launcher.exe']:
                        main_exe = os.path.join(root, file)
                        break
                if main_exe:
                    break
            
            if main_exe:
                # Se trova un eseguibile, usa il metodo di sostituzione diretta
                current_exe = self.get_current_executable()
                if current_exe:
                    update_script = self.create_exe_update_script(main_exe, current_exe)
                else:
                    raise Exception("Impossibile determinare l'eseguibile corrente")
            else:
                # Altrimenti usa il metodo di copia completa
                update_script = self.create_full_update_script(extract_dir)
            
            print("🚀 Avvio processo di aggiornamento...")
            
            # Esegue lo script di aggiornamento e chiude il launcher
            if platform.system() == 'Windows':
                subprocess.Popen([update_script], shell=True)
            else:
                subprocess.Popen(['bash', update_script])
            
            return True
            
        except Exception as e:
            print(f"❌ Errore durante l'installazione da zip: {e}")
            raise

    def create_full_update_script(self, extract_dir):
        """Crea uno script per aggiornamento completo (per file zip)"""
        if platform.system() == 'Windows':
            script_path = os.path.join(self.launcher_dir, "update_launcher_full.bat")
            script_content = f"""@echo off
echo Aggiornamento WTF Modpack Launcher in corso...
timeout /t 3 /nobreak > nul

REM Termina eventuali processi del launcher
taskkill /f /im "WTF_Modpack_Launcher.exe" 2>nul
taskkill /f /im "main.exe" 2>nul
taskkill /f /im "python.exe" 2>nul

REM Attende che i processi si chiudano
timeout /t 2 /nobreak > nul

REM Esegue il backup dei file correnti
if exist "{self.launcher_dir}\\backup" rmdir /s /q "{self.launcher_dir}\\backup"
mkdir "{self.launcher_dir}\\backup"
xcopy "{self.launcher_dir}\\*" "{self.launcher_dir}\\backup\\" /e /i /y 2>nul

REM Copia i nuovi file
xcopy "{extract_dir}\\*" "{self.launcher_dir}\\" /e /i /y

REM Riavvia il launcher
if exist "{self.launcher_dir}\\WTF_Modpack_Launcher.exe" (
    start "" "{self.launcher_dir}\\WTF_Modpack_Launcher.exe"
) else if exist "{self.launcher_dir}\\main.exe" (
    start "" "{self.launcher_dir}\\main.exe"
) else if exist "{self.launcher_dir}\\main.py" (
    start "" python "{self.launcher_dir}\\main.py"
)

REM Pulisce i file temporanei di aggiornamento
timeout /t 5 /nobreak > nul
if exist "{self.launcher_dir}\\update_extract" rmdir /s /q "{self.launcher_dir}\\update_extract" 2>nul

echo Aggiornamento completato!
del "%~f0"
"""
        else:
            script_path = os.path.join(self.launcher_dir, "update_launcher_full.sh")
            script_content = f"""#!/bin/bash
echo "Aggiornamento WTF Modpack Launcher in corso..."
sleep 3

# Termina eventuali processi del launcher
pkill -f "main.py" 2>/dev/null
pkill -f "WTF_Modpack_Launcher" 2>/dev/null

# Attende che i processi si chiudano
sleep 2

# Esegue il backup dei file correnti
if [ -d "{self.launcher_dir}/backup" ]; then
    rm -rf "{self.launcher_dir}/backup"
fi
mkdir -p "{self.launcher_dir}/backup"
cp -r "{self.launcher_dir}"/* "{self.launcher_dir}/backup/" 2>/dev/null

# Copia i nuovi file
cp -rf "{extract_dir}"/* "{self.launcher_dir}/"

# Riavvia il launcher
if [ -f "{self.launcher_dir}/WTF_Modpack_Launcher" ]; then
    chmod +x "{self.launcher_dir}/WTF_Modpack_Launcher"
    "{self.launcher_dir}/WTF_Modpack_Launcher" &
elif [ -f "{self.launcher_dir}/main.py" ]; then
    python3 "{self.launcher_dir}/main.py" &
fi

# Pulisce i file temporanei di aggiornamento
sleep 5
if [ -d "{self.launcher_dir}/update_extract" ]; then
    rm -rf "{self.launcher_dir}/update_extract"
fi

echo "Aggiornamento completato!"
rm "$0"
"""
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Rende eseguibile lo script su sistemi Unix
        if platform.system() != 'Windows':
            os.chmod(script_path, 0o755)
        
        return script_path

    def update_version_file(self, new_version):
        """Aggiorna il file launcher_version.txt con la nuova versione"""
        try:
            version_file = os.path.join(self.launcher_dir, "launcher_version.txt")
            with open(version_file, 'w', encoding='utf-8') as f:
                f.write(new_version)
            print(f"✅ File versione aggiornato: {new_version}")
        except Exception as e:
            print(f"⚠️ Errore nell'aggiornamento del file versione: {e}")

    def download_and_install_fresh(self, progress_callback=None):
        """Scarica e installa l'aggiornamento senza cercare un eseguibile esistente"""
        try:
            print("🚀 Download e installazione aggiornamento (modalità fresh install)...")
            
            # Controlla aggiornamenti
            update_info = self.check_for_updates()
            
            if not update_info['available']:
                print("✅ Nessun aggiornamento disponibile")
                return False
            
            print(f"📦 Scaricamento versione {update_info['version']}...")
            
            # Scarica l'aggiornamento
            download_url = update_info['download_url']
            if not download_url:
                print("❌ URL di download non disponibile")
                return False
            
            update_file = self.download_update(download_url, self.create_safe_progress_callback(progress_callback))
            
            # Determina dove installare il file
            target_locations = [
                os.path.join(self.launcher_dir, 'WTF_Modpack_Launcher.exe'),
                os.path.join(self.launcher_dir, 'dist', 'WTF_Modpack_Launcher.exe'),
                os.path.join(self.launcher_dir, 'main.exe')
            ]
            
            for target_path in target_locations:
                target_dir = os.path.dirname(target_path)
                
                try:
                    # Crea la directory se non esiste
                    if not os.path.exists(target_dir):
                        print(f"📁 Creazione directory: {target_dir}")
                        os.makedirs(target_dir, exist_ok=True)
                    
                    print(f"📦 Installazione dell'aggiornamento in: {target_path}")
                    
                    # Copia il file di aggiornamento
                    shutil.copy2(update_file, target_path)
                    print(f"✅ Aggiornamento installato: {target_path}")
                    
                    # Aggiorna il file di versione
                    self.update_version_file(update_info['version'])
                    
                    print("🎉 Installazione completata!")
                    print(f"💡 Puoi ora eseguire: {target_path}")
                    return True
                    
                except Exception as e:
                    print(f"⚠️ Errore nell'installazione in {target_path}: {e}")
                    continue
            
            print("❌ Impossibile installare l'aggiornamento in nessuna location")
            return False
            
        except Exception as e:
            print(f"❌ Errore durante download e installazione: {e}")
            return False
        finally:
            # Nota: i file di aggiornamento ora vengono gestiti direttamente nella cartella del launcher
            pass

    def debug_executable_detection(self):
        """Funzione di debug per testare l'identificazione dell'eseguibile"""
        print("🔍 DEBUG: Identificazione eseguibile")
        print(f"   - Directory launcher: {self.launcher_dir}")
        print(f"   - Directory corrente: {os.getcwd()}")
        print(f"   - sys.frozen: {hasattr(sys, 'frozen')}")
        print(f"   - sys._MEIPASS: {hasattr(sys, '_MEIPASS')}")
        print(f"   - sys.executable: {sys.executable}")
        print(f"   - sys.argv[0]: {sys.argv[0]}")
        print(f"   - __file__: {__file__}")
        
        print("\n🔍 File nella directory launcher:")
        try:
            for file in os.listdir(self.launcher_dir):
                if file.endswith('.exe'):
                    file_path = os.path.join(self.launcher_dir, file)
                    file_size = os.path.getsize(file_path)
                    print(f"   - {file} ({file_size} bytes)")
        except Exception as e:
            print(f"   - Errore nella lettura directory: {e}")
        
        print("\n🔍 File nella directory dist:")
        try:
            dist_dir = os.path.join(self.launcher_dir, 'dist')
            if os.path.exists(dist_dir):
                for file in os.listdir(dist_dir):
                    if file.endswith('.exe'):
                        file_path = os.path.join(dist_dir, file)
                        file_size = os.path.getsize(file_path)
                        print(f"   - dist/{file} ({file_size} bytes)")
            else:
                print("   - Directory dist non esistente")
        except Exception as e:
            print(f"   - Errore nella lettura directory dist: {e}")
        
        print("\n🔍 File nella directory corrente:")
        try:
            for file in os.listdir(os.getcwd()):
                if file.endswith('.exe'):
                    file_path = os.path.join(os.getcwd(), file)
                    file_size = os.path.getsize(file_path)
                    print(f"   - {file} ({file_size} bytes)")
        except Exception as e:
            print(f"   - Errore nella lettura directory: {e}")
        
        detected_exe = self.get_current_executable()
        print(f"\n✅ Eseguibile rilevato: {detected_exe}")
        
        return detected_exe

    def graceful_close_launcher(self):
        """Chiude il launcher in modo controllato prima dell'aggiornamento"""
        try:
            print("🔄 Preparazione per l'aggiornamento...")
            
            # Se siamo in un eseguibile PyInstaller, possiamo tentare una chiusura più controllata
            if hasattr(sys, 'frozen'):
                print("💡 Launcher compilato rilevato, preparazione chiusura controllata...")
                
                # Salva un flag per indicare che è in corso un aggiornamento
                update_flag_file = os.path.join(self.launcher_dir, ".updating")
                try:
                    with open(update_flag_file, 'w') as f:
                        f.write("UPDATE_IN_PROGRESS")
                    print("✅ Flag di aggiornamento creato")
                except Exception as e:
                    print(f"⚠️ Impossibile creare flag di aggiornamento: {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Errore nella chiusura controllata: {e}")
            return False

    def set_safe_gui_mode(self, enabled=True):
        """Imposta se è sicuro utilizzare componenti GUI come messagebox"""
        self._safe_gui_mode = enabled
        if not enabled:
            print("⚠️ Modalità GUI sicura disabilitata - nessun messagebox verrà mostrato")
    
    def safe_messagebox(self, func, *args, **kwargs):
        """Esegue un messagebox solo se siamo in modalità GUI sicura"""
        try:
            if not hasattr(self, '_safe_gui_mode') or not self._safe_gui_mode:
                print(f"⚠️ Messagebox saltato (modalità non sicura): {args[0] if args else 'Messaggio'}")
                return None
            
            return func(*args, **kwargs)
        except Exception as e:
            print(f"⚠️ Errore nel mostrare messagebox: {e}")
            return None

    def create_safe_progress_callback(self, original_callback):
        """Crea un progress callback sicuro che non causa errori GUI"""
        if not original_callback:
            # Se non c'è callback originale, crea uno che stampa in console
            def console_callback(progress):
                if int(progress) % 5 == 0:  # Stampa ogni 5%
                    print(f"📥 Download: {progress:.0f}%")
            return console_callback
        
        def safe_callback(progress):
            # Stampa sempre il progresso in console per debug
            if int(progress) % 5 == 0:  # Stampa ogni 5%
                print(f"📥 Progresso: {progress:.0f}%")
            
            try:
                # Verifica se siamo in modalità GUI sicura
                if hasattr(self, '_safe_gui_mode') and self._safe_gui_mode:
                    original_callback(progress)
                # Se non siamo in modalità GUI sicura, mostra solo in console (già fatto sopra)
            except Exception as e:
                print(f"⚠️ Errore nel callback GUI (continuo con console): {e}")
                # Non ri-solleva l'eccezione per evitare di interrompere il download
        
        return safe_callback

def main():
    """Funzione principale per test standalone"""
    # Imposta un limite di ricorsione più basso per evitare problemi
    original_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(100)
    
    try:
        updater = LauncherUpdater()
        
        print("=== WTF Modpack Launcher Auto-Updater ===")
        print(f"Versione corrente: {updater.current_version}")
        
        # Determina se siamo in un exe o in uno script
        is_exe = hasattr(sys, 'frozen')
        auto_mode = is_exe  # Se siamo in un exe, usa modalità automatica
        
        print(f"💡 Modalità: {'EXE (automatica)' if is_exe else 'Script (manuale)'}")
        
        # Debug identificazione eseguibile solo se non siamo in un exe
        if not is_exe:
            print("\n=== DEBUG IDENTIFICAZIONE ESEGUIBILE ===")
            try:
                updater.debug_executable_detection()
            except Exception as e:
                print(f"❌ Errore nel debug: {e}")
        
        # Controlla aggiornamenti
        print("\n=== CONTROLLO AGGIORNAMENTI ===")
        try:
            update_info = updater.check_for_updates()
        except Exception as e:
            print(f"❌ Errore nel controllo aggiornamenti: {e}")
            return
        
        if update_info['available']:
            print(f"🎉 Aggiornamento disponibile: {update_info['version']}")
            
            # Prova prima l'aggiornamento normale
            exe_path = updater.get_current_executable()
            if exe_path:
                print("🔄 Tentativo aggiornamento normale...")
                # Simula il download con progress
                def progress_callback(progress):
                    print(f"📥 Download: {progress:.1f}%")
                
                try:
                    if updater.update_launcher(progress_callback, auto_mode=auto_mode):
                        print("✅ Aggiornamento completato!")
                    else:
                        print("❌ Aggiornamento fallito")
                except KeyboardInterrupt:
                    print("\n⏹️ Aggiornamento interrotto dall'utente")
                except Exception as e:
                    print(f"❌ Errore durante l'aggiornamento: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print("🔄 Nessun eseguibile trovato, tentativo fresh install...")
                def progress_callback(progress):
                    print(f"📥 Download: {progress:.1f}%")
                
                try:
                    if updater.download_and_install_fresh(progress_callback):
                        print("✅ Fresh install completato!")
                    else:
                        print("❌ Fresh install fallito")
                except KeyboardInterrupt:
                    print("\n⏹️ Fresh install interrotto dall'utente")
                except Exception as e:
                    print(f"❌ Errore durante fresh install: {e}")
                    import traceback
                    traceback.print_exc()
        else:
            print("✅ Nessun aggiornamento disponibile")
            if 'error' in update_info:
                print(f"❌ Errore: {update_info['error']}")
    
    except Exception as e:
        print(f"❌ Errore critico nel main: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Ripristina il limite di ricorsione originale
        sys.setrecursionlimit(original_limit)


if __name__ == "__main__":
    main()
