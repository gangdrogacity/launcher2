#!/bin/bash

# WTF Modpack Launcher - Avvio Rapido per macOS
# Script di avvio semplificato che risolve i problemi di Python

echo "🚀 WTF Modpack Launcher - Avvio Rapido"

# Vai nella directory del launcher
cd "$(dirname "$0")"

# Avvia con la configurazione corretta
echo "🎮 Avvio in corso..."
TK_SILENCE_DEPRECATION=1 python3 main.py

echo "👋 Launcher chiuso."
