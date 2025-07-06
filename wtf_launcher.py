from tkinter import Canvas, PhotoImage, Entry, Tk, StringVar, DoubleVar
from tkinter import Button as Button1
from tkinter import Label as Label1
from tkinter.font import Font

import tkinter as tk
from tkinter.ttk import Combobox, Progressbar, Frame, Label, Radiobutton, Notebook, Checkbutton, Scale, Button
from tkinter.messagebox import showerror, showinfo, showwarning, askquestion
import tkinter.messagebox
from tkvideo import tkvideo
import os
import subprocess
import time
import minecraft_launcher_lib
from minecraft_launcher_lib.forge import install_forge_version, run_forge_installer, supports_automatic_install
from minecraft_launcher_lib.fabric import install_fabric, get_all_minecraft_versions, get_stable_minecraft_versions, get_latest_loader_version
import uuid
import platform
from ttkbootstrap import Style
import json
import sys
from threading import Thread
import time
import requests
import wget
from zipfile import ZipFile
from shutil import move, rmtree, copytree
import psutil
import re

print("🚀 Avvio WTF Modpack Launcher v1.0...")
print("⏳ Caricamento componenti, attendere prego...")
time.sleep(2)
print("✅ Componenti caricati!")
print("🎮 Preparazione interfaccia grafica...")

style = Style(theme="flatly")
style.configure("TNotebook.Tab", foreground="#15d38f", background="#23272a", bordercolor="#072A6C")

currn_dir = os.getcwd()
mc_dir = r"{}/.minecraft".format(currn_dir)
OS = platform.platform()

# WTF Modpack specific settings
WTF_MODPACK_REPO = "https://github.com/jamnaga/wtf-modpack"
WTF_LATEST_RELEASE_API = "https://api.github.com/repos/jamnaga/wtf-modpack/releases/latest"
WTF_FORGE_VERSION = "1.20.1-47.3.33"
WTF_MC_VERSION = "1.20.1"
WTF_MINIMUM_RAM = 4  # 4GB minimum


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


svmem = psutil.virtual_memory()

def get_latest_wtf_release():
    """Get the latest WTF modpack release info"""
    try:
        response = requests.get(WTF_LATEST_RELEASE_API)
        if response.status_code == 200:
            release_data = response.json()
            # Find the client.zip asset
            for asset in release_data['assets']:
                if asset['name'] == 'client.zip':
                    return {
                        'version': release_data['tag_name'],
                        'download_url': asset['browser_download_url'],
                        'size': asset['size']
                    }
    except Exception as e:
        print(f"Error fetching latest release: {e}")
    return None


# Generate settings.json for WTF Modpack
if OS.startswith("Linux"):
    settings = {
        "accessToken": None,
        "clientToken": None,
        "User-info": [
            {
                "username": None,
                "AUTH_TYPE": None,
                "UUID": None
            }
        ],
        "PC-info": [
            {
                "OS": platform.platform(),
                "Total-Ram": f"{get_size(svmem.total)}",
            }
        ],
        "Minecraft-home": mc_dir,
        "selected-version": f"WTF Modpack - Forge {WTF_FORGE_VERSION}",
        "Fps-Boost": False,
        "Tor-Enabled": False,
        "setting-info": [
            {
                "fps_boost_selected": False,
                "tor_enabled_selected": False,
                "allocated_ram_selected": f"{WTF_MINIMUM_RAM}G",
            }
        ],
        "allocated_ram": f"{WTF_MINIMUM_RAM}G",
        "jvm-args": None,
        "executablePath": "java",
        "ramlimiterExceptionBypassed": False,
        "ramlimiterExceptionBypassedSelected": False,
        "wtf_modpack_version": None,
        "wtf_modpack_installed": False
    }

elif OS.startswith("Windows"):
    settings = {
        "accessToken": None,
        "clientToken": None,
        "User-info": [
            {
                "username": None,
                "AUTH_TYPE": None,
                "UUID": None
            }
        ],
        "PC-info": [
            {
                "OS": platform.platform(),
                "Total-Ram": f"{get_size(svmem.total)}",
            }
        ],
        "Minecraft-home": mc_dir,
        "selected-version": f"WTF Modpack - Forge {WTF_FORGE_VERSION}",
        "Tor-Enabled": False,
        "setting-info": [
            {
                "tor_enabled_selected": False,
                "allocated_ram_selected": f"{WTF_MINIMUM_RAM}G"
            }
        ],
        "allocated_ram": f"{WTF_MINIMUM_RAM}G",
        "jvm-args": None,
        "executablePath": r"C:\\Program Files\\BellSoft\\LibericaJDK-17\\bin\\java",
        "ramlimiterExceptionBypassed": False,
        "ramlimiterExceptionBypassedSelected": False,
        "wtf_modpack_version": None,
        "wtf_modpack_installed": False
    }


if not os.path.exists(r"{}/settings.json".format(currn_dir)):
    with open("settings.json", "w") as js_set:
        json.dump(settings, js_set, indent=4)
        js_set.close()

# Load settings
with open("settings.json", "r") as js_read:
    s = js_read.read()
    s = s.replace('\t','')
    s = s.replace('\n','')
    s = s.replace(',}','}')
    s = s.replace(',]',']')
    data = json.loads(s)

os_name = data["PC-info"][0]["OS"]
mc_home = data["Minecraft-home"]
username = data["User-info"][0]["username"]
uid = data["User-info"][0]["UUID"]
accessToken = data["accessToken"]
mc_dir = data["Minecraft-home"]
auth_type = data["User-info"][0]["AUTH_TYPE"]
jvm_args = data["jvm-args"]
selected_ver = data["selected-version"]
allocated_ram = data["allocated_ram"]
wtf_modpack_version = data.get("wtf_modpack_version")
wtf_modpack_installed = data.get("wtf_modpack_installed", False)


def reload_data():
    """Reloads the json data."""
    global mc_home, username, uid, os_name, mc_dir, selected_ver
    global auth_type, jvm_args, allocated_ram, accessToken
    global wtf_modpack_version, wtf_modpack_installed

    with open("settings.json", "r") as js_read:
        s = js_read.read()
        s = s.replace('\t','')
        s = s.replace('\n','')
        s = s.replace(',}','}')
        s = s.replace(',]',']')
        data = json.loads(s)

    os_name = data["PC-info"][0]["OS"]
    mc_home = data["Minecraft-home"]
    username = data["User-info"][0]["username"]
    uid = data["User-info"][0]["UUID"]
    accessToken = data["accessToken"]
    mc_dir = data["Minecraft-home"]
    auth_type = data["User-info"][0]["AUTH_TYPE"]
    jvm_args = data["jvm-args"]
    selected_ver = data["selected-version"]
    allocated_ram = data["allocated_ram"]
    wtf_modpack_version = data.get("wtf_modpack_version")
    wtf_modpack_installed = data.get("wtf_modpack_installed", False)


# Check if .minecraft directory exists
if os.path.exists(r"{}/.minecraft".format(currn_dir)):
    print("📂 Installazione Minecraft esistente trovata...")
else:
    print("📂 Creazione directory Minecraft...")
    os.mkdir(".minecraft")
    os.chdir(".minecraft")
    os.mkdir("versions")
    os.mkdir("mods")
    print("✅ Directory Minecraft create con successo!")

connected = True

def check_internet(url='https://www.google.com', timeout=5):
    global connected
    try:
        print("🌐 Verifica connessione Internet...")
        r2 = requests.head(url, timeout=timeout)
        print("✅ Connesso a Internet")
        connected = True
        return True
    except requests.ConnectionError:
        connected = False
        print("❌ Nessuna connessione Internet disponibile.")
        return False
    except requests.exceptions.Timeout:
        connected = False
        print("⏱️ Timeout della connessione")
        return False


