#!/bin/bash

# WTF Modpack Launcher - Script di Riavvio per macOS
# Questo script riavvia il launcher dopo un aggiornamento

echo "🔄 Riavvio WTF Modpack Launcher..."
sleep 3

# Directory del launcher
LAUNCHER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$LAUNCHER_DIR"

# Riavvia il launcher
echo "🚀 Avvio launcher aggiornato..."
TK_SILENCE_DEPRECATION=1 python3 main.py
