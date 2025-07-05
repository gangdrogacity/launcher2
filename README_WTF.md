# WTF Modpack Launcher

Un launcher personalizzato per il modpack WTF basato sul repository [jamnaga/wtf-modpack](https://github.com/jamnaga/wtf-modpack).

## Caratteristiche

- **Installazione automatica**: Scarica automaticamente l'ultima versione del modpack dal repository GitHub
- **Gestione Forge**: Installa automaticamente Forge 47.3.33 per Minecraft 1.20.1
- **Gestione RAM**: Configurazione automatica con minimo 4GB di RAM
- **Aggiornamenti automatici**: Controlla e installa automaticamente gli aggiornamenti del modpack
- **Interfaccia intuitiva**: GUI moderna e facile da usare

## Requisiti di Sistema

- **Java 17+**: Richiesto per Minecraft 1.20.1 e Forge
- **RAM**: Minimo 4GB disponibili per Minecraft
- **Spazio disco**: Almeno 2GB liberi per il modpack
- **Connessione internet**: Necessaria per download e aggiornamenti

## Installazione

1. **Installa Python 3.8+** (se non già installato)

2. **Installa le dipendenze**:
   ```bash
   pip install -r requirements_wtf.txt
   ```

3. **Avvia il launcher**:
   ```bash
   python wtf_launcher.py
   ```

## Utilizzo

### Prima configurazione

1. **Avvia il launcher** - Il launcher controllerà automaticamente la connessione internet
2. **Installa il modpack** - Clicca su "Install WTF Modpack" per scaricare l'ultima versione
3. **Configura l'account** - Inserisci il tuo username Minecraft (modalità offline supportata)
4. **Avvia il gioco** - Clicca su "Play" per lanciare Minecraft con il modpack

### Aggiornamenti

Il launcher controlla automaticamente gli aggiornamenti all'avvio. Puoi anche controllare manualmente cliccando su "Check for Updates".

### Impostazioni

- **RAM Allocation**: Configura la quantità di RAM da allocare (minimo 4GB)
- **Account Settings**: Gestisci le informazioni dell'account Minecraft

## Struttura del Modpack

Il modpack WTF include:

- **Minecraft 1.20.1**
- **Forge 47.3.33**
- **Oltre 100 mod** tra cui:
  - Create
  - Immersive Engineering
  - JEI (Just Enough Items)
  - Xaero's Minimap
  - E molte altre...

## Risoluzione Problemi

### Errore di avvio
- Verifica di avere Java 17+ installato
- Controlla di avere almeno 4GB di RAM liberi
- Assicurati che la cartella `.minecraft` abbia i permessi di scrittura

### Problemi di download
- Controlla la connessione internet
- Verifica che GitHub sia accessibile
- Riprova dopo qualche minuto (potrebbe essere un problema temporaneo)

### Performance basse
- Aumenta l'allocazione di RAM nelle impostazioni
- Chiudi altre applicazioni per liberare risorse
- Considera di ridurre le impostazioni grafiche in-game

## File di Configurazione

Il launcher crea un file `settings.json` che contiene:
- Informazioni dell'account
- Configurazione RAM
- Versione del modpack installata
- Percorsi di Minecraft

## Aggiornamenti del Modpack

Il launcher scarica automaticamente:
1. **client.zip** - Contiene tutte le mod del modpack
2. **Forge installer** - Versione specifica richiesta
3. **Configurazioni** - File di configurazione delle mod

## Sicurezza

- Il launcher usa solo fonti ufficiali (GitHub releases)
- Non vengono memorizzate password (solo modalità offline)
- Tutti i download sono verificati

## Supporto

Per problemi o suggerimenti:
1. Controlla la sezione "Risoluzione Problemi" sopra
2. Verifica le [Issues del modpack](https://github.com/jamnaga/wtf-modpack/issues)
3. Assicurati di avere l'ultima versione del launcher

## Licenza

Questo launcher è basato sul progetto PyCraft originale e modificato per il modpack WTF.

---

**Nota**: Questo launcher è specificamente progettato per il modpack WTF. Per altri modpack o versioni vanilla di Minecraft, usa il launcher originale PyCraft.
