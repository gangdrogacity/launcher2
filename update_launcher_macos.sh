#!/bin/bash

# WTF Modpack Launcher - Script di Aggiornamento per macOS
# Questo script gestisce l'aggiornamento del launcher

echo "🔄 WTF Modpack Launcher - Script di Aggiornamento macOS"
echo "⏳ Preparazione aggiornamento..."

# Directory del launcher
LAUNCHER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$LAUNCHER_DIR"

# Scarica e applica l'aggiornamento
if [ -f "updater.py" ]; then
    echo "📦 Esecuzione aggiornamento..."
    python3 updater.py
    
    if [ $? -eq 0 ]; then
        echo "✅ Aggiornamento completato!"
        echo "🚀 Riavvio launcher..."
        sleep 2
        TK_SILENCE_DEPRECATION=1 python3 main.py
    else
        echo "❌ Errore durante l'aggiornamento!"
        echo "🔧 Prova a riavviare manualmente il launcher"
    fi
else
    echo "❌ File updater.py non trovato!"
    echo "🔧 Impossibile eseguire l'aggiornamento automatico"
fi

echo "Premi qualsiasi tasto per chiudere..."
read -n 1
