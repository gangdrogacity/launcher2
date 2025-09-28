#!/bin/bash

# WTF Modpack Launcher - Script di Avvio per macOS
# Questo script avvia il launcher Python direttamente

echo "🚀 Avvio WTF Modpack Launcher..."

# Verifica che Python sia installato
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trovato."
    echo "📝 Installa Python 3 da https://www.python.org/downloads/"
    exit 1
fi

# Verifica che pip sia installato
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 non trovato."
    echo "📝 Installa pip3 insieme a Python 3"
    exit 1
fi

# Installa le dipendenze se necessario
echo "📦 Verifica dipendenze..."
pip3 install -q -r requirements.txt

# Avvia il launcher
echo "🎮 Avvio launcher..."
source launcher_env/bin/activate
TK_SILENCE_DEPRECATION=1 python main.py
