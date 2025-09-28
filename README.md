# WTF Modpack Launcher 🚀

Un launcher moderno per modpack Minecraft con supporto cross-platform.

## � Compatibilità

- ✅ **Windows** (7/10/11)
- ✅ **macOS** (10.14+)
- ✅ **Linux** (Ubuntu/Debian)

## 🎯 Caratteristiche

- 🖥️ Interfaccia grafica moderna con ttkbootstrap
- ⚡ Download automatico modpack
- 🎮 Integrazione Minecraft Launcher
- 📦 Build automatico per tutte le piattaforme
- � Supporto firma app macOS

## 🛠️ Quick Start

### Metodo 1: Script Python (Raccomandato)

```bash
# Compila per la tua piattaforma
python build.py
```

### Metodo 2: Makefile

```bash
# Compila
make build

# Test in modalità sviluppo
make test

# Esegui app compilata
make run

# Pulizia
make clean
```

## 📋 Requisiti

- **Python 3.8+** (raccomandato 3.13+)
- **pip** per le dipendenze
- **PyInstaller** (installato automaticamente)

### Dipendenze automatiche

Il build script installerà automaticamente:
- `minecraft-launcher-lib`
- `ttkbootstrap`
- `requests`
- `psutil`
- `PyInstaller`

## 🏗️ Build Dettagliato

### Windows
```bash
python build.py
# Output: dist/WTF Modpack Launcher.exe
```

### macOS
```bash
python build.py
# Output: dist/WTF Modpack Launcher.app
# Include fix Gatekeeper automatici
```

### Linux
```bash
python build.py
# Output: dist/WTF Modpack Launcher
```
1. Clona il repository:
   ```bash
   git clone https://github.com/your-repo/wtf-modpack-launcher.git
   cd wtf-modpack-launcher
   ```

2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

3. Avvia il launcher:
   ```bash
   python main.py
   ```

## 🏗️ Compilazione

Per creare un eseguibile:

1. Installa PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Compila il launcher:
   ```bash
   compile.bat
   ```

L'eseguibile sarà disponibile in `dist/WTF_Modpack_Launcher.exe`

## 🎮 Utilizzo

1. **Prima configurazione**: Inserisci il tuo username per la modalità offline
2. **Installazione**: Clicca "Installa WTF Modpack" per scaricare automaticamente tutto
3. **Gioco**: Clicca "Gioca Ora!" per avviare Minecraft con il modpack
4. **Aggiornamenti**: Il launcher controllerà automaticamente gli aggiornamenti

## ⚙️ Configurazione

### Memoria RAM
- **Minimo**: 4GB (richiesto per il modpack)
- **Consigliato**: 6-8GB per prestazioni ottimali
- Configurabile nelle impostazioni del launcher

### Directory
- **Minecraft**: `.minecraft` (creata automaticamente)
- **Mod**: `.minecraft/mods` (gestite automaticamente)
- **Configurazioni**: `settings.json`

## 🔧 Risoluzione Problemi

### Errori Comuni

