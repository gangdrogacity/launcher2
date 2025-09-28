#!/bin/bash

# WTF Modpack Launcher - Script di Compilazione per macOS
# Questo script compila il launcher in un'applicazione macOS nativa

echo "🚀 Compilazione WTF Modpack Launcher per macOS..."
echo "⏳ Preparazione ambiente di compilazione..."

# Verifica che Python sia installato
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trovato. Installare Python 3 prima di continuare."
    exit 1
fi

# Verifica che pip sia installato
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 non trovato. Installare pip3 prima di continuare."
    exit 1
fi

# Installa/aggiorna PyInstaller
echo "📦 Installazione/aggiornamento PyInstaller..."
pip3 install --upgrade pyinstaller

# Installa le dipendenze
echo "📦 Installazione dipendenze..."
pip3 install -r requirements.txt

# Rimuovi build precedenti
echo "🧹 Pulizia build precedenti..."
rm -rf build/
rm -rf dist/

# Compila l'applicazione
echo "⚙️ Compilazione in corso..."
python3 -m PyInstaller main_macos.spec

# Verifica se la compilazione è riuscita
if [ -d "dist/WTF Modpack Launcher.app" ]; then
    echo "✅ Compilazione completata con successo!"
    echo "📱 Applicazione creata in: dist/WTF Modpack Launcher.app"
    echo ""
    echo "🎯 Per eseguire l'applicazione:"
    echo "   open 'dist/WTF Modpack Launcher.app'"
    echo ""
    echo "📦 Per creare un DMG per la distribuzione:"
    echo "   create-dmg --volname 'WTF Modpack Launcher' --window-pos 200 120 --window-size 600 300 --icon-size 100 --icon 'WTF Modpack Launcher.app' 175 120 --hide-extension 'WTF Modpack Launcher.app' --app-drop-link 425 120 'WTF-Modpack-Launcher.dmg' 'dist/'"
else
    echo "❌ Compilazione fallita!"
    echo "Controlla i log sopra per individuare il problema."
    exit 1
fi
