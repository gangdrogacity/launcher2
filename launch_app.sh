#!/bin/bash

# WTF Modpack Launcher - Avvio App macOS
# Script per aprire l'applicazione compilata

echo "🚀 Avvio WTF Modpack Launcher..."

# Vai nella directory dello script
cd "$(dirname "$0")"

# Controlla se l'applicazione esiste
if [ ! -d "dist/WTF Modpack Launcher.app" ]; then
    echo "❌ Applicazione non trovata!"
    echo "⚙️ Compila prima l'applicazione con:"
    echo "   ./compile_macos_simple.sh"
    exit 1
fi

# Rimuovi attributi di quarantena se presenti
echo "🔧 Rimozione attributi di sicurezza..."
xattr -cr "dist/WTF Modpack Launcher.app" 2>/dev/null || true

# Avvia l'applicazione
echo "🎮 Apertura applicazione..."
open "dist/WTF Modpack Launcher.app"

echo "✅ Applicazione avviata!"
echo ""
echo "💡 Se l'app non si apre:"
echo "   1. Vai in Preferenze di Sistema → Sicurezza e Privacy"
echo "   2. Clicca 'Apri comunque' per autorizzare l'app"
echo "   3. Oppure esegui: ./launch_app_direct.sh"