**"Java non trovato"**
- Installa Java 17+ da [Adoptium](https://adoptium.net/)
- Su Windows, il launcher cerca Java in: `C:\Program Files\BellSoft\LibericaJDK-17\bin\java`

**"Errore download modpack"**
- Verifica la connessione Internet
- Controlla che GitHub sia accessibile
- Riprova l'installazione

**"Minecraft non si avvia"**
- Verifica che ci sia abbastanza RAM disponibile
- Controlla che Forge sia installato correttamente
- Usa il pulsante "Ripara" nel launcher

### Log e Debug
- I log di Minecraft sono in `.minecraft/logs/`
- Apri la cartella con il pulsante "Apri Logs" nelle impostazioni

## 📁 Struttura File

```
wtf-modpack-launcher/
├── main.py              # Codice principale del launcher
├── main.spec            # Configurazione PyInstaller
├── requirements.txt     # Dipendenze Python
├── settings.json        # Configurazioni utente (generato automaticamente)
├── compile.bat          # Script di compilazione
├── icon.ico            # Icona del launcher
├── fonts/              # Font personalizzati
│   ├── GALS.ttf
│   ├── GALSB.ttf
│   ├── Minecraft.ttf
│   └── Sunshiney-Regular.ttf
└── .minecraft/         # Directory Minecraft (creata automaticamente)
    ├── versions/       # Versioni Minecraft e Forge
    ├── mods/          # Mod del WTF Modpack
    └── logs/          # Log di gioco
```

## 🤝 Contribuire

1. Fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Questo progetto è sotto licenza MIT. Vedi il file `LICENSE` per i dettagli.

## 🎯 WTF Modpack

Il WTF Modpack è una collezione curata di mod per Minecraft 1.20.1 che include:
- Mod di ottimizzazione prestazioni
- Nuovi biomi e strutture
- Meccaniche di gioco migliorate
- Interfaccia utente migliorata

Per maggiori informazioni sul modpack, visita il [repository ufficiale](https://github.com/jamnaga/wtf-modpack).

## 📞 Supporto

- **Issues**: Usa la sezione Issues di GitHub per bug e richieste
- **Documentazione**: Questo README e i commenti nel codice
- **Community**: Unisciti al server Discord del WTF Modpack

---

**Nota**: Questo launcher è progettato specificamente per il WTF Modpack e la modalità offline. Per giocare online con account Premium, usa il launcher ufficiale di Minecraft.

## 📋 Caratteristiche

- ✅ **Installazione Automatica**: Scarica e installa automaticamente Minecraft Forge 1.20.1-47.3.33
- 📦 **Gestione Modpack**: Download automatico delle mod dal repository GitHub
- 🔄 **Aggiornamenti**: Controllo automatico degli aggiornamenti del modpack
- 💾 **Gestione RAM**: Configurazione della memoria allocata (minimo 4GB)
- 🎮 **Modalità Offline**: Gioca senza account Minecraft Premium
- 🔧 **Riparazione**: Sistema di verifica e riparazione automatica
- 🎨 **Interfaccia Moderna**: GUI user-friendly con tema scuro

---

## 🚀 Come Iniziare

### 1. **Primi Passi**
   - Avvia `WTF_Modpack_Launcher.exe`
   - Il launcher verificherà automaticamente la connessione Internet
   - Alla prima apertura vedrai l'interfaccia principale

### 2. **Installazione Modpack**
   - Clicca su "📦 Installa WTF Modpack"
   - Conferma l'installazione nella finestra di dialogo
   - Attendi il completamento (3-10 minuti a seconda della connessione)

### 3. **Configurazione Account**
   - Al primo avvio di Minecraft, inserisci un username
   - L'username può essere qualsiasi nome (modalità offline)
   - Evita spazi e caratteri speciali

### 4. **Gioca!**
   - Clicca "🎮 Gioca Ora!" per avviare Minecraft
   - Il primo avvio può richiedere alcuni minuti
   - Il launcher monitorerà lo stato del gioco

---

## ⚙️ Impostazioni

Accedi alle impostazioni tramite il pulsante "⚙️ Impostazioni":

### 👤 **Account**
- Modifica username
- Visualizza informazioni account

### 💾 **Memoria RAM**
- Configura RAM allocata (minimo 4GB)
- Visualizza RAM sistema disponibile
- Raccomandazioni automatiche

### 💻 **Sistema**
- Informazioni sistema operativo
- Directory Minecraft
- Stato connessione
- Versioni installate

### 🔧 **Strumenti**
- Apri cartella Minecraft
- Visualizza log di gioco
- Reset impostazioni

---

## 🔧 Risoluzione Problemi

### **Minecraft non si avvia**
1. Verifica di avere Java installato
2. Controlla la RAM allocata (minimo 4GB)
3. Usa il pulsante "🔧 Ripara" per verificare l'installazione
4. Controlla i log in `.minecraft/logs/latest.log`

### **Errori di download**
1. Verifica la connessione Internet
2. Controlla che GitHub sia accessibile
3. Riprova dopo qualche minuto
4. Usa una connessione stabile per i download

### **Prestazioni scarse**
1. Aumenta la RAM allocata nelle impostazioni
2. Chiudi altri programmi durante il gioco
3. Verifica che il PC soddisfi i requisiti minimi

### **Problemi di avvio del launcher**
1. Esegui come amministratore
2. Controlla l'antivirus (potrebbe bloccare il launcher)
3. Verifica di avere i permessi di scrittura nella cartella

---

## 📊 Requisiti di Sistema

### **Minimi**
- **OS**: Windows 10/11 (64-bit)
- **RAM**: 8GB (4GB per Minecraft + 4GB per il sistema)
- **Storage**: 5GB liberi per il modpack
- **Internet**: Connessione stabile per download e aggiornamenti

### **Raccomandati**
- **OS**: Windows 11 (64-bit)
- **RAM**: 16GB (8GB per Minecraft + 8GB per il sistema)
- **Storage**: 10GB liberi per mod aggiuntive
- **Internet**: Connessione veloce per download rapidi

---

## 📁 Struttura File

```
WTF_Modpack_Launcher_Release/
├── WTF_Modpack_Launcher.exe    # Launcher principale
├── README_LAUNCHER.md          # Questo file
├── wtf_modpack_config.json     # Configurazione modpack
├── img/                        # Risorse grafiche
├── fonts/                      # Font personalizzati
└── config/                     # Configurazioni
```

Dopo il primo avvio verrà creata anche:
```
.minecraft/                     # Directory Minecraft
├── versions/                   # Versioni Minecraft e Forge
├── mods/                       # Mod del modpack
├── saves/                      # Mondi salvati
├── logs/                       # Log di gioco
└── settings.json               # Impostazioni launcher
```

---

## 🔄 Aggiornamenti

Il launcher controlla automaticamente gli aggiornamenti:
- **All'avvio**: Verifica aggiornamenti del modpack
- **Manuale**: Pulsante "🔄 Verifica Aggiornamenti"
- **Automatico**: Notifica quando è disponibile una nuova versione

---

## 🎮 Modalità di Gioco

### **Offline (Predefinita)**
- Non richiede account Minecraft Premium
- Username personalizzabile
- Ideale per gioco singolo e LAN

### **Online (Account Premium)**
- Per server online con autenticazione
- Usa il launcher ufficiale Minecraft
- Copia le mod dalla cartella `.minecraft/mods`

---

## 🆘 Supporto

### **Problemi Comuni**
1. **"Java non trovato"**: Installa Java 17 o superiore
2. **"RAM insufficiente"**: Aumenta RAM allocata nelle impostazioni
3. **"Modpack non trovato"**: Verifica connessione Internet
4. **"Launcher non si apre"**: Esegui come amministratore

### **Log e Debug**
- Log launcher: Console durante l'esecuzione
- Log Minecraft: `.minecraft/logs/latest.log`
- Impostazioni: `settings.json` nella directory launcher

### **Reset Completo**
Se tutto va storto:
1. Chiudi Minecraft e launcher
2. Elimina la cartella `.minecraft`
3. Elimina `settings.json`
4. Riavvia il launcher e reinstalla

---

## 📄 Informazioni Tecniche

- **Versione Minecraft**: 1.20.1
- **Versione Forge**: 47.3.33
- **RAM Minima**: 4GB
- **Linguaggio**: Python 3.x compilato
- **GUI**: tkinter + ttkbootstrap
- **Repository**: [jamnaga/wtf-modpack](https://github.com/jamnaga/wtf-modpack)

---

## 🎯 Note Finali

Questo launcher è stato creato specificatamente per il WTF Modpack e ottimizzato per fornire la migliore esperienza di gioco possibile. 

**Buon divertimento con il WTF Modpack! 🎮**

---

*Launcher sviluppato nel 2025 • Versione 1.0*
