#!/bin/bash

# WTF Modpack Launcher - Avvio Diretto
# Script per avviare direttamente l'eseguibile (bypassa Gatekeeper)

echo "🚀 Avvio Diretto WTF Modpack Launcher..."

# Vai nella directory dello script
cd "$(dirname "$0")"

# Controlla se l'applicazione esiste
if [ ! -f "dist/WTF Modpack Launcher.app/Contents/MacOS/WTF Modpack Launcher" ]; then
    echo "❌ Eseguibile non trovato!"
    echo "⚙️ Compila prima l'applicazione con:"
    echo "   ./compile_macos_simple.sh"
    exit 1
fi

echo "🎮 Avvio launcher..."

# Avvia direttamente l'eseguibile
"./dist/WTF Modpack Launcher.app/Contents/MacOS/WTF Modpack Launcher"
