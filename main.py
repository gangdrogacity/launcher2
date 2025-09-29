import tkinter as tk
from tkinter import Canvas, Entry, StringVar
from tkinter.font import Font
from tkinter.messagebox import showerror, showinfo, showwarning, askquestion
from tkinter.ttk import Progressbar, Frame, Label, Button

import os
import sys
import subprocess
import time
import minecraft_launcher_lib
from minecraft_launcher_lib.forge import install_forge_version, run_forge_installer, supports_automatic_install
import uuid
import platform
from ttkbootstrap import Style
import json
from threading import Thread
import requests
from zipfile import ZipFile
from shutil import rmtree
import psutil
import re

# Import launcher updater
try:
    from updater import LauncherUpdater
except ImportError:
    print("⚠️ Modulo updater non trovato. Funzionalità di autoaggiornamento disabilitata.")
    LauncherUpdater = None

print("🚀 Avvio WTF Modpack Launcher v1.0...")
print("⏳ Caricamento componenti, attendere prego...")
print("✅ Componenti caricati!")
print("🎮 Preparazione interfaccia grafica...")

style = Style(theme="flatly")
style.configure("TNotebook.Tab", foreground="#15d38f", background="#23272a", bordercolor="#072A6C")

currn_dir = os.getcwd()
mc_dir = r"{}/.minecraft".format(currn_dir)
OS = platform.platform()

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# WTF Modpack specific settings
WTF_MODPACK_REPO = "https://github.com/jamnaga/wtf-modpack"
WTF_LATEST_RELEASE_API = "https://api.github.com/repos/jamnaga/wtf-modpack/releases/latest"
WTF_FORGE_VERSION = "1.20.1-47.3.33"
WTF_MC_VERSION = "1.20.1"
WTF_MINIMUM_RAM = 4  # 4GB minimum


def get_size(bytes, suffix="B"):
    """Scale bytes to its proper format"""
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
settings_base = {
    "accessToken": None,
    "clientToken": None,
    "User-info": [{"username": None, "AUTH_TYPE": None, "UUID": None}],
    "PC-info": [{"OS": platform.platform(), "Total-Ram": f"{get_size(svmem.total)}"}],
    "Minecraft-home": mc_dir,
    "selected-version": f"WTF Modpack - Forge {WTF_FORGE_VERSION}",
    "Tor-Enabled": False,
    "setting-info": [{"tor_enabled_selected": False, "allocated_ram_selected": f"{WTF_MINIMUM_RAM}G"}],
    "allocated_ram": f"{WTF_MINIMUM_RAM}G",
    "jvm-args": None,
    "executablePath": r"C:\\Program Files\\BellSoft\\LibericaJDK-17\\bin\\java" if OS.startswith("Windows") else "java",
    "ramlimiterExceptionBypassed": False,
    "ramlimiterExceptionBypassedSelected": False,
    "wtf_modpack_version": None,
    "wtf_modpack_installed": False,
    "auto_update_launcher": True,
    "launcher_last_update_check": None
}

# Add Windows-specific settings
if OS.startswith("Windows"):
    settings = settings_base
elif OS.startswith("Linux"):
    settings = settings_base.copy()
    settings["setting-info"][0]["fps_boost_selected"] = False
    settings["Fps-Boost"] = False
    settings["executablePath"] = "java"


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
auto_update_launcher = data.get("auto_update_launcher", True)
launcher_last_update_check = data.get("launcher_last_update_check")


