# WTF Modpack Launcher - Guida Installazione macOS

## Requisiti di Sistema

- **macOS**: 10.14 (Mojave) o superiore
- **Python**: 3.8 o superiore
- **Spazio su disco**: Almeno 2GB liberi
- **RAM**: Minimo 4GB consigliati
- **Java**: Java 8 o superiore (per Minecraft)

## Installazione

### Metodo 1: Eseguibile Precompilato (Consigliato)

1. Scarica l'applicazione `WTF Modpack Launcher.app` dalla sezione releases
2. Trascina l'applicazione nella cartella Applicazioni
3. Al primo avvio, fai clic destro → "Apri" per autorizzare l'app
4. L'applicazione è pronta all'uso!

### Metodo 2: Da Codice Sorgente

1. **Installa Python 3**:
   ```bash
   # Usando Homebrew (consigliato)
   brew install python3
   
   # Oppure scarica da https://www.python.org/downloads/
   ```

2. **Scarica il launcher**:
   ```bash
   git clone [URL_REPOSITORY]
   cd launcher2
   ```

3. **Installa le dipendenze**:
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Avvia il launcher**:
   ```bash
   chmod +x run_launcher_macos.sh
   ./run_launcher_macos.sh
   ```

## Compilazione (Per Sviluppatori)

Per compilare l'applicazione da soli:

```bash
# Rendi eseguibile lo script
chmod +x compile_macos.sh

# Compila l'applicazione
./compile_macos.sh
```

L'applicazione compilata sarà disponibile in `dist/WTF Modpack Launcher.app`.

## Creazione DMG per Distribuzione

Per creare un file DMG per la distribuzione:

1. **Installa create-dmg**:
   ```bash
   brew install create-dmg
   ```

2. **Crea il DMG**:
   ```bash
   create-dmg \
     --volname "WTF Modpack Launcher" \
     --window-pos 200 120 \
     --window-size 600 300 \
     --icon-size 100 \
     --app-drop-link 425 120 \
     "WTF-Modpack-Launcher.dmg" \
     "dist/"
   ```

## Aggiornamenti

Il launcher supporta gli aggiornamenti automatici. In alternativa:

```bash
chmod +x update_launcher_macos.sh
./update_launcher_macos.sh
```

## Risoluzione Problemi

### Errore "App non può essere aperta"
- Vai in Preferenze di Sistema → Sicurezza e Privacy
- Clicca "Apri comunque" nella sezione Generale

### Errore Python non trovato
```bash
# Installa Python tramite Homebrew
brew install python3

# Oppure usando pyenv
brew install pyenv
pyenv install 3.11.0
pyenv global 3.11.0
```

### Errore dipendenze mancanti
```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

### Prestazioni lente
- Assicurati di avere almeno 4GB di RAM liberi
- Chiudi applicazioni non necessarie
- Verifica lo spazio su disco disponibile

## Struttura Directory

```
launcher2/
├── main.py                     # File principale del launcher
├── main_macos.spec            # Configurazione PyInstaller per macOS
├── compile_macos.sh           # Script di compilazione
├── run_launcher_macos.sh      # Script di avvio
├── update_launcher_macos.sh   # Script di aggiornamento
├── restart_launcher_macos.sh  # Script di riavvio
├── requirements.txt           # Dipendenze Python
├── fonts/                     # Font personalizzati
├── authlib/                   # Librerie autenticazione
└── README_MACOS.md           # Questa guida
```

## Supporto

Per problemi o domande:
- Controlla la sezione Issues del repository
- Verifica i log in `~/.minecraft/logs/`
- Assicurati che Java sia installato correttamente

## Licenza

Questo software è distribuito sotto licenza [inserire licenza].