class WTFModpackLauncher():
    def __init__(self):
        self.custom_font = Font(family="Galiver Sans", size=26)
        self.custom_font1 = Font(family="Galiver Sans", size=14)
        self.custom_font2 = Font(family="Galiver Sans", size=26)
        self.custom_font3 = Font(family="Galiver Sans", size=16)
        self.custom_font4 = Font(family="Galiver Sans", size=12)

        self.window = style.master
        self.window.geometry("1024x600+110+60")
        self.window.title("WTF Modpack Launcher")
        self.window.configure(bg="#1c1c1c")
        
        # Track Minecraft process
        self.minecraft_process = None
        self.is_minecraft_running = False

        # Set icon (handle PyInstaller bundle)
        if os_name.startswith("Windows"):
            try:
                # Function to get correct resource path for PyInstaller
                def resource_path(relative_path):
                    """ Get absolute path to resource, works for dev and for PyInstaller """
                    try:
                        # PyInstaller creates a temp folder and stores path in _MEIPASS
                        base_path = sys._MEIPASS
                    except Exception:
                        base_path = os.path.abspath(".")
                    return os.path.join(base_path, relative_path)
                
                # Try to find icon using resource_path function
                icon_path = resource_path("icon.ico")
                if os.path.exists(icon_path):
                    self.window.iconbitmap(icon_path)
                    print(f"✅ Icona caricata da: {icon_path}")
                else:
                    print(f"⚠️ Icona non trovata in: {icon_path}")
            except Exception as e:
                # Ignore icon errors, launcher will work without icon
                print(f"⚠️ Impossibile caricare l'icona: {e}")

        self.setup_ui()
        
        # Check for updates on startup
        if connected:
            self.check_for_updates()

    def setup_ui(self):
        """Setup the main user interface"""
        self.canvas = Canvas(
            self.window,
            bg="#1c1c1c",
            height=600,
            width=1024,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Background - solid color only
        self.canvas.create_rectangle(0, 0, 1024, 600, fill="#1c1c1c", outline="")
        
        # Header section with gradient effect
        self.canvas.create_rectangle(0, 0, 1024, 120, fill="#2d2d2d", outline="")
        self.canvas.create_rectangle(0, 115, 1024, 120, fill="#15d38f", outline="")

        # Title with modern styling
        self.canvas.create_text(
            512, 60,
            text="WTF MODPACK LAUNCHER",
            fill="white",
            font=("Arial", 28, "bold")
        )

        # Subtitle
        self.canvas.create_text(
            512, 90,
            text="Minecraft 1.20.1 • Forge 47.3.33",
            fill="#b0b0b0",
            font=("Arial", 12)
        )

        # Status cards background
        self.canvas.create_rectangle(50, 140, 974, 220, fill="#2d2d2d", outline="#444444", width=1)
        
        # Version status card
        self.canvas.create_rectangle(70, 155, 320, 205, fill="#333333", outline="#555555", width=1)
        self.canvas.create_text(
            195, 170,
            text="📦 STATO MODPACK",
            fill="#15d38f",
            font=("Arial", 10, "bold")
        )
        
        # Version and status info area
        self.version_text = self.canvas.create_text(
            195, 190,
            text=f"{wtf_modpack_version if wtf_modpack_version else 'Non Installato'}",
            fill="white",
            font=("Arial", 12, "bold")
        )
        
        # System info card
        self.canvas.create_rectangle(340, 155, 590, 205, fill="#333333", outline="#555555", width=1)
        self.canvas.create_text(
            465, 170,
            text="💾 SISTEMA",
            fill="#15d38f",
            font=("Arial", 10, "bold")
        )
        
        # System info display
        total_ram = get_size(svmem.total)
        system_info = f"RAM: {total_ram} | Allocata: {allocated_ram if allocated_ram else f'{WTF_MINIMUM_RAM}G'}"
        self.system_info_text = self.canvas.create_text(
            465, 190,
            text=system_info,
            fill="white",
            font=("Arial", 9)
        )

        # Connection status card
        self.canvas.create_rectangle(610, 155, 860, 205, fill="#333333", outline="#555555", width=1)
        self.canvas.create_text(
            735, 170,
            text="🌐 CONNESSIONE",
            fill="#15d38f",
            font=("Arial", 10, "bold")
        )
        
        # Connection status indicator
        connection_status = "Online" if connected else "Offline"
        connection_color = "white" if connected else "#ff4757"
        self.connection_text = self.canvas.create_text(
            735, 190,
            text=connection_status,
            fill=connection_color,
            font=("Arial", 11, "bold")
        )

        # Modpack status indicator
        if wtf_modpack_installed:
            status_text = "✅ Pronto per Giocare"
            status_color = "#15d38f"
        else:
            status_text = "⚠️ Installazione Richiesta"
            status_color = "#ffa502"
            
        self.modpack_status_text = self.canvas.create_text(
            512, 235,
            text=status_text,
            fill=status_color,
            font=("Arial", 14, "bold")
        )

        # Install/Update button
        if wtf_modpack_installed:
            button_text = "🔄 Verifica Aggiornamenti"
            button_command = self.check_for_updates
            button_style = "info"
        else:
            button_text = "📦 Installa WTF Modpack"
            button_command = self.install_modpack
            button_style = "primary"

        self.install_button = Button(
            self.window,
            text=button_text,
            command=button_command,
            bootstyle=button_style,
            width=25
        )
        self.install_button.place(x=120, y=280, width=250, height=45)

        # Play button (larger and more prominent)
        play_text = self.get_play_button_text()
        play_command = self.get_play_button_command()
        self.play_button = Button(
            self.window,
            text=play_text,
            command=play_command,
            bootstyle="success" if not self.is_minecraft_running else "danger",
            width=30
        )
        self.play_button.place(x=387, y=275, width=250, height=55)

        # Settings button
        self.settings_button = Button(
            self.window,
            text="⚙️ Impostazioni",
            command=self.open_settings,
            bootstyle="warning",
            width=15
        )
        self.settings_button.place(x=655, y=280, width=120, height=45)

        # Repair button (only show if modpack is installed)
        if wtf_modpack_installed:
            self.repair_button = Button(
                self.window,
                text="🔧 Ripara",
                command=self.verify_and_repair_installation,
                bootstyle="secondary",
                width=12
            )
            self.repair_button.place(x=790, y=280, width=100, height=45)

        # Progress bar (initially hidden)
        self.progress_bar = Progressbar(
            self.window,
            mode='indeterminate',
            bootstyle="success-striped"
        )

        # Status area background
        self.canvas.create_rectangle(50, 360, 974, 480, fill="#2d2d2d", outline="#444444", width=1)
        
        # Status header
        self.canvas.create_text(
            512, 375,
            text="📊 STATO OPERAZIONI",
            fill="#15d38f",
            font=("Arial", 11, "bold")
        )

        # Main status label
        self.status_label = Label(
            self.window,
            text="🚀 Pronto per l'azione! Seleziona un'opzione sopra per iniziare.",
            background="#2d2d2d",
            foreground="white",
            font=("Arial", 12, "bold")
        )
        self.status_label.place(x=512, y=400, anchor="center")
        
        # Detailed status area (for longer messages)
        self.detail_label = Label(
            self.window,
            text="",
            background="#2d2d2d",
            foreground="#b0b0b0",
            font=("Arial", 10),
            wraplength=800
        )
        self.detail_label.place(x=512, y=425, anchor="center")
        
        # Progress percentage label
        self.progress_label = Label(
            self.window,
            text="",
            background="#2d2d2d",
            foreground="#15d38f",
            font=("Arial", 10, "bold")
        )
        self.progress_label.place(x=512, y=450, anchor="center")

        # Footer section
        self.canvas.create_rectangle(0, 500, 1024, 600, fill="#2d2d2d", outline="")
        self.canvas.create_rectangle(0, 500, 1024, 505, fill="#15d38f", outline="")
        
        # Info panel at bottom
        info_text = "💡 Suggerimento: Usa il modpack in modalità offline. Per il multiplayer Premium usa il launcher ufficiale."
        self.info_text = self.canvas.create_text(
            512, 530,
            text=info_text,
            fill="#b0b0b0",
            font=("Arial", 10),
            width=900
        )
        
        # Version info at bottom
        launcher_version = "WTF Modpack Launcher v1.0 • Creato per Minecraft 1.20.1"
        self.canvas.create_text(
            512, 570,
            text=launcher_version,
            fill="#666666",
            font=("Arial", 8),
            width=900
        )

        # Enable/disable play button based on installation status
        if not wtf_modpack_installed:
            self.play_button["state"] = "disabled"
        
        # Start monitoring Minecraft process
        self.start_minecraft_monitor()

    def get_play_button_text(self):
        """Get the appropriate text for the play button based on current state"""
        if self.is_minecraft_running:
            return "🛑 Chiudi Gioco"
        elif not wtf_modpack_installed:
            return "🚫 Installa Prima il Modpack"
        else:
            return "🎮 Gioca Ora!"
    
    def get_play_button_command(self):
        """Get the appropriate command for the play button based on current state"""
        if self.is_minecraft_running:
            return self.close_minecraft
        else:
            return self.launch_minecraft
    
    def start_minecraft_monitor(self):
        """Start monitoring Minecraft process status"""
        def monitor_thread():
            while True:
                try:
                    # Check if Minecraft process is still running
                    if self.minecraft_process and self.minecraft_process.poll() is None:
                        # Process is still running
                        if not self.is_minecraft_running:
                            self.is_minecraft_running = True
                            self.window.after(0, self.update_play_button)
                    else:
                        # Process has ended or doesn't exist
                        if self.is_minecraft_running:
                            self.is_minecraft_running = False
                            self.minecraft_process = None
                            self.window.after(0, self.update_play_button)
                            self.window.after(0, lambda: self.update_gui_status(
                                "✅ Sessione Completata",
                                "Minecraft è stato chiuso correttamente.",
                                "Pronto per una nuova partita!"
                            ))
                    
                    time.sleep(2)  # Check every 2 seconds
                except Exception as e:
                    print(f"Errore nel monitoraggio Minecraft: {e}")
                    time.sleep(5)
        
        monitor_thread_obj = Thread(target=monitor_thread, daemon=True)
        monitor_thread_obj.start()
    
    def update_play_button(self):
        """Update the play button text and command based on Minecraft status"""
        new_text = self.get_play_button_text()
        new_command = self.get_play_button_command()
        
        self.play_button.config(text=new_text, command=new_command)
        
        # Update button style based on state
        if self.is_minecraft_running:
            self.play_button.config(bootstyle="danger")
        else:
            self.play_button.config(bootstyle="success")
    
    def close_minecraft(self):
        """Close the running Minecraft process"""
        if self.minecraft_process and self.minecraft_process.poll() is None:
            result = askquestion("🛑 Chiudi Minecraft", 
                               "🎮 Minecraft è attualmente in esecuzione.\n\n" +
                               "⚠️ Vuoi davvero chiudere il gioco?\n" +
                               "Assicurati di aver salvato i tuoi progressi!")
            
            if result == 'yes':
                try:
                    self.update_gui_status(
                        "🛑 Chiusura Minecraft...",
                        "Terminando il processo di Minecraft...",
                        "Attendi la chiusura completa del gioco"
                    )
                    
                    # Try graceful termination first
                    self.minecraft_process.terminate()
                    
                    # Wait a moment for graceful shutdown
                    try:
                        self.minecraft_process.wait(timeout=10)
                        print("✅ Minecraft chiuso correttamente")
                    except subprocess.TimeoutExpired:
                        # Force kill if it doesn't close gracefully
                        print("⚠️ Forzando la chiusura di Minecraft...")
                        self.minecraft_process.kill()
                        self.minecraft_process.wait()
                        print("✅ Minecraft forzatamente chiuso")
                    
                    self.minecraft_process = None
                    self.is_minecraft_running = False
                    self.update_play_button()
                    
                    showinfo("✅ Gioco Chiuso", 
                            "🎮 Minecraft è stato chiuso con successo!\n\n" +
                            "Ora puoi:\n" +
                            "• Avviare una nuova sessione\n" +
                            "• Modificare le impostazioni\n" +
                            "• Verificare aggiornamenti")
                    
                except Exception as e:
                    showerror("❌ Errore", 
                             f"❌ Errore durante la chiusura di Minecraft:\n\n" +
                             f"🔧 Dettagli: {str(e)}\n\n" +
                             f"💡 Prova a chiudere Minecraft manualmente.")
        else:
            showwarning("⚠️ Processo Non Trovato", 
                       "❌ Il processo di Minecraft non è stato trovato.\n\n" +
                       "Il gioco potrebbe essere già stato chiuso.")
            self.is_minecraft_running = False
            self.minecraft_process = None
            self.update_play_button()
    
    def check_for_updates(self):
        """Check for modpack updates"""
        if not connected:
            self.update_gui_status(
                "❌ Connessione Internet Richiesta",
                "Impossibile verificare aggiornamenti senza connessione Internet.",
                "Controlla la tua connessione e riprova."
            )
            showwarning("Connessione Internet Richiesta", 
                       "È necessaria una connessione Internet per verificare gli aggiornamenti del modpack.\n\n" +
                       "Controlla la tua connessione e riprova.")
            return

        self.update_gui_status(
            "🔍 Controllo Aggiornamenti...",
            "Contattando il repository GitHub per verificare nuove versioni...",
            "Connessione al server in corso...",
            True
        )

        try:
            latest_release = get_latest_wtf_release()
            if latest_release:
                if latest_release['version'] != wtf_modpack_version:
                    file_size_mb = latest_release['size'] / (1024 * 1024)
                    
                    self.update_gui_status(
                        "🎉 Aggiornamento Disponibile!",
                        f"Nuova versione {latest_release['version']} trovata (dimensione: {file_size_mb:.1f} MB)",
                        f"Versione corrente: {wtf_modpack_version or 'Nessuna'}"
                    )
                    
                    result = askquestion(
                        "🎉 Aggiornamento Disponibile!",
                        f"📦 Nuova versione trovata: {latest_release['version']}\n" +
                        f"📋 Versione corrente: {wtf_modpack_version or 'Nessuna'}\n" +
                        f"📊 Dimensione download: {file_size_mb:.1f} MB\n\n" +
                        f"🔧 L'aggiornamento includerà:\n" +
                        f"   • Nuove mod e configurazioni\n" +
                        f"   • Correzioni di bug\n" +
                        f"   • Miglioramenti delle prestazioni\n\n" +
                        f"Vuoi procedere con l'aggiornamento?"
                    )
                    if result == 'yes':
                        self.download_and_install_modpack(latest_release)
                    else:
                        self.update_gui_status(
                            "❌ Aggiornamento Annullato",
                            "L'utente ha scelto di non aggiornare il modpack.",
                            "Puoi verificare nuovamente gli aggiornamenti in qualsiasi momento."
                        )
                else:
                    self.update_gui_status(
                        "✅ Versione Aggiornata",
                        f"Stai già utilizzando l'ultima versione disponibile: {wtf_modpack_version}",
                        f"Ultimo controllo: {time.strftime('%H:%M:%S')}"
                    )
                    showinfo("Nessun Aggiornamento", 
                            f"🎯 Perfetto! Stai già utilizzando l'ultima versione del WTF Modpack.\n\n" +
                            f"📋 Versione corrente: {wtf_modpack_version}\n" +
                            f"🕐 Ultimo controllo: {time.strftime('%H:%M:%S')}")
            else:
                self.update_gui_status(
                    "❌ Errore di Connessione",
                    "Impossibile contattare il repository GitHub.",
                    "Controlla la connessione Internet e riprova."
                )
                showerror("Errore di Connessione", 
                         "❌ Impossibile verificare gli aggiornamenti.\n\n" +
                         "Possibili cause:\n" +
                         "• Problemi di connessione Internet\n" +
                         "• Server GitHub temporaneamente non disponibile\n" +
                         "• Repository non accessibile\n\n" +
                         "Riprova tra qualche minuto.")
        except Exception as e:
            self.update_gui_status(
                "❌ Errore Imprevisto",
                f"Si è verificato un errore durante il controllo: {str(e)}",
                "Riprova o contatta il supporto se il problema persiste."
            )
            showerror("Errore Imprevisto", 
                     f"❌ Si è verificato un errore durante il controllo degli aggiornamenti:\n\n" +
                     f"🔧 Dettagli tecnici: {str(e)}\n\n" +
                     f"💡 Suggerimenti:\n" +
                     f"• Controlla la connessione Internet\n" +
                     f"• Riavvia il launcher\n" +
                     f"• Riprova tra qualche minuto")

    def install_modpack(self):
        """Install the WTF modpack"""
        if not connected:
            self.update_gui_status(
                "❌ Connessione Internet Richiesta",
                "È necessaria una connessione Internet per installare il modpack.",
                "Controlla la tua connessione e riprova."
            )
            showwarning("Connessione Internet Richiesta", 
                       "È necessaria una connessione Internet per installare il modpack.\n\n" +
                       "Il launcher deve scaricare:\n" +
                       "• Minecraft Forge 1.20.1-47.3.33\n" +
                       "• File mod del WTF Modpack\n" +
                       "• Configurazioni e risorse\n\n" +
                       "Controlla la tua connessione e riprova.")
            return

        self.update_gui_status(
            "🔍 Preparazione Installazione...",
            "Recuperando informazioni dell'ultima versione del modpack...",
            "Connessione al repository GitHub...",
            True
        )

        try:
            latest_release = get_latest_wtf_release()
            if latest_release:
                file_size_mb = latest_release['size'] / (1024 * 1024)
                
                self.update_gui_status(
                    "📦 Modpack Trovato",
                    f"Versione {latest_release['version']} disponibile per l'installazione",
                    f"Dimensione: {file_size_mb:.1f} MB"
                )
                
                result = askquestion(
                    "🎮 Installazione WTF Modpack",
                    f"📦 Versione da installare: {latest_release['version']}\n" +
                    f"📊 Dimensione download: {file_size_mb:.1f} MB\n" +
                    f"🎯 Versione Minecraft: {WTF_MC_VERSION}\n" +
                    f"⚙️ Forge richiesto: {WTF_FORGE_VERSION}\n" +
                    f"🎮 RAM minima: {WTF_MINIMUM_RAM}GB\n\n" +
                    f"🔧 Il processo includerà:\n" +
                    f"   1. Download e installazione di Minecraft Forge\n" +
                    f"   2. Download delle mod del modpack\n" +
                    f"   3. Configurazione automatica\n" +
                    f"   4. Preparazione per il primo avvio\n\n" +
                    f"⏱️ Tempo stimato: 3-10 minuti (dipende dalla connessione)\n\n" +
                    f"Vuoi procedere con l'installazione?"
                )
                if result == 'yes':
                    self.download_and_install_modpack(latest_release)
                else:
                    self.update_gui_status(
                        "❌ Installazione Annullata",
                        "L'utente ha scelto di non installare il modpack.",
                        "Puoi avviare l'installazione in qualsiasi momento."
                    )
            else:
                self.update_gui_status(
                    "❌ Errore Repository",
                    "Impossibile recuperare informazioni del modpack dal repository.",
                    "Controlla la connessione Internet e riprova."
                )
                showerror("Errore di Connessione", 
                         "❌ Impossibile recuperare le informazioni del modpack.\n\n" +
                         "Possibili cause:\n" +
                         "• Problemi di connessione Internet\n" +
                         "• Server GitHub temporaneamente non disponibile\n" +
                         "• Repository del modpack non accessibile\n\n" +
                         "💡 Suggerimenti:\n" +
                         "• Controlla la connessione Internet\n" +
                         "• Riprova tra qualche minuto\n" +
                         "• Verifica che GitHub sia accessibile")
        except Exception as e:
            self.update_gui_status(
                "❌ Errore Imprevisto",
                f"Errore durante il recupero informazioni: {str(e)}",
                "Riprova o contatta il supporto se il problema persiste."
            )
            showerror("Errore Imprevisto", 
                     f"❌ Si è verificato un errore durante il recupero delle informazioni:\n\n" +
                     f"🔧 Dettagli tecnici: {str(e)}\n\n" +
                     f"💡 Suggerimenti:\n" +
                     f"• Riavvia il launcher\n" +
                     f"• Controlla la connessione Internet\n" +
                     f"• Riprova tra qualche minuto")

    def download_and_install_modpack(self, release_info):
        """Download and install the modpack"""
        def install_thread():
            try:
                # Step 1: Install Forge
                self.window.after(0, lambda: self.update_gui_status(
                    "⚙️ Fase 1/4: Installazione Forge",
                    f"Installando Minecraft Forge {WTF_FORGE_VERSION}...",
                    "Download e configurazione componenti Forge in corso...",
                    True
                ))
                
                self.install_forge()
                
                # Step 2: Download modpack
                self.window.after(0, lambda: self.update_gui_status(
                    "📦 Fase 2/4: Download Modpack",
                    f"Scaricando WTF Modpack {release_info['version']} dal repository...",
                    f"Dimensione: {release_info['size'] / (1024*1024):.1f} MB",
                    True
                ))
                
                client_zip_path = os.path.join(currn_dir, "client.zip")
                self.download_file(release_info['download_url'], client_zip_path)
                
                # Step 3: Install mods
                self.window.after(0, lambda: self.update_gui_status(
                    "🔧 Fase 3/4: Installazione Mod",
                    "Estraendo e installando le mod nella directory Minecraft...",
                    "Configurazione mod e dipendenze in corso...",
                    True
                ))
                
                self.extract_and_install_mods(client_zip_path)
                
                # Step 4: Update configuration
                self.window.after(0, lambda: self.update_gui_status(
                    "⚙️ Fase 4/4: Configurazione Finale",
                    "Salvando configurazioni e impostazioni del launcher...",
                    "Preparazione completamento installazione...",
                    True
                ))
                
                # Update settings
                data["wtf_modpack_version"] = release_info['version']
                data["wtf_modpack_installed"] = True
                data["allocated_ram"] = f"{WTF_MINIMUM_RAM}G"
                
                with open("settings.json", "w") as f:
                    json.dump(data, f, indent=4)
                
                # Clean up
                self.window.after(0, lambda: self.update_gui_status(
                    "🧹 Pulizia File Temporanei",
                    "Rimozione file di installazione temporanei...",
                    "Finalizzazione installazione...",
                    True
                ))
                time.sleep(1)
                os.remove(client_zip_path)
                
                self.window.after(0, self.installation_complete, release_info['version'])
                
            except Exception as e:
                error_msg = str(e)
                self.window.after(0, lambda: self.update_gui_status(
                    "❌ Errore di Installazione",
                    f"L'installazione è fallita: {error_msg}",
                    "Controlla i dettagli e riprova l'installazione."
                ))
                self.window.after(0, lambda: showerror("❌ Errore di Installazione", 
                                                      f"❌ L'installazione del modpack è fallita.\n\n" +
                                                      f"🔧 Dettagli dell'errore:\n{error_msg}\n\n" +
                                                      f"💡 Possibili soluzioni:\n" +
                                                      f"• Verifica di avere spazio sufficiente sul disco\n" +
                                                      f"• Controlla che la connessione Internet sia stabile\n" +
                                                      f"• Assicurati di avere i permessi di scrittura\n" +
                                                      f"• Riprova l'installazione\n\n" +
                                                      f"Se il problema persiste, contatta il supporto."))
        
        # Start installation in thread
        install_thread_obj = Thread(target=install_thread)
        install_thread_obj.daemon = True
        install_thread_obj.start()

    def install_forge(self):
        """Install Forge for the modpack"""
        print(f"🔧 Inizio installazione Minecraft Forge {WTF_FORGE_VERSION}")
        
        callback = {
            "setStatus": lambda text: print(f"⚙️ Forge: {text}"),
            "setProgress": lambda value: print(f"📊 Progresso Forge: {value}%") if value else None,
            "setMax": lambda value: print(f"📋 Dimensione totale Forge: {value}") if value else None
        }
        
        try:
            # First, check if Minecraft 1.20.1 is installed
            if not minecraft_launcher_lib.utils.is_version_valid("1.20.1", mc_dir):
                print(f"📦 Installando Minecraft 1.20.1...")
                minecraft_launcher_lib.install.install_minecraft_version("1.20.1", mc_dir, callback=callback)
                print(f"✅ Minecraft 1.20.1 installato")
            
            # Then install Forge
            if supports_automatic_install(WTF_FORGE_VERSION):
                print(f"✅ Installazione automatica supportata per Forge {WTF_FORGE_VERSION}")
                install_forge_version(WTF_FORGE_VERSION, mc_dir, callback=callback)
                print(f"🎉 Forge {WTF_FORGE_VERSION} installato con successo!")
                
                # Verify installation
                if minecraft_launcher_lib.utils.is_version_valid(WTF_FORGE_VERSION, mc_dir):
                    print(f"✅ Installazione Forge verificata")
                else:
                    print(f"⚠️ Verifica installazione Forge fallita")
                    
            else:
                print(f"🔧 Avvio installer manuale per Forge {WTF_FORGE_VERSION}")
                run_forge_installer(WTF_FORGE_VERSION)
                print(f"⚠️ Completare l'installazione Forge manualmente se richiesto")
                
        except Exception as e:
            print(f"❌ Errore durante l'installazione di Forge: {str(e)}")
            # Try alternative installation method
            try:
                print(f"🔄 Tentativo installazione alternativa...")
                minecraft_launcher_lib.forge.run_forge_installer(WTF_FORGE_VERSION)
                print(f"✅ Installazione alternativa avviata")
            except Exception as e2:
                print(f"❌ Anche l'installazione alternativa è fallita: {str(e2)}")
                raise e

    def download_file(self, url, destination):
        """Download a file with progress tracking"""
        print(f"📦 Inizio download: {url}")
        print(f"💾 Destinazione: {destination}")
        
        try:
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            print(f"📊 Dimensione file: {total_size / (1024*1024):.1f} MB")
            
            with open(destination, 'wb') as file:
                downloaded = 0
                chunk_count = 0
                last_update = 0
                
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        chunk_count += 1
                        
                        # Update GUI every 500 chunks to avoid too frequent updates
                        if chunk_count - last_update >= 500 and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            downloaded_mb = downloaded / (1024*1024)
                            total_mb = total_size / (1024*1024)
                            
                            main_status = f"📦 Download in Corso: {progress:.1f}%"
                            detail_status = f"Scaricando WTF Modpack dal repository GitHub..."
                            progress_text = f"📊 {downloaded_mb:.1f}MB / {total_mb:.1f}MB • Velocità: {(downloaded/1024/1024)/(chunk_count*8192/1024/1024/10):.1f}MB/s"
                            
                            self.window.after(0, lambda ms=main_status, ds=detail_status, pt=progress_text: 
                                            self.update_gui_status(ms, ds, pt, True))
                            
                            last_update = chunk_count
            
            print(f"✅ Download completato: {destination}")
            
        except Exception as e:
            print(f"❌ Errore durante il download: {str(e)}")
            raise

    def extract_and_install_mods(self, zip_path):
        """Extract and install mods from client.zip"""
        print(f"📂 Inizio estrazione mod da: {zip_path}")
        
        mods_dir = os.path.join(mc_dir, "mods")
        print(f"📁 Directory mod: {mods_dir}")
        
        # Clear existing mods
        if os.path.exists(mods_dir):
            print(f"🧹 Rimozione mod esistenti...")
            rmtree(mods_dir)
            print(f"✅ Mod esistenti rimosse")
        
        os.makedirs(mods_dir, exist_ok=True)
        print(f"📁 Directory mod ricreata")
        
        # Extract zip file
        try:
            print(f"📦 Estrazione archizio modpack...")
            with ZipFile(zip_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                print(f"📋 File da estrarre: {len(file_list)}")
                
                for i, file in enumerate(file_list):
                    zip_ref.extract(file, mods_dir)
                    if i % 10 == 0:  # Update every 10 files
                        progress = (i / len(file_list)) * 100
                        print(f"📊 Estrazione: {i}/{len(file_list)} file ({progress:.1f}%)")
                        self.window.after(0, lambda p=progress: self.status_label.config(
                            text=f"🔧 Estrazione mod: {i}/{len(file_list)} file ({p:.1f}%)"
                        ))
                
                print(f"✅ Estrazione completata: {len(file_list)} file estratti")
                
                # Count extracted mod files
                mod_files = [f for f in os.listdir(mods_dir) if f.endswith('.jar')]
                print(f"🎮 Mod installate: {len(mod_files)} file .jar")
                
        except Exception as e:
            print(f"❌ Errore durante l'estrazione: {str(e)}")
            raise

    def installation_complete(self, version):
        """Called when installation is complete"""
        print(f"🎉 Installazione completata con successo!")
        print(f"📋 Versione installata: {version}")
        
        # Update GUI status
        self.update_modpack_status(installed=True, version=version)
        
        # Count installed mods for user info
        mods_dir = os.path.join(mc_dir, "mods")
        mod_count = 0
        if os.path.exists(mods_dir):
            mod_count = len([f for f in os.listdir(mods_dir) if f.endswith('.jar')])
        
        self.update_gui_status(
            "🎉 Installazione Completata con Successo!",
            f"WTF Modpack {version} è stato installato e configurato correttamente.",
            f"✅ Mod installate: {mod_count} • ⚙️ Forge: {WTF_FORGE_VERSION} • 💾 RAM: {WTF_MINIMUM_RAM}GB"
        )
        
        showinfo("🎉 Installazione Completata!", 
                f"✅ WTF Modpack {version} installato con successo!\n\n" +
                f"📊 Riepilogo installazione:\n" +
                f"   🎮 Versione Minecraft: {WTF_MC_VERSION}\n" +
                f"   ⚙️ Forge installato: {WTF_FORGE_VERSION}\n" +
                f"   📦 Mod installate: {mod_count} file\n" +
                f"   💾 RAM configurata: {WTF_MINIMUM_RAM}GB\n\n" +
                f"🚀 Ora puoi:\n" +
                f"   • Cliccare 'Play' per avviare Minecraft\n" +
                f"   • Modificare le impostazioni se necessario\n" +
                f"   • Verificare aggiornamenti futuri\n\n" +
                f"🎯 Il modpack è pronto per essere giocato!\n" +
                f"Buon divertimento! 🎮")

    def launch_minecraft(self):
        """Launch Minecraft with the modpack"""
        if not wtf_modpack_installed:
            showwarning("Modpack Non Installato", 
                       "❌ Il WTF Modpack non è ancora installato.\n\n" +
                       "🔧 Per iniziare a giocare devi prima:\n" +
                       "1. Cliccare su 'Installa WTF Modpack'\n" +
                       "2. Attendere il completamento dell'installazione\n" +
                       "3. Poi potrai cliccare su 'Play'\n\n" +
                       "💡 L'installazione richiede una connessione Internet attiva.")
            return
        
        if not username:
            showinfo("Configurazione Account", 
                    "🎮 Prima di giocare, devi configurare il tuo username!\n\n" +
                    "📋 Il launcher aprirà una finestra per inserire:\n" +
                    "• Il tuo username per Minecraft\n" +
                    "• Modalità di gioco offline\n\n" +
                    "⚠️ Nota: Questo launcher utilizza la modalità offline.\n" +
                    "Per giocare online con account Premium, usa il launcher ufficiale.")
            self.open_login_window()
            return
        
        def launch_thread():
            try:
                self.window.after(0, lambda: self.update_gui_status(
                    "🔍 Verifica Installazione...",
                    "Controllando che tutte le versioni necessarie siano installate...",
                    "Verifica Forge e Minecraft in corso..."
                ))
                
                # Check if Forge version exists
                forge_version = self.find_forge_version()
                if not forge_version:
                    self.window.after(0, lambda: self.update_gui_status(
                        "❌ Forge Non Trovato",
                        "La versione di Forge richiesta non è stata trovata.",
                        "Prova a reinstallare il modpack."
                    ))
                    self.window.after(0, lambda: showerror("❌ Forge Non Trovato", 
                                                          f"❌ Minecraft Forge {WTF_FORGE_VERSION} non è stato trovato.\n\n" +
                                                          f"💡 Possibili soluzioni:\n" +
                                                          f"• Reinstalla il modpack\n" +
                                                          f"• Verifica che l'installazione di Forge sia completata\n" +
                                                          f"• Controlla la directory .minecraft/versions\n\n" +
                                                          f"Il launcher proverà a reinstallare Forge automaticamente."))
                    return
                
                self.window.after(0, lambda: self.update_gui_status(
                    "🚀 Preparazione Avvio...",
                    f"Configurando Minecraft con Forge {forge_version}...",
                    "Preparazione parametri di gioco..."
                ))
                
                print(f"🎮 Avvio Minecraft per utente: {username}")
                print(f"📋 UUID utente: {uid}")
                print(f"⚙️ Versione Forge trovata: {forge_version}")
                
                # Set JVM arguments for minimum 4GB RAM
                ram_gb = max(WTF_MINIMUM_RAM, int(allocated_ram.rstrip('G')) if allocated_ram else WTF_MINIMUM_RAM)
                jvm_arguments = [f"-Xmx{ram_gb}G", f"-Xms{ram_gb}G"]
                
                print(f"💾 RAM allocata: {ram_gb}GB")
                print(f"⚙️ Argomenti JVM: {jvm_arguments}")
                
                self.window.after(0, lambda: self.update_gui_status(
                    "⚙️ Configurazione Parametri...",
                    "Impostando parametri di memoria e configurazioni di gioco...",
                    f"RAM: {ram_gb}GB • Username: {username}"
                ))
                
                options = {
                    "username": username,
                    "uuid": uid or str(uuid.uuid4()),
                    "token": accessToken or "",
                    "jvmArguments": jvm_arguments
                }
                
                print(f"🔧 Generazione comando di avvio...")
                
                # Generate launch command with found Forge version
                launch_command = minecraft_launcher_lib.command.get_minecraft_command(
                    forge_version, mc_dir, options
                )
                
                print(f"✅ Comando generato: {' '.join(launch_command[:3])}...")
                
                self.window.after(0, lambda: self.update_gui_status(
                    "🎮 Avvio Minecraft...",
                    "Minecraft si sta avviando con il WTF Modpack...",
                    "Caricamento in corso... Questo può richiedere alcuni minuti"
                ))
                
                print(f"🚀 Avvio Minecraft...")
                print(f"📂 Directory Minecraft: {mc_dir}")
                print(f"🎯 Questo potrebbe richiedere alcuni minuti al primo avvio...")
                
                # Launch Minecraft and store process
                self.minecraft_process = subprocess.Popen(launch_command)
                self.is_minecraft_running = True
                
                # Update play button immediately
                self.window.after(0, self.update_play_button)
                
                self.window.after(0, lambda: self.update_gui_status(
                    "🎮 Minecraft Avviato!",
                    "Il gioco è stato lanciato con successo.",
                    "Usa il pulsante 'Chiudi Gioco' per terminare Minecraft quando necessario"
                ))
                
                print(f"✅ Minecraft avviato con PID: {self.minecraft_process.pid}")
                
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Errore durante l'avvio di Minecraft: {error_msg}")
                self.window.after(0, lambda: self.update_gui_status(
                    "❌ Errore di Avvio",
                    f"Impossibile avviare Minecraft: {error_msg}",
                    "Controlla i dettagli dell'errore e riprova"
                ))
                self.window.after(0, lambda: showerror("❌ Errore di Avvio", 
                                                      f"❌ Impossibile avviare Minecraft.\n\n" +
                                                      f"🔧 Dettagli dell'errore:\n{error_msg}\n\n" +
                                                      f"💡 Possibili soluzioni:\n" +
                                                      f"• Verifica che Java sia installato correttamente\n" +
                                                      f"• Controlla che ci sia abbastanza RAM disponibile\n" +
                                                      f"• Assicurati che Forge sia installato correttamente\n" +
                                                      f"• Prova a reinstallare il modpack\n\n" +
                                                      f"Se il problema persiste, controlla i log di Minecraft."))
        
        # Show launch confirmation
        ram_gb = max(WTF_MINIMUM_RAM, int(allocated_ram.rstrip('G')) if allocated_ram else WTF_MINIMUM_RAM)
        
        result = askquestion("🚀 Avvio Minecraft", 
                           f"🎮 Pronto per avviare Minecraft con il WTF Modpack!\n\n" +
                           f"📋 Configurazione di gioco:\n" +
                           f"   👤 Username: {username}\n" +
                           f"   🎯 Modpack: {wtf_modpack_version}\n" +
                           f"   ⚙️ Forge: {WTF_FORGE_VERSION}\n" +
                           f"   💾 RAM: {ram_gb}GB\n" +
                           f"   🎮 Modalità: Offline\n\n" +
                           f"⏱️ Il primo avvio potrebbe richiedere alcuni minuti.\n" +
                           f"Minecraft si aprirà in una finestra separata.\n\n" +
                           f"Vuoi avviare il gioco?")
        
        if result == 'yes':
            showinfo("🎮 Avvio in Corso", 
                    "🚀 Minecraft si sta avviando...\n\n" +
                    "📋 Cosa aspettarsi:\n" +
                    "• Il caricamento può richiedere 2-5 minuti\n" +
                    "• Apparirà la schermata di caricamento Forge\n" +
                    "• Verranno caricate tutte le mod del modpack\n" +
                    "• Infine si aprirà il menu principale\n\n" +
                    "⚠️ Non chiudere questo launcher fino all'apertura di Minecraft!\n\n" +
                    "🎯 Buon divertimento con il WTF Modpack! 🎮")
            
            launch_thread_obj = Thread(target=launch_thread)
            launch_thread_obj.daemon = True
            launch_thread_obj.start()
        else:
            self.update_gui_status(
                "❌ Avvio Annullato",
                "L'utente ha scelto di non avviare Minecraft.",
                "Pronto per l'azione!"
            )

    def open_login_window(self):
        """Open login window for username input"""
        login_window = tk.Toplevel(self.window)
        login_window.title("🎮 Configurazione Account")
        login_window.geometry("450x300")
        login_window.configure(bg="#1c1c1c")
        login_window.resizable(False, False)
        
        # Center the window
        login_window.transient(self.window)
        login_window.grab_set()
        
        # Title
        tk.Label(login_window, text="🎮 Configurazione Account Minecraft", 
                bg="#1c1c1c", fg="#15d38f", font=self.custom_font3).pack(pady=15)
        
        # Description
        tk.Label(login_window, text="Inserisci il tuo username per giocare in modalità offline.", 
                bg="#1c1c1c", fg="white", font=self.custom_font4).pack(pady=5)
        
        tk.Label(login_window, text="L'username può essere qualsiasi nome a tua scelta.", 
                bg="#1c1c1c", fg="gray", font=self.custom_font4).pack(pady=5)
        
        # Username input
        tk.Label(login_window, text="👤 Username:", bg="#1c1c1c", fg="white", font=self.custom_font4).pack(pady=(15, 5))
        
        username_entry = tk.Entry(login_window, width=25, font=self.custom_font4, justify='center')
        username_entry.pack(pady=5)
        username_entry.focus()
        
        # Instructions
        tk.Label(login_window, text="💡 Suggerimenti:", 
                bg="#1c1c1c", fg="yellow", font=self.custom_font4).pack(pady=(15, 5))
        tk.Label(login_window, text="• Usa solo lettere, numeri e underscore", 
                bg="#1c1c1c", fg="gray", font=("Arial", 9)).pack()
        tk.Label(login_window, text="• Evita spazi e caratteri speciali", 
                bg="#1c1c1c", fg="gray", font=("Arial", 9)).pack()
        tk.Label(login_window, text="• Lunghezza consigliata: 3-16 caratteri", 
                bg="#1c1c1c", fg="gray", font=("Arial", 9)).pack()
        
        def save_username():
            global username, uid
            entered_username = username_entry.get().strip()
            
            if not entered_username:
                tk.messagebox.showerror("❌ Errore", 
                                       "⚠️ Devi inserire un username!\n\n" +
                                       "L'username è necessario per identificarti nel gioco.")
                username_entry.focus()
                return
            
            if len(entered_username) < 3:
                tk.messagebox.showerror("❌ Username Troppo Corto", 
                                       "⚠️ L'username deve essere di almeno 3 caratteri.\n\n" +
                                       "Inserisci un username più lungo.")
                username_entry.focus()
                return
            
            if len(entered_username) > 16:
                tk.messagebox.showerror("❌ Username Troppo Lungo", 
                                       "⚠️ L'username non può superare i 16 caratteri.\n\n" +
                                       "Inserisci un username più corto.")
                username_entry.focus()
                return
            
            # Check for invalid characters
            import re
            if not re.match("^[a-zA-Z0-9_]+$", entered_username):
                tk.messagebox.showerror("❌ Caratteri Non Validi", 
                                       "⚠️ L'username può contenere solo:\n" +
                                       "• Lettere (a-z, A-Z)\n" +
                                       "• Numeri (0-9)\n" +
                                       "• Underscore (_)\n\n" +
                                       "Rimuovi spazi e caratteri speciali.")
                username_entry.focus()
                return
            
            username = entered_username
            uid = str(uuid.uuid4())
            
            print(f"👤 Username configurato: {username}")
            print(f"🆔 UUID generato: {uid}")
            
            data["User-info"][0]["username"] = username
            data["User-info"][0]["UUID"] = uid
            data["User-info"][0]["AUTH_TYPE"] = "offline"
            
            with open("settings.json", "w") as f:
                json.dump(data, f, indent=4)
            
            print(f"💾 Configurazione salvata nel file settings.json")
            
            tk.messagebox.showinfo("✅ Configurazione Salvata", 
                                  f"🎉 Account configurato con successo!\n\n" +
                                  f"👤 Username: {username}\n" +
                                  f"🎮 Modalità: Offline\n" +
                                  f"💾 Configurazione salvata\n\n" +
                                  f"Ora Minecraft verrà avviato!")
            
            login_window.destroy()
            self.launch_minecraft()
        
        def on_enter(event):
            save_username()
        
        username_entry.bind('<Return>', on_enter)
        
        # Buttons frame
        button_frame = tk.Frame(login_window, bg="#1c1c1c")
        button_frame.pack(pady=20)
        
        Button(button_frame, text="🎮 Conferma e Gioca", command=save_username, 
               bootstyle="success-outline").pack(side=tk.LEFT, padx=10)
        
        Button(button_frame, text="❌ Annulla", command=login_window.destroy, 
               bootstyle="danger-outline").pack(side=tk.LEFT, padx=10)

    def open_settings(self):
        """Open settings window"""
        settings_window = tk.Toplevel(self.window)
        settings_window.title("⚙️ Impostazioni WTF Modpack")
        settings_window.geometry("600x500")
        settings_window.configure(bg="#1c1c1c")
        settings_window.resizable(False, False)
        
        # Center the window
        settings_window.transient(self.window)
        settings_window.grab_set()
        
        # Main container with padding
        main_frame = tk.Frame(settings_window, bg="#1c1c1c")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="⚙️ IMPOSTAZIONI LAUNCHER", 
                              bg="#1c1c1c", fg="#15d38f", font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Username Section
        username_frame = tk.Frame(main_frame, bg="#2d2d2d", relief="solid", bd=1)
        username_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(username_frame, text="👤 CONFIGURAZIONE ACCOUNT", 
                bg="#2d2d2d", fg="#15d38f", font=("Arial", 12, "bold")).pack(pady=(10, 5))
        
        current_username = username if username else "Non configurato"
        tk.Label(username_frame, text=f"Username attuale: {current_username}", 
                bg="#2d2d2d", fg="white", font=("Arial", 10)).pack(pady=5)
        
        username_input_frame = tk.Frame(username_frame, bg="#2d2d2d")
        username_input_frame.pack(pady=10)
        
        tk.Label(username_input_frame, text="Nuovo username:", 
                bg="#2d2d2d", fg="white", font=("Arial", 10)).pack(side="left", padx=(10, 5))
        
        self.username_var = tk.StringVar(value=username if username else "")
        username_entry = tk.Entry(username_input_frame, textvariable=self.username_var, 
                                 width=20, font=("Arial", 10))
        username_entry.pack(side="left", padx=5)
        
        def change_username():
            new_username = self.username_var.get().strip()
            if not new_username:
                tk.messagebox.showerror("Errore", "Inserisci un username valido!")
                return
                
            if len(new_username) < 3 or len(new_username) > 16:
                tk.messagebox.showerror("Errore", "L'username deve essere tra 3 e 16 caratteri!")
                return
                
            if not re.match("^[a-zA-Z0-9_]+$", new_username):
                tk.messagebox.showerror("Errore", "L'username può contenere solo lettere, numeri e underscore!")
                return
            
            global username, uid
            username = new_username
            uid = str(uuid.uuid4())
            
            data["User-info"][0]["username"] = username
            data["User-info"][0]["UUID"] = uid
            data["User-info"][0]["AUTH_TYPE"] = "offline"
            
            with open("settings.json", "w") as f:
                json.dump(data, f, indent=4)
            
            tk.messagebox.showinfo("Successo", f"Username cambiato in: {username}")
            settings_window.destroy()
        
        Button(username_input_frame, text="Cambia", command=change_username, 
               bootstyle="info-outline", width=8).pack(side="left", padx=5)
        
        tk.Label(username_frame, text="", bg="#2d2d2d").pack(pady=5)  # Spacer
        
        # RAM Section
        ram_frame = tk.Frame(main_frame, bg="#2d2d2d", relief="solid", bd=1)
        ram_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(ram_frame, text="💾 GESTIONE MEMORIA RAM", 
                bg="#2d2d2d", fg="#15d38f", font=("Arial", 12, "bold")).pack(pady=(10, 5))
        
        # Current RAM info
        current_ram = allocated_ram.rstrip('G') if allocated_ram else str(WTF_MINIMUM_RAM)
        tk.Label(ram_frame, text=f"RAM attualmente allocata: {current_ram}GB", 
                bg="#2d2d2d", fg="white", font=("Arial", 10)).pack(pady=5)
        
        # System RAM info
        total_ram_gb = int(svmem.total / (1024**3))
        available_ram_gb = int(svmem.available / (1024**3))
        tk.Label(ram_frame, text=f"RAM sistema: {total_ram_gb}GB totali, {available_ram_gb}GB disponibili", 
                bg="#2d2d2d", fg="#b0b0b0", font=("Arial", 9)).pack(pady=2)
        
        # RAM input
        ram_input_frame = tk.Frame(ram_frame, bg="#2d2d2d")
        ram_input_frame.pack(pady=10)
        
        tk.Label(ram_input_frame, text="Nuova allocazione RAM (GB):", 
                bg="#2d2d2d", fg="white", font=("Arial", 10)).pack(side="left", padx=(10, 5))
        
        ram_var = tk.StringVar(value=current_ram)
        ram_entry = tk.Entry(ram_input_frame, textvariable=ram_var, width=5, font=("Arial", 10))
        ram_entry.pack(side="left", padx=5)
        
        tk.Label(ram_input_frame, text=f"(Min: {WTF_MINIMUM_RAM}GB)", 
                bg="#2d2d2d", fg="yellow", font=("Arial", 9)).pack(side="left", padx=5)
        
        tk.Label(ram_frame, text="", bg="#2d2d2d").pack(pady=5)  # Spacer
        
        # System Info Section
        system_frame = tk.Frame(main_frame, bg="#2d2d2d", relief="solid", bd=1)
        system_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(system_frame, text="💻 INFORMAZIONI SISTEMA", 
                bg="#2d2d2d", fg="#15d38f", font=("Arial", 12, "bold")).pack(pady=(10, 5))
        
        # System details
        info_items = [
            ("Sistema Operativo:", platform.platform()),
            ("Minecraft Directory:", mc_dir),
            ("Versione Modpack:", wtf_modpack_version if wtf_modpack_version else "Non installato"),
            ("Versione Forge:", WTF_FORGE_VERSION),
            ("Stato Connessione:", "Online" if connected else "Offline")
        ]
        
        for label, value in info_items:
            info_frame = tk.Frame(system_frame, bg="#2d2d2d")
            info_frame.pack(fill="x", padx=10, pady=2)
            
            tk.Label(info_frame, text=label, bg="#2d2d2d", fg="#b0b0b0", 
                    font=("Arial", 9), anchor="w").pack(side="left")
            tk.Label(info_frame, text=value, bg="#2d2d2d", fg="white", 
                    font=("Arial", 9), anchor="w", wraplength=350).pack(side="right")
        
        tk.Label(system_frame, text="", bg="#2d2d2d").pack(pady=5)  # Spacer
        
        # Advanced Settings Section
        advanced_frame = tk.Frame(main_frame, bg="#2d2d2d", relief="solid", bd=1)
        advanced_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(advanced_frame, text="🔧 IMPOSTAZIONI AVANZATE", 
                bg="#2d2d2d", fg="#15d38f", font=("Arial", 12, "bold")).pack(pady=(10, 5))
        
        # Directory buttons
        button_frame = tk.Frame(advanced_frame, bg="#2d2d2d")
        button_frame.pack(pady=10)
        
        def open_minecraft_folder():
            try:
                if os.path.exists(mc_dir):
                    os.startfile(mc_dir)
                else:
                    tk.messagebox.showerror("Errore", "Directory Minecraft non trovata!")
            except Exception as e:
                tk.messagebox.showerror("Errore", f"Impossibile aprire la directory: {str(e)}")
        
        def open_logs_folder():
            try:
                logs_dir = os.path.join(mc_dir, "logs")
                if os.path.exists(logs_dir):
                    os.startfile(logs_dir)
                else:
                    tk.messagebox.showwarning("Avviso", "Directory logs non trovata. Avvia Minecraft almeno una volta.")
            except Exception as e:
                tk.messagebox.showerror("Errore", f"Impossibile aprire i logs: {str(e)}")
        
        Button(button_frame, text="📂 Apri Cartella Minecraft", command=open_minecraft_folder, 
               bootstyle="secondary-outline", width=20).pack(side="left", padx=5)
        
        Button(button_frame, text="📜 Apri Logs", command=open_logs_folder, 
               bootstyle="secondary-outline", width=15).pack(side="left", padx=5)
        
        tk.Label(advanced_frame, text="", bg="#2d2d2d").pack(pady=5)  # Spacer
        
        # Bottom buttons
        button_bottom_frame = tk.Frame(main_frame, bg="#1c1c1c")
        button_bottom_frame.pack(fill="x", pady=(10, 0))
        
        def save_settings():
            global allocated_ram
            try:
                ram_value = int(ram_var.get())
                if ram_value < WTF_MINIMUM_RAM:
                    tk.messagebox.showwarning("RAM Insufficiente", 
                                            f"Il WTF Modpack richiede almeno {WTF_MINIMUM_RAM}GB di RAM.\n" +
                                            f"Hai inserito {ram_value}GB che potrebbero causare problemi di prestazioni.")
                    result = tk.messagebox.askquestion("Conferma", "Vuoi comunque salvare questa impostazione?")
                    if result != 'yes':
                        return
                
                if ram_value > total_ram_gb:
                    tk.messagebox.showerror("RAM Eccessiva", 
                                          f"Non puoi allocare più RAM di quella disponibile sul sistema!\n" +
                                          f"RAM sistema: {total_ram_gb}GB\n" +
                                          f"RAM richiesta: {ram_value}GB")
                    return
                
                allocated_ram = f"{ram_value}G"
                data["allocated_ram"] = allocated_ram
                data["setting-info"][0]["allocated_ram_selected"] = allocated_ram
                
                with open("settings.json", "w") as f:
                    json.dump(data, f, indent=4)
                
                tk.messagebox.showinfo("✅ Impostazioni Salvate", 
                                     f"Impostazioni salvate con successo!\n\n" +
                                     f"• RAM allocata: {ram_value}GB\n" +
                                     f"• Username: {username if username else 'Non configurato'}\n\n" +
                                     f"Le modifiche saranno applicate al prossimo avvio di Minecraft.")
                settings_window.destroy()
                
                # Update system info in main GUI
                total_ram = get_size(svmem.total)
                system_info = f"RAM: {total_ram} | Allocata: {allocated_ram}"
                self.canvas.itemconfig(self.system_info_text, text=system_info)
                
            except ValueError:
                tk.messagebox.showerror("Valore Non Valido", "Inserisci un numero valido per la RAM!")
        
        def reset_settings():
            result = tk.messagebox.askquestion("⚠️ Conferma Reset", 
                                             "Sei sicuro di voler ripristinare le impostazioni predefinite?\n\n" +
                                             "Questo resetterà:\n" +
                                             "• Allocazione RAM al minimo\n" +
                                             "• Username (dovrai riconfigurarlo)\n" +
                                             "• Altre impostazioni del launcher")
            if result == 'yes':
                global username, uid, allocated_ram
                username = None
                uid = None
                allocated_ram = f"{WTF_MINIMUM_RAM}G"
                
                data["User-info"][0]["username"] = None
                data["User-info"][0]["UUID"] = None
                data["allocated_ram"] = allocated_ram
                data["setting-info"][0]["allocated_ram_selected"] = allocated_ram
                
                with open("settings.json", "w") as f:
                    json.dump(data, f, indent=4)
                
                tk.messagebox.showinfo("✅ Reset Completato", "Impostazioni ripristinate ai valori predefiniti!")
                settings_window.destroy()
        
        # Bottom buttons
        Button(button_bottom_frame, text="💾 Salva Impostazioni", command=save_settings, 
               bootstyle="success", width=18).pack(side="left", padx=(0, 10))
        
        Button(button_bottom_frame, text="🔄 Reset Predefiniti", command=reset_settings, 
               bootstyle="warning", width=18).pack(side="left", padx=10)
        
        Button(button_bottom_frame, text="❌ Chiudi", command=settings_window.destroy, 
               bootstyle="danger", width=10).pack(side="right")
        tk.Label(settings_window, text="RAM Allocation (GB):", bg="#1c1c1c", fg="white", font=self.custom_font3).pack(pady=10)
        
        ram_var = tk.StringVar(value=allocated_ram.rstrip('G') if allocated_ram else str(WTF_MINIMUM_RAM))
        ram_entry = tk.Entry(settings_window, textvariable=ram_var, width=10, font=self.custom_font4)
        ram_entry.pack(pady=5)
        
        tk.Label(settings_window, text=f"Minimum required: {WTF_MINIMUM_RAM}GB", bg="#1c1c1c", fg="yellow", font=self.custom_font4).pack()
        
        # Minecraft directory display
        tk.Label(settings_window, text="Minecraft Directory:", bg="#1c1c1c", fg="white", font=self.custom_font4).pack(pady=(20, 5))
        tk.Label(settings_window, text=mc_dir, bg="#1c1c1c", fg="#15d38f", font=self.custom_font4, wraplength=450).pack()
        
        def save_settings():
            global allocated_ram
            try:
                ram_value = int(ram_var.get())
                if ram_value < WTF_MINIMUM_RAM:
                    showwarning("Invalid RAM", f"Minimum {WTF_MINIMUM_RAM}GB required for WTF Modpack")
                    return
                
                allocated_ram = f"{ram_value}G"
                data["allocated_ram"] = allocated_ram
                data["setting-info"][0]["allocated_ram_selected"] = allocated_ram
                
                with open("settings.json", "w") as f:
                    json.dump(data, f, indent=4)
                
                showinfo("Settings Saved", "Settings have been saved successfully!")
                settings_window.destroy()
                
            except ValueError:
                showerror("Invalid Input", "Please enter a valid number for RAM allocation.")
        
        Button(settings_window, text="Save", command=save_settings, bootstyle="success-outline").pack(pady=20)

    def run(self):
        """Start the launcher"""
        self.window.mainloop()

    def update_gui_status(self, main_status, detail_status="", progress_text="", show_progress=False):
        """Update the GUI with detailed status information"""
        self.status_label.config(text=main_status)
        self.detail_label.config(text=detail_status)
        self.progress_label.config(text=progress_text)
        
        if show_progress:
            if not self.progress_bar.winfo_viewable():
                self.progress_bar.place(x=200, y=340, width=600, height=20)
                self.progress_bar.start()
        else:
            if self.progress_bar.winfo_viewable():
                self.progress_bar.place_forget()
                self.progress_bar.stop()
        
        self.window.update()

    def update_modpack_status(self, installed=None, version=None):
        """Update modpack status in the GUI"""
        if installed is not None:
            global wtf_modpack_installed
            wtf_modpack_installed = installed
            
        if version is not None:
            global wtf_modpack_version
            wtf_modpack_version = version
            
        # Update version text
        version_display = f"{wtf_modpack_version if wtf_modpack_version else 'Non Installato'}"
        self.canvas.itemconfig(self.version_text, text=version_display)
        
        # Update status indicator
        if wtf_modpack_installed:
            status_text = "✅ Pronto per Giocare"
            status_color = "#15d38f"
            button_text = "🔄 Verifica Aggiornamenti"
            button_style = "info"
            play_text = self.get_play_button_text()
            play_state = "normal"
            
            # Show repair button if modpack is installed
            if not hasattr(self, 'repair_button'):
                self.repair_button = Button(
                    self.window,
                    text="🔧 Ripara",
                    command=self.verify_and_repair_installation,
                    bootstyle="secondary"
                )
            self.repair_button.place(x=790, y=280, width=100, height=45)
            
        else:
            status_text = "⚠️ Installazione Richiesta"
            status_color = "#ffa502"
            button_text = "📦 Installa WTF Modpack"
            button_style = "primary"
            play_text = "🚫 Installa Prima il Modpack"
            play_state = "disabled"
            
            # Hide repair button if modpack is not installed
            if hasattr(self, 'repair_button'):
                self.repair_button.place_forget()
            
        self.canvas.itemconfig(self.modpack_status_text, text=status_text, fill=status_color)
        self.install_button.config(text=button_text, bootstyle=button_style)
        self.play_button.config(text=play_text, state=play_state)

    def update_connection_status(self, is_connected):
        """Update connection status indicator"""
        global connected
        connected = is_connected
        
        connection_status = "🟢 Online" if connected else "🔴 Offline"
        connection_color = "#15d38f" if connected else "#ff4757"
        
        self.canvas.itemconfig(self.connection_text, text=connection_status, fill=connection_color)

    def find_forge_version(self):
        """Find the installed Forge version"""
        try:
            import minecraft_launcher_lib
            
            # Check if the exact version exists
            if minecraft_launcher_lib.utils.is_version_valid(WTF_FORGE_VERSION, mc_dir):
                print(f"✅ Versione Forge trovata: {WTF_FORGE_VERSION}")
                return WTF_FORGE_VERSION
            
            # Look for alternative Forge versions
            versions = minecraft_launcher_lib.utils.get_installed_versions(mc_dir)
            forge_versions = []
            
            for version in versions:
                if "forge" in version["id"].lower() and "1.20.1" in version["id"]:
                    forge_versions.append(version["id"])
                    print(f"🔍 Versione Forge alternativa trovata: {version['id']}")
            
            if forge_versions:
                # Use the first available Forge version for 1.20.1
                selected_version = forge_versions[0]
                print(f"✅ Utilizzando versione Forge: {selected_version}")
                return selected_version
            
            # Check for vanilla 1.20.1
            if minecraft_launcher_lib.utils.is_version_valid("1.20.1", mc_dir):
                print(f"⚠️ Forge non trovato, utilizzando Minecraft vanilla 1.20.1")
                showwarning("Forge Non Trovato", 
                           "⚠️ Minecraft Forge non è stato trovato.\n\n" +
                           "Il launcher avvierà Minecraft vanilla senza mod.\n" +
                           "Per utilizzare le mod, reinstalla il modpack.")
                return "1.20.1"
            
            print(f"❌ Nessuna versione valida trovata per 1.20.1")
            return None
            
        except Exception as e:
            print(f"❌ Errore durante la ricerca versioni: {str(e)}")
            return None

    def verify_and_repair_installation(self):
        """Verify and repair the modpack installation"""
        try:
            self.update_gui_status(
                "🔍 Verifica Installazione...",
                "Controllando l'integrità dell'installazione del modpack...",
                "Verifica componenti in corso...",
                True
            )
            
            issues_found = []
            
            # Check Minecraft directory
            if not os.path.exists(mc_dir):
                issues_found.append("Directory .minecraft mancante")
                
            # Check mods directory
            mods_dir = os.path.join(mc_dir, "mods")
            if not os.path.exists(mods_dir):
                issues_found.append("Directory mods mancante")
            else:
                mod_files = [f for f in os.listdir(mods_dir) if f.endswith('.jar')]
                if len(mod_files) == 0:
                    issues_found.append("Nessuna mod trovata")
                    
            # Check Forge installation
            forge_version = self.find_forge_version()
            if not forge_version:
                issues_found.append("Minecraft Forge non installato")
                
            if issues_found:
                self.update_gui_status(
                    "⚠️ Problemi Trovati",
                    f"Trovati {len(issues_found)} problemi nell'installazione",
                    "Riparazione necessaria"
                )
                
                result = askquestion("🔧 Riparazione Necessaria",
                                   f"⚠️ Trovati i seguenti problemi:\n\n" +
                                   "\n".join(f"• {issue}" for issue in issues_found) +
                                   f"\n\nVuoi che il launcher ripari automaticamente questi problemi?")
                
                if result == 'yes':
                    return self.repair_installation()
                else:
                    return False
            else:
                self.update_gui_status(
                    "✅ Installazione Verificata",
                    "Tutti i componenti del modpack sono installati correttamente",
                    "Nessun problema trovato"
                )
                return True
                
        except Exception as e:
            self.update_gui_status(
                "❌ Errore durante la verifica",
                f"Si è verificato un errore durante la verifica: {str(e)}",
                "Verifica fallita"
            )
            print(f"❌ Errore durante la verifica dell'installazione: {str(e)}")
            return False

    def run(self):
        """Start the launcher"""
        self.window.mainloop()

    def update_gui_status(self, main_status, detail_status="", progress_text="", show_progress=False):
        """Update the GUI with detailed status information"""
        self.status_label.config(text=main_status)
        self.detail_label.config(text=detail_status)
        self.progress_label.config(text=progress_text)
        
        if show_progress:
            if not self.progress_bar.winfo_viewable():
                self.progress_bar.place(x=200, y=340, width=600, height=20)
                self.progress_bar.start()
        else:
            if self.progress_bar.winfo_viewable():
                self.progress_bar.place_forget()
                self.progress_bar.stop()
        
        self.window.update()

    def update_modpack_status(self, installed=None, version=None):
        """Update modpack status in the GUI"""
        if installed is not None:
            global wtf_modpack_installed
            wtf_modpack_installed = installed
            
        if version is not None:
            global wtf_modpack_version
            wtf_modpack_version = version
            
        # Update version text
        version_display = f"{wtf_modpack_version if wtf_modpack_version else 'Non Installato'}"
        self.canvas.itemconfig(self.version_text, text=version_display)
        
        # Update status indicator
        if wtf_modpack_installed:
            status_text = "✅ Pronto per Giocare"
            status_color = "#15d38f"
            button_text = "🔄 Verifica Aggiornamenti"
            button_style = "info"
            play_text = "🎮 Gioca Ora!"
            play_state = "normal"
            
            # Show repair button if modpack is installed
            if not hasattr(self, 'repair_button'):
                self.repair_button = Button(
                    self.window,
                    text="🔧 Ripara",
                    command=self.verify_and_repair_installation,
                    bootstyle="secondary",
                    width=12
                )
            self.repair_button.place(x=790, y=280, width=100, height=45)
            
        else:
            status_text = "⚠️ Installazione Richiesta"
            status_color = "#ffa502"
            button_text = "📦 Installa WTF Modpack"
            button_style = "primary"
            play_text = "🚫 Installa Prima il Modpack"
            play_state = "disabled"
            
            # Hide repair button if modpack is not installed
            if hasattr(self, 'repair_button'):
                self.repair_button.place_forget()
            
        self.canvas.itemconfig(self.modpack_status_text, text=status_text, fill=status_color)
        self.install_button.config(text=button_text, bootstyle=button_style)
        if not self.is_minecraft_running:
            self.play_button.config(text=play_text, state=play_state)

    def update_connection_status(self, is_connected):
        """Update connection status indicator"""
        global connected
        connected = is_connected
        
        connection_status = "Online" if connected else "Offline"
        connection_color = "white" if connected else "#ff4757"
        
        self.canvas.itemconfig(self.connection_text, text=connection_status, fill=connection_color)

    def find_forge_version(self):
        """Find the installed Forge version"""
        try:
            versions_dir = os.path.join(mc_dir, "versions")
            if os.path.exists(versions_dir):
                # Look for the exact Forge version first
                if os.path.exists(os.path.join(versions_dir, WTF_FORGE_VERSION)):
                    return WTF_FORGE_VERSION
                
                # Look for any Forge version for 1.20.1
                for version_folder in os.listdir(versions_dir):
                    if "1.20.1" in version_folder and "forge" in version_folder.lower():
                        json_file = os.path.join(versions_dir, version_folder, f"{version_folder}.json")
                        if os.path.exists(json_file):
                            return version_folder
                
                # Fallback to vanilla 1.20.1 if available
                if os.path.exists(os.path.join(versions_dir, "1.20.1")):
                    return "1.20.1"
                    
            return None
                        
        except Exception as e:
            print(f"❌ Errore nella ricerca versione Forge: {str(e)}")
            return None

    def verify_and_repair_installation(self):
        """Verify and repair the modpack installation"""
        try:
            result = askquestion("🔧 Riparazione Installazione", 
                               "🔍 Verifica e ripara l'installazione del WTF Modpack.\n\n" +
                               "Questo processo:\n" +
                               "• Controllerà l'integrità dei file installati\n" +
                               "• Reinstallerà componenti mancanti\n" +
                               "• Riparerà eventuali configurazioni corrotte\n\n" +
                               "⏱️ Il processo può richiedere alcuni minuti.\n" +
                               "Vuoi procedere?")
            
            if result == 'yes':
                def repair_thread():
                    try:
                        self.window.after(0, lambda: self.update_gui_status(
                            "🔍 Verifica Installazione...",
                            "Controllando l'integrità dei file del modpack...",
                            "Analisi componenti in corso...",
                            True
                        ))
                        
                        # Check Minecraft installation
                        mc_installed = minecraft_launcher_lib.utils.is_version_valid("1.20.1", mc_dir)
                        
                        # Check Forge installation
                        forge_installed = self.find_forge_version() is not None
                        
                        # Check mods directory
                        mods_dir = os.path.join(mc_dir, "mods")
                        mods_count = 0
                        if os.path.exists(mods_dir):
                            mods_count = len([f for f in os.listdir(mods_dir) if f.endswith('.jar')])
                        
                        issues_found = []
                        if not mc_installed:
                            issues_found.append("Minecraft 1.20.1 non installato")
                        if not forge_installed:
                            issues_found.append("Minecraft Forge non trovato")
                        if mods_count == 0:
                            issues_found.append("Mod del modpack mancanti")
                        
                        if issues_found:
                            self.window.after(0, lambda: self.update_gui_status(
                                "⚠️ Problemi Rilevati",
                                f"Trovati {len(issues_found)} problemi da risolvere",
                                "Avvio riparazione automatica...",
                                True
                            ))
                            
                            # Auto-repair by reinstalling
                            latest_release = get_latest_wtf_release()
                            if latest_release:
                                self.window.after(0, lambda: self.download_and_install_modpack(latest_release))
                            else:
                                self.window.after(0, lambda: showerror("Errore Riparazione", 
                                                                      "Impossibile riparare: repository non raggiungibile."))
                        else:
                            self.window.after(0, lambda: self.update_gui_status(
                                "✅ Installazione Verificata",
                                "L'installazione del modpack è corretta e completa.",
                                f"Componenti verificati: Minecraft ✓ Forge ✓ Mod ({mods_count}) ✓"
                            ))
                            
                            self.window.after(0, lambda: showinfo("✅ Verifica Completata", 
                                                                 f"🎯 L'installazione del WTF Modpack è perfetta!\n\n" +
                                                                 f"📊 Componenti verificati:\n" +
                                                                 f"   ✅ Minecraft 1.20.1\n" +
                                                                 f"   ✅ Minecraft Forge\n" +
                                                                 f"   ✅ {mods_count} mod installate\n\n" +
                                                                 f"🎮 Il modpack è pronto per essere giocato!"))
                        
                    except Exception as e:
                        error_msg = str(e)
                        self.window.after(0, lambda: self.update_gui_status(
                            "❌ Errore Verifica",
                            f"Errore durante la verifica: {error_msg}",
                            "Controlla i dettagli dell'errore"
                        ))
                        self.window.after(0, lambda: showerror("❌ Errore Verifica", 
                                                              f"Si è verificato un errore durante la verifica:\n\n{error_msg}"))
                
                repair_thread_obj = Thread(target=repair_thread, daemon=True)
                repair_thread_obj.start()
                
        except Exception as e:
            print(f"❌ Errore durante la verifica: {str(e)}")
            return False


# Main execution
if __name__ == "__main__":
    try:
        print("🌐 Verifica connessione Internet...")
        check_internet()
        
        print("🚀 Avvio WTF Modpack Launcher...")
        launcher = WTFModpackLauncher()
        print("✅ GUI caricata con successo!")
        launcher.window.mainloop()
        
    except Exception as e:
        print(f"❌ Errore critico durante l'avvio: {str(e)}")
        import traceback
        traceback.print_exc()
        input("Premi Invio per chiudere...")