def reload_data():
    """Reloads the json data."""
    global mc_home, username, uid, os_name, mc_dir, selected_ver
    global auth_type, jvm_args, allocated_ram, accessToken
    global wtf_modpack_version, wtf_modpack_installed
    global auto_update_launcher, launcher_last_update_check

    with open("settings.json", "r") as js_read:
        s = js_read.read()
        s = s.replace('\t','').replace('\n','').replace(',}','}').replace(',]',']')
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
    auto_update_launcher = data.get("auto_update_launcher", True)
    launcher_last_update_check = data.get("launcher_last_update_check")


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
        requests.head(url, timeout=timeout)
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

        # Initialize launcher updater
        self.launcher_updater = LauncherUpdater() if LauncherUpdater else None

        self.window = style.master
        self.window.geometry("1024x600+110+60")
        self.window.title("WTF Modpack Launcher")
        self.window.configure(bg="#1c1c1c")
        
        # Track Minecraft process
        self.minecraft_process = None
        self.is_minecraft_running = False
        
        # Track launcher update status
        self.is_launcher_updating = False
        self.setup_complete = False

        if os_name.startswith("Windows"):
            try:
                icon_path = resource_path("icon.ico")
                if os.path.exists(icon_path):
                    self.window.iconbitmap(icon_path)
                else:
                    print(f"⚠️ Icona non trovata: {icon_path}")
            except Exception as e:
                print(f"⚠️ Impossibile caricare l'icona: {str(e)}")

        self.setup_ui()
        
        # Check for launcher updates on startup
        if connected and self.launcher_updater and auto_update_launcher:
            self.check_launcher_updates_async()
            # Schedule periodic update checks (every hour)
            self.schedule_periodic_update_check()

    def setup_ui(self):
        """Setup the modern, clean user interface"""
        # Configure modern theme colors
        style.configure("Modern.TButton", borderwidth=0, relief="flat", focuscolor="none")
        style.map("Modern.TButton", 
                  foreground=[('active', '#E5E7EB'), ('!active', '#E5E7EB')],
                  background=[('active', '#1F2937'), ('!active', '#111827')])
        
        self.canvas = Canvas(
            self.window,
            bg="#0B0F14",
            height=600,
            width=1024,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Background
        self.canvas.create_rectangle(0, 0, 1024, 600, fill="#0B0F14", outline="")
        
        # AppBar (Top Navigation)
        self.canvas.create_rectangle(0, 0, 1024, 80, fill="#111827", outline="")
        
        # Logo and title
        self.canvas.create_text(
            30, 25,
            text="WTF Modpack Launcher",
            fill="#E5E7EB",
            font=("Arial", 18, "bold"),
            anchor="w"
        )
        
        # Version tag
        self.canvas.create_text(
            30, 50,
            text="Minecraft 1.20.1 • Forge 47.3.33",
            fill="#9CA3AF",
            font=("Arial", 10),
            anchor="w"
        )

        # Primary CTA Button (Top Right)
        if wtf_modpack_installed:
            cta_text = "Avvia"
            cta_command = self.get_play_button_command()
            cta_color = "#34D399" if not self.is_minecraft_running else "#EF4444"
        else:
            cta_text = "Installa"
            cta_command = self.install_modpack
            cta_color = "#F59E0B"

        self.primary_cta = Button(
            self.window,
            text=cta_text,
            command=cta_command,
            width=12
        )
        self.primary_cta.place(x=750, y=15, width=100, height=50)

        # Action buttons (Top Right)
        self.verify_button = Button(
            self.window,
            text="🔧",
            command=self.verify_and_repair_installation if wtf_modpack_installed else None,
            width=4
        )
        self.verify_button.place(x=860, y=15, width=40, height=25)

        self.settings_button = Button(
            self.window,
            text="⚙️",
            command=self.open_settings,
            width=4
        )
        self.settings_button.place(x=860, y=45, width=40, height=25)

        self.help_button = Button(
            self.window,
            text="❓",
            command=self.show_help,
            width=4
        )
        self.help_button.place(x=910, y=15, width=40, height=25)

        self.update_button = Button(
            self.window,
            text="🔄",
            command=self.check_for_updates if wtf_modpack_installed else None,
            width=4
        )
        self.update_button.place(x=910, y=45, width=40, height=25)

        # Status Strip (Compact chips)
        chip_y = 95
        
        # Pack status chip
        pack_status = "Installato" if wtf_modpack_installed else "Non installato"
        pack_color = "#34D399" if wtf_modpack_installed else "#F59E0B"
        self.canvas.create_rectangle(20, chip_y, 180, chip_y + 30, fill="#111827", outline="#1F2937", width=1)
        self.canvas.create_text(25, chip_y + 8, text="Pack:", fill="#9CA3AF", font=("Arial", 9), anchor="w")
        self.pack_status_text = self.canvas.create_text(25, chip_y + 20, text=pack_status, fill=pack_color, font=("Arial", 9, "bold"), anchor="w")

        # System chip
        total_ram_gb = int(svmem.total / (1024**3))
        available_ram_gb = int(svmem.available / (1024**3))
        allocated_ram_gb = allocated_ram.rstrip('G') if allocated_ram else str(WTF_MINIMUM_RAM)
        self.canvas.create_rectangle(190, chip_y, 380, chip_y + 30, fill="#111827", outline="#1F2937", width=1)
        self.canvas.create_text(195, chip_y + 8, text="Sistema:", fill="#9CA3AF", font=("Arial", 9), anchor="w")
        self.system_status_text = self.canvas.create_text(195, chip_y + 20, text=f"RAM: {allocated_ram_gb}GB/{total_ram_gb}GB", fill="#E5E7EB", font=("Arial", 9), anchor="w")

        # Connection chip
        connection_status = "Online" if connected else "Offline"
        connection_color = "#34D399" if connected else "#EF4444"
        self.canvas.create_rectangle(390, chip_y, 550, chip_y + 30, fill="#111827", outline="#1F2937", width=1)
        self.canvas.create_text(395, chip_y + 8, text="Connessione:", fill="#9CA3AF", font=("Arial", 9), anchor="w")
        self.connection_status_text = self.canvas.create_text(395, chip_y + 20, text=connection_status, fill=connection_color, font=("Arial", 9, "bold"), anchor="w")

        # Disk space chip
        import shutil
        free_space_gb = shutil.disk_usage('.').free / (1024**3)
        self.canvas.create_rectangle(560, chip_y, 720, chip_y + 30, fill="#111827", outline="#1F2937", width=1)
        self.canvas.create_text(565, chip_y + 8, text="Spazio:", fill="#9CA3AF", font=("Arial", 9), anchor="w")
        self.disk_status_text = self.canvas.create_text(565, chip_y + 20, text=f"{free_space_gb:.1f}GB liberi", fill="#E5E7EB", font=("Arial", 9), anchor="w")

        # Main Panel - Stepper
        stepper_y = 140
        self.canvas.create_rectangle(20, stepper_y, 1004, stepper_y + 280, fill="#111827", outline="#1F2937", width=1)
        
        # Step indicators
        step_width = 320
        for i, (step_num, step_title, step_desc) in enumerate([
            ("1", "Seleziona Pack", "Installa o verifica il modpack"),
            ("2", "Configura", "Imposta RAM e Java"),
            ("3", "Avvia", "Lancia Minecraft")
        ]):
            x = 40 + i * step_width
            
            # Step number circle
            if (i == 0 and not wtf_modpack_installed) or (i == 1 and wtf_modpack_installed and not username) or (i == 2 and wtf_modpack_installed and username):
                circle_color = "#F59E0B"  # Current step
                text_color = "#0B0F14"
            elif (i == 0 and wtf_modpack_installed) or (i == 1 and username):
                circle_color = "#34D399"  # Completed
                text_color = "#0B0F14"
            else:
                circle_color = "#1F2937"  # Future step
                text_color = "#9CA3AF"
                
            self.canvas.create_oval(x, stepper_y + 20, x + 30, stepper_y + 50, fill=circle_color, outline="")
            self.canvas.create_text(x + 15, stepper_y + 35, text=step_num, fill=text_color, font=("Arial", 12, "bold"))
            
            # Step title and description
            self.canvas.create_text(x + 40, stepper_y + 28, text=step_title, fill="#E5E7EB", font=("Arial", 12, "bold"), anchor="w")
            self.canvas.create_text(x + 40, stepper_y + 45, text=step_desc, fill="#9CA3AF", font=("Arial", 10), anchor="w")
            
            # Connection line (except for last step)
            if i < 2:
                self.canvas.create_line(x + 30, stepper_y + 35, x + step_width - 10, stepper_y + 35, fill="#1F2937", width=2)

        # Active step content area
        content_y = stepper_y + 80
        self.canvas.create_rectangle(40, content_y, 984, content_y + 120, fill="#0B0F14", outline="#1F2937", width=1)
        
        # Step content based on current state
        if not wtf_modpack_installed:
            # Step 1: Install pack
            self.canvas.create_text(60, content_y + 20, text="Installa il pack per iniziare", fill="#F59E0B", font=("Arial", 14, "bold"), anchor="w")
            self.canvas.create_text(60, content_y + 45, text="Il WTF Modpack include tutte le mod necessarie per giocare", fill="#9CA3AF", font=("Arial", 10), anchor="w")
            
            self.step_install_button = Button(
                self.window,
                text="Installa Pack",
                command=self.install_modpack,
                width=15
            )
            self.step_install_button.place(x=60, y=content_y + 70, width=120, height=35)
            
        elif not username:
            # Step 2: Configure
            self.canvas.create_text(60, content_y + 20, text="Configura il tuo profilo", fill="#F59E0B", font=("Arial", 14, "bold"), anchor="w")
            self.canvas.create_text(60, content_y + 45, text="Imposta username e altre preferenze", fill="#9CA3AF", font=("Arial", 10), anchor="w")
            
            self.step_config_button = Button(
                self.window,
                text="Configura",
                command=self.open_settings,
                width=15
            )
            self.step_config_button.place(x=60, y=content_y + 70, width=120, height=35)
            
        else:
            # Step 3: Ready to play
            self.canvas.create_text(60, content_y + 20, text="Pronto. Seleziona un'opzione.", fill="#34D399", font=("Arial", 14, "bold"), anchor="w")
            self.canvas.create_text(60, content_y + 45, text="Tutto configurato correttamente", fill="#9CA3AF", font=("Arial", 10), anchor="w")
            
            play_text = self.get_play_button_text()
            self.step_play_button = Button(
                self.window,
                text=play_text,
                command=self.get_play_button_command(),
                width=15
            )
            self.step_play_button.place(x=60, y=content_y + 70, width=120, height=35)

        # Progress bar (initially hidden)
        self.progress_bar = Progressbar(
            self.window,
            mode='indeterminate',
            bootstyle="success-striped"
        )

        # Collapsible log area
        log_y = stepper_y + 220
        self.canvas.create_rectangle(40, log_y, 984, log_y + 60, fill="#111827", outline="#1F2937", width=1)
        
        # Log header with collapse toggle
        self.log_collapsed = True
        self.canvas.create_text(60, log_y + 15, text="Log operazioni", fill="#9CA3AF", font=("Arial", 10, "bold"), anchor="w")
        self.toggle_log_button = Button(
            self.window,
            text="📋",
            command=self.toggle_log,
            width=4
        )
        self.toggle_log_button.place(x=920, y=log_y + 5, width=30, height=20)

        self.copy_log_button = Button(
            self.window,
            text="📋",
            command=self.copy_log,
            width=6
        )
        self.copy_log_button.place(x=955, y=log_y + 5, width=25, height=20)

        # Status labels (for log content)
        self.status_label = Label(
            self.window,
            text="Pronto. Seleziona un'opzione.",
            background="#111827",
            foreground="#E5E7EB",
            font=("Arial", 10)
        )
        self.status_label.place(x=60, y=log_y + 35)
        
        self.detail_label = Label(
            self.window,
            text="",
            background="#111827",
            foreground="#9CA3AF",
            font=("Arial", 9),
            wraplength=800
        )
        
        self.progress_label = Label(
            self.window,
            text="",
            background="#111827",
            foreground="#34D399",
            font=("Arial", 9, "bold")
        )

        # Footer
        self.canvas.create_rectangle(0, 560, 1024, 600, fill="#111827", outline="")
        footer_text = "Per il multiplayer usa il launcher ufficiale Minecraft"
        self.canvas.create_text(
            512, 580,
            text=footer_text,
            fill="#9CA3AF",
            font=("Arial", 9),
            anchor="center"
        )

        # Start monitoring and complete setup
        self.start_minecraft_monitor()
        self.window.after(500, self.complete_setup)

    def complete_setup(self):
        """Mark the launcher setup as complete"""
        self.setup_complete = True
        self.update_play_button()
        print("✅ Setup del launcher completato!")
    
    def show_help(self):
        """Show help dialog"""
        showinfo("❓ Aiuto WTF Modpack", 
                "🎮 WTF Modpack Launcher - Guida Rapida\n\n" +
                "📦 Installazione:\n" +
                "• Clicca 'Installa' per scaricare il modpack\n" +
                "• Richiede connessione Internet\n\n" +
                "⚙️ Configurazione:\n" +
                "• Imposta username per modalità offline\n" +
                "• Configura RAM (minimo 4GB)\n\n" +
                "🎯 Avvio:\n" +
                "• Clicca 'Avvia' per lanciare Minecraft\n" +
                "• Prima configurazione più lenta\n\n" +
                "💡 Suggerimenti:\n" +
                "• Usa 'Verifica file' se ci sono problemi\n" +
                "• Per multiplayer Premium usa launcher ufficiale")
    
    def toggle_log(self):
        """Toggle log area visibility"""
        # This will be implemented for showing/hiding detailed logs
        pass
    
    def copy_log(self):
        """Copy log content to clipboard"""
        # This will be implemented to copy current status to clipboard
        try:
            import pyperclip
            log_content = f"WTF Modpack Launcher Log\n" + \
                         f"Status: {self.status_label.cget('text')}\n" + \
                         f"Details: {self.detail_label.cget('text')}\n" + \
                         f"Progress: {self.progress_label.cget('text')}"
            pyperclip.copy(log_content)
            showinfo("📋 Log Copiato", "Il log è stato copiato negli appunti!")
        except ImportError:
            showinfo("📋 Copia Log", "Installa pyperclip per copiare i log automaticamente.")
        except Exception as e:
            showinfo("📋 Errore", f"Impossibile copiare: {str(e)}")
    
    def update_status_chips(self):
        """Update the status chips in the UI"""
        try:
            # Update pack status
            pack_status = "Installato" if wtf_modpack_installed else "Non installato"
            pack_color = "#34D399" if wtf_modpack_installed else "#F59E0B"
            if hasattr(self, 'pack_status_text'):
                self.canvas.itemconfig(self.pack_status_text, text=pack_status, fill=pack_color)
            
            # Update system status
            allocated_ram_gb = allocated_ram.rstrip('G') if allocated_ram else str(WTF_MINIMUM_RAM)
            total_ram_gb = int(svmem.total / (1024**3))
            if hasattr(self, 'system_status_text'):
                self.canvas.itemconfig(self.system_status_text, text=f"RAM: {allocated_ram_gb}GB/{total_ram_gb}GB")
            
            # Update connection status
            connection_status = "Online" if connected else "Offline"
            connection_color = "#34D399" if connected else "#EF4444"
            if hasattr(self, 'connection_status_text'):
                self.canvas.itemconfig(self.connection_status_text, text=connection_status, fill=connection_color)
                
        except Exception as e:
            print(f"Error updating status chips: {e}")
    
    def show_help(self):
        """Show help dialog"""
        showinfo("❓ Aiuto WTF Modpack", 
                "🎮 WTF Modpack Launcher - Guida Rapida\n\n" +
                "📦 Installazione:\n" +
                "• Clicca 'Installa' per scaricare il modpack\n" +
                "• Richiede connessione Internet\n\n" +
                "⚙️ Configurazione:\n" +
                "• Imposta username per modalità offline\n" +
                "• Configura RAM (minimo 4GB)\n\n" +
                "🎯 Avvio:\n" +
                "• Clicca 'Avvia' per lanciare Minecraft\n" +
                "• Prima configurazione più lenta\n\n" +
                "💡 Suggerimenti:\n" +
                "• Usa 'Verifica file' se ci sono problemi\n" +
                "• Per multiplayer Premium usa launcher ufficiale")
    
    def toggle_log(self):
        """Toggle log area visibility"""
        # This will be implemented for showing/hiding detailed logs
        pass
    
    def copy_log(self):
        """Copy log content to clipboard"""
        # This will be implemented to copy current status to clipboard
        try:
            import pyperclip
            log_content = f"WTF Modpack Launcher Log\n" + \
                         f"Status: {self.status_label.cget('text')}\n" + \
                         f"Details: {self.detail_label.cget('text')}\n" + \
                         f"Progress: {self.progress_label.cget('text')}"
            pyperclip.copy(log_content)
            showinfo("📋 Log Copiato", "Il log è stato copiato negli appunti!")
        except ImportError:
            showinfo("📋 Copia Log", "Installa pyperclip per copiare i log automaticamente.")
        except Exception as e:
            showinfo("📋 Errore", f"Impossibile copiare: {str(e)}")

    def get_play_button_text(self):
        """Get the appropriate text for the play button based on current state"""
        if self.is_launcher_updating:
            return "🔄 Aggiornamento Launcher..."
        elif not self.setup_complete:
            return "⏳ Inizializzazione..."
        elif self.is_minecraft_running:
            return "🛑 Chiudi Gioco"
        elif not wtf_modpack_installed:
            return "🚫 Installa Prima il Modpack"
        else:
            return "🎮 Gioca Ora!"
    
    def get_play_button_command(self):
        """Get the appropriate command for the play button based on current state"""
        if self.is_launcher_updating or not self.setup_complete:
            return None  # Disabled state
        elif self.is_minecraft_running:
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
        
        # Update primary CTA button
        if hasattr(self, 'primary_cta'):
            if wtf_modpack_installed:
                if self.is_minecraft_running:
                    self.primary_cta.config(text="Stop", command=self.close_minecraft)
                else:
                    self.primary_cta.config(text="Avvia", command=self.get_play_button_command())
            else:
                self.primary_cta.config(text="Installa", command=self.install_modpack)
        
        # Update step play button if it exists
        if hasattr(self, 'step_play_button'):
            self.step_play_button.config(text=new_text, command=new_command)
        
        # Update status chips
        self.update_status_chips()
    
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
                
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        chunk_count += 1
                        
                        # Update GUI every 500 chunks
                        if chunk_count % 500 == 0 and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            downloaded_mb = downloaded / (1024*1024)
                            total_mb = total_size / (1024*1024)
                            
                            main_status = f"📦 Download in Corso: {progress:.1f}%"
                            detail_status = f"Scaricando WTF Modpack dal repository GitHub..."
                            progress_text = f"📊 {downloaded_mb:.1f}MB / {total_mb:.1f}MB"
                            
                            self.window.after(0, lambda ms=main_status, ds=detail_status, pt=progress_text: 
                                            self.update_gui_status(ms, ds, pt, True))
            
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
                    "📋 Il launcher aprirà le impostazioni per configurare:\n" +
                    "• Il tuo username per Minecraft\n" +
                    "• Modalità di gioco offline\n" +
                    "• Altre impostazioni del launcher\n\n" +
                    "⚠️ Nota: Questo launcher utilizza la modalità offline.\n" +
                    "Per giocare online con account Premium, usa il launcher ufficiale.")
            self.open_settings()
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
            was_first_setup = username is None  # Controlla se è la prima configurazione
            username = new_username
            uid = str(uuid.uuid4())
            
            data["User-info"][0]["username"] = username
            data["User-info"][0]["UUID"] = uid
            data["User-info"][0]["AUTH_TYPE"] = "offline"
            
            with open("settings.json", "w") as f:
                json.dump(data, f, indent=4)
            
            # Se è la prima configurazione e il modpack è installato, offri di giocare subito
            if was_first_setup and wtf_modpack_installed:
                result = tk.messagebox.askquestion("✅ Username Configurato", 
                                                  f"🎉 Username configurato con successo: {username}\n\n" +
                                                  f"🎮 Il WTF Modpack è già installato!\n" +
                                                  f"Vuoi avviare Minecraft subito?")
                settings_window.destroy()
                if result == 'yes':
                    self.launch_minecraft()
            else:
                tk.messagebox.showinfo("✅ Successo", f"Username cambiato in: {username}")
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
        
        # Launcher Update Settings Section
        if self.launcher_updater:
            update_frame = tk.Frame(main_frame, bg="#2d2d2d", relief="solid", bd=1)
            update_frame.pack(fill="x", pady=(0, 15))
            
            tk.Label(update_frame, text="🚀 AGGIORNAMENTI LAUNCHER", 
                    bg="#2d2d2d", fg="#15d38f", font=("Arial", 12, "bold")).pack(pady=(10, 5))
            
            # Current launcher version
            current_version = self.launcher_updater.current_version
            tk.Label(update_frame, text=f"Versione corrente: {current_version}", 
                    bg="#2d2d2d", fg="white", font=("Arial", 10)).pack(pady=5)
            
            # Auto-update info
            tk.Label(update_frame, text="Gli aggiornamenti del launcher sono completamente automatici", 
                    bg="#2d2d2d", fg="#15d38f", font=("Arial", 10)).pack(pady=5)
            
            tk.Label(update_frame, text="Il launcher si aggiornerà automaticamente all'avvio quando disponibile", 
                    bg="#2d2d2d", fg="white", font=("Arial", 9)).pack(pady=5)
            
            tk.Label(update_frame, text="", bg="#2d2d2d").pack(pady=5)  # Spacer
        
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
                
                # Auto-update is always enabled now
                data["auto_update_launcher"] = True
                
                with open("settings.json", "w") as f:
                    json.dump(data, f, indent=4)
                
                settings_summary = f"• RAM allocata: {ram_value}GB\n• Username: {username if username else 'Non configurato'}"
                settings_summary += f"\n• Aggiornamenti automatici: Sempre abilitati"
                
                tk.messagebox.showinfo("✅ Impostazioni Salvate", 
                                     f"Impostazioni salvate con successo!\n\n{settings_summary}\n\n" +
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
                                             "Sei sicuro di voler ripristinare le impostazioni predefiniti?\n\n" +
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



    def run(self):
        """Start the launcher"""
        self.window.mainloop()

    def update_gui_status(self, main_status, detail_status="", progress_text="", show_progress=False):
        """Update the GUI with detailed status information"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=main_status)
        if hasattr(self, 'detail_label'):
            self.detail_label.config(text=detail_status)
        if hasattr(self, 'progress_label'):
            self.progress_label.config(text=progress_text)
        
        if show_progress:
            if hasattr(self, 'progress_bar') and not self.progress_bar.winfo_viewable():
                self.progress_bar.place(x=60, y=480, width=900, height=8)
                self.progress_bar.start()
        else:
            if hasattr(self, 'progress_bar') and self.progress_bar.winfo_viewable():
                self.progress_bar.place_forget()
                self.progress_bar.stop()
        
        # Also update status chips
        self.update_status_chips()
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

    def check_launcher_updates_async(self):
        """Check for launcher updates asynchronously on startup and auto-update if available"""
        if not self.launcher_updater:
            return
        
        def update_callback(update_info):
            if update_info.get('available', False):
                # Auto-update directly without notification
                self.window.after(0, lambda: self.handle_launcher_update_available(update_info))
        
        self.launcher_updater.check_updates_async(update_callback)
    
    def schedule_periodic_update_check(self):
        """Schedule periodic launcher update checks"""
        if not self.launcher_updater:
            return
        
        # Check every hour (3600000 ms)
        def periodic_check():
            if connected and auto_update_launcher:
                self.check_launcher_updates_async()
            # Schedule next check only if auto-update is enabled
            if auto_update_launcher:
                self.window.after(3600000, periodic_check)  # 1 hour
        
        # Start the periodic checking only if auto-update is enabled
        if auto_update_launcher:
            self.window.after(3600000, periodic_check)  # First check in 1 hour
    
    def handle_launcher_update_available(self, update_info):
        """Handle when launcher update is available - automatically start update"""
        try:
            # Set launcher updating flag
            self.is_launcher_updating = True
            self.window.after(0, self.update_play_button)
            
            self.update_gui_status(
                "🚀 Aggiornamento Launcher Automatico...",
                f"Nuova versione {update_info.get('version', 'Sconosciuta')} trovata",
                "Avvio automatico aggiornamento in corso..."
            )
            
            print(f"🚀 Aggiornamento automatico del launcher alla versione {update_info.get('version', 'Sconosciuta')}")
            
            # Start the update process automatically
            self.start_launcher_update(update_info)
            
        except Exception as e:
            print(f"Errore nel gestire aggiornamento disponibile: {e}")
            # Reset flag on error
            self.is_launcher_updating = False
            self.window.after(0, self.update_play_button)
    
    def handle_launcher_update_error(self, error_msg):
        """Handle launcher update errors"""
        try:
            # Reset launcher updating flag
            self.is_launcher_updating = False
            self.window.after(0, self.update_play_button)
            
            self.update_gui_status(
                "❌ Errore Controllo Aggiornamenti",
                "Impossibile verificare aggiornamenti del launcher",
                "Controlla la connessione Internet"
            )
            
            print(f"❌ Errore aggiornamento launcher: {error_msg}")
            
        except Exception as e:
            print(f"Errore nel gestire errore aggiornamento: {e}")
            
        except Exception as e:
            print(f"Errore nel gestire errore aggiornamento: {e}")
    
    def start_launcher_update(self, update_info):
        """Start the launcher update process automatically"""
        try:
            # Ensure launcher updating flag is set
            self.is_launcher_updating = True
            self.window.after(0, self.update_play_button)
            
            # Show progress
            self.update_gui_status(
                "📥 Aggiornamento Launcher in Corso...",
                "Scaricamento e installazione della nuova versione...",
                "Non chiudere il launcher durante l'aggiornamento",
                True
            )
            
            def progress_callback(progress):
                # Update progress in GUI
                self.window.after(0, lambda: self.update_gui_status(
                    "📥 Scaricamento Aggiornamento...",
                    f"Progresso: {progress:.1f}%",
                    "Attendere il completamento del download...",
                    True
                ))
            
            def update_thread():
                try:
                    # Use auto_mode=True to skip confirmation prompts
                    success = self.launcher_updater.update_launcher(progress_callback, auto_mode=True)
                    
                    if success:
                        # Update successful - launcher will restart
                        self.window.after(0, lambda: self.update_gui_status(
                            "✅ Aggiornamento Completato!",
                            "Il launcher verrà riavviato automaticamente",
                            "Chiusura in corso..."
                        ))
                        
                        # Close the launcher after a delay
                        self.window.after(2000, lambda: self.window.quit())
                    else:
                        # Update failed - reset flag
                        self.is_launcher_updating = False
                        self.window.after(0, self.update_play_button)
                        
                        # Update failed
                        self.window.after(0, lambda: self.update_gui_status(
                            "❌ Aggiornamento Fallito",
                            "Impossibile completare l'aggiornamento del launcher",
                            "Riprova riavviando il launcher"
                        ))
                        
                except Exception as e:
                    # Reset flag on error
                    self.is_launcher_updating = False
                    self.window.after(0, self.update_play_button)
                    
                    error_msg = str(e)
                    self.window.after(0, lambda: self.handle_launcher_update_error(error_msg))
            
            Thread(target=update_thread, daemon=True).start()
            
        except Exception as e:
            print(f"Errore nell'avviare aggiornamento: {e}")
            # Reset flag on error
            self.is_launcher_updating = False
            self.window.after(0, self.update_play_button)
            self.handle_launcher_update_error(str(e))

    def debug_update_process(self):
        """Debug dell'intero processo di aggiornamento"""
        print("🔍 DEBUG: Processo di aggiornamento")
        
        if not self.launcher_updater:
            print("❌ LauncherUpdater non disponibile")
            return
        
        print("✅ LauncherUpdater disponibile")
        
        # Test identificazione eseguibile
        detected_exe = self.launcher_updater.debug_executable_detection()
        
        # Test controllo aggiornamenti
        print("\n🔍 Test controllo aggiornamenti...")
        try:
            update_info = self.launcher_updater.check_for_updates()
            print(f"✅ Controllo completato: {update_info}")
        except Exception as e:
            print(f"❌ Errore controllo: {e}")
        
        return detected_exe

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
        
        # Gestione errori per eseguibili compilati
        try:
            # Prova a mostrare un messagebox se possibile
            from tkinter.messagebox import showerror
            showerror("Errore Critico", 
                     f"❌ Si è verificato un errore critico durante l'avvio:\n\n{str(e)}\n\n" +
                     "Per assistenza, contatta il supporto tecnico.")
        except:
            # Se non è possibile mostrare il messagebox, non usare input() negli eseguibili
            if hasattr(sys, '_MEIPASS'):
                # Siamo in un eseguibile compilato, non usare input()
                print("Chiusura automatica dell'applicazione...")
                time.sleep(3)
            else:
                # Siamo in modalità sviluppo, possiamo usare input()
                input("Premi Invio per chiudere...")
