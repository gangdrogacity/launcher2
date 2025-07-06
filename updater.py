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
import tempfile
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
        self.temp_dir = tempfile.mkdtemp()
        
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
                if 'windows' in asset_name or asset_name.endswith('.exe') or asset_name.endswith('.zip'):
                    return asset['browser_download_url']
            elif os_type == 'linux':
                if 'linux' in asset_name or asset_name.endswith('.tar.gz'):
                    return asset['browser_download_url']
            elif os_type == 'darwin':  # macOS
                if 'mac' in asset_name or 'darwin' in asset_name or asset_name.endswith('.dmg'):
                    return asset['browser_download_url']
        
        # Fallback: cerca un file zip generico o il primo asset
        for asset in release_data['assets']:
            if asset['name'].endswith('.zip'):
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
                filename = f"launcher_update_{int(time.time())}.zip"
            
            file_path = os.path.join(self.temp_dir, filename)
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            progress_callback(progress)
            
            print(f"✅ Download completato: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"❌ Errore durante il download: {e}")
            raise
    
    def extract_and_install(self, update_file):
        """Estrae e installa l'aggiornamento"""
        try:
            print("📦 Estrazione aggiornamento...")
            
            # Crea una directory temporanea per l'estrazione
            extract_dir = os.path.join(self.temp_dir, "update_extract")
            os.makedirs(extract_dir, exist_ok=True)
            
            # Estrae il file
            with ZipFile(update_file, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            print("🔄 Installazione aggiornamento...")
            
            # Crea uno script di aggiornamento per sostituire i file
            update_script = self.create_update_script(extract_dir)
            
            print("🚀 Avvio processo di aggiornamento...")
            
            # Esegue lo script di aggiornamento e chiude il launcher
            if platform.system() == 'Windows':
                subprocess.Popen([update_script], shell=True)
            else:
                subprocess.Popen(['bash', update_script])
            
            return True
            
        except Exception as e:
            print(f"❌ Errore durante l'installazione: {e}")
            raise
    
    def create_update_script(self, extract_dir):
        """Crea uno script per completare l'aggiornamento"""
        if platform.system() == 'Windows':
            script_path = os.path.join(self.temp_dir, "update_launcher.bat")
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
xcopy "{self.launcher_dir}\\*" "{self.launcher_dir}\\backup\\" /e /i /y /exclude:backup

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

REM Pulisce i file temporanei
timeout /t 5 /nobreak > nul
rmdir /s /q "{self.temp_dir}"

echo Aggiornamento completato!
pause
del "%~f0"
"""
        else:
            script_path = os.path.join(self.temp_dir, "update_launcher.sh")
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
    "{self.launcher_dir}/WTF_Modpack_Launcher" &
elif [ -f "{self.launcher_dir}/main.py" ]; then
    python3 "{self.launcher_dir}/main.py" &
fi

# Pulisce i file temporanei
sleep 5
rm -rf "{self.temp_dir}"

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
            return False
    
    def update_launcher(self, progress_callback=None):
        """Processo completo di aggiornamento del launcher"""
        try:
            # Controlla aggiornamenti
            update_info = self.check_for_updates()
            
            if not update_info['available']:
                if 'error' in update_info:
                    messagebox.showerror(
                        "Errore",
                        f"Impossibile controllare gli aggiornamenti:\n{update_info['error']}"
                    )
                return False
            
            # Chiede conferma all'utente
            if not self.prompt_for_update(update_info):
                print("Aggiornamento annullato dall'utente")
                return False
            
            # Scarica l'aggiornamento
            download_url = update_info['download_url']
            if not download_url:
                messagebox.showerror(
                    "Errore",
                    "Impossibile trovare il file di aggiornamento per il tuo sistema operativo."
                )
                return False
            
            update_file = self.download_update(download_url, progress_callback)
            
            # Installa l'aggiornamento
            self.extract_and_install(update_file)
            
            # Chiude il launcher corrente
            messagebox.showinfo(
                "Aggiornamento",
                "Aggiornamento scaricato! Il launcher verrà riavviato..."
            )
            
            return True
            
        except Exception as e:
            print(f"❌ Errore durante l'aggiornamento: {e}")
            messagebox.showerror(
                "Errore Aggiornamento",
                f"Si è verificato un errore durante l'aggiornamento:\n{str(e)}"
            )
            return False
        finally:
            # Pulisce i file temporanei in caso di errore
            try:
                if os.path.exists(self.temp_dir):
                    shutil.rmtree(self.temp_dir)
            except:
                pass
    
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


def main():
    """Funzione principale per test standalone"""
    updater = LauncherUpdater()
    
    print("=== WTF Modpack Launcher Auto-Updater ===")
    print(f"Versione corrente: {updater.current_version}")
    
    # Controlla aggiornamenti
    update_info = updater.check_for_updates()
    
    if update_info['available']:
        print(f"🎉 Aggiornamento disponibile: {update_info['version']}")
        
        # Simula il download con progress
        def progress_callback(progress):
            print(f"📥 Download: {progress:.1f}%")
        
        try:
            if updater.update_launcher(progress_callback):
                print("✅ Aggiornamento completato!")
            else:
                print("❌ Aggiornamento fallito")
        except KeyboardInterrupt:
            print("\n⏹️ Aggiornamento interrotto dall'utente")
    else:
        print("✅ Nessun aggiornamento disponibile")


if __name__ == "__main__":
    main()
