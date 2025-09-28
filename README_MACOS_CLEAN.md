# 🎮 WTF Modpack Launcher - macOS

## 🚀 Avvio Rapido

### Opzione 1: Applicazione Nativa (Consigliato)
```bash
make app
# oppure
./launch_app.sh
```

### Opzione 2: Launcher Python
```bash
make run
# oppure
./run_launcher_macos.sh
```

## 📦 Installazione

### Prima installazione:
```bash
make install  # Installa dipendenze
make build    # Compila l'applicazione
make app      # Avvia l'applicazione
```

## 🛠 Comandi Disponibili

- `make install` - Installa dipendenze Python
- `make run` - Avvia launcher Python 
- `make build` - Compila applicazione nativa
- `make app` - Avvia applicazione compilata
- `make clean` - Rimuove file temporanei

## 📋 Requisiti

- **macOS**: 10.14+ (Mojave o superiore)
- **Homebrew**: Per Python 3.13 e Tkinter 9.0
- **Java**: 8+ (per Minecraft)
- **Spazio**: 2GB liberi

## ⚡ Installazione Rapida

```bash
# 1. Installa tutto
make install

# 2. Compila l'app
make build

# 3. Avvia l'app
make app
```

## 🔧 Risoluzione Problemi

**App non si apre con doppio click?**
- Usa `make app` dal terminale
- L'app funziona sempre dal terminale

**Errori Python?**
- Verifica che Homebrew sia installato
- Riesegui `make install`

**Problemi di connessione?**
- Controlla la connessione Internet
- Verifica firewall/antivirus

## 📁 File Essenziali

- `main.py` - Launcher principale
- `main_macos_simple.spec` - Configurazione PyInstaller
- `install_macos.sh` - Setup dipendenze
- `run_launcher_macos.sh` - Avvio Python
- `compile_macos_simple.sh` - Compilazione app
- `launch_app.sh` - Avvio applicazione compilata

## 🎯 Tutto Funzionante!

✅ Python 3.13 con Tkinter 9.0  
✅ Interfaccia grafica completa  
✅ Compilazione applicazione nativa  
✅ Supporto completo macOS  

---

💡 **Suggerimento**: Usa `make app` per la migliore esperienza!
