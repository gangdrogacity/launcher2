# 🎮 WTF Modpack Launcher

**Launcher personalizzato per il WTF Modpack - Minecraft 1.20.1**

---

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
