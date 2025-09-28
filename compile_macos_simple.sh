#!/bin/bash

# WTF Modpack Launcher - Script di Compilazione Semplificato per macOS

echo "🚀 Compilazione WTF Modpack Launcher per macOS (versione semplificata)..."
echo "⏳ Preparazione ambiente di compilazione..."

# Vai nella directory del launcher
cd "$(dirname "$0")"

# Attiva l'ambiente virtuale
echo "🔧 Attivazione ambiente virtuale..."
source launcher_env/bin/activate

# Verifica che PyInstaller sia installato
echo "📦 Verifica PyInstaller..."
pip install --upgrade pyinstaller

# Rimuovi build precedenti
echo "🧹 Pulizia build precedenti..."
rm -rf build/
rm -rf dist/

# Compila l'applicazione con il file spec semplificato
echo "⚙️ Compilazione in corso..."
python -m PyInstaller main_macos_simple.spec --clean --noconfirm

# Verifica se la compilazione è riuscita
if [ -d "dist/WTF Modpack Launcher.app" ]; then
    echo "✅ Compilazione completata con successo!"
    echo "📱 Applicazione creata in: dist/WTF Modpack Launcher.app"
    
    # Rimuovi attributi che possono causare problemi su macOS
    echo "🔧 Rimozione attributi macOS..."
    xattr -cr "dist/WTF Modpack Launcher.app" 2>/dev/null || true
    
    # Firma automatica dell'applicazione per bypassare Gatekeeper
    echo "🔐 Firma dell'applicazione..."
    codesign --force --sign - --deep "dist/WTF Modpack Launcher.app" 2>/dev/null
    
    # Applica fix PyInstaller per macOS (risolve problema doppio click)
    echo "🔧 Applicazione fix PyInstaller per macOS..."
    ./fix_pyinstaller_macos.sh >/dev/null 2>&1
    
    if codesign --verify --deep --strict "dist/WTF Modpack Launcher.app" 2>/dev/null; then
        echo "✅ Applicazione pronta per il doppio click!"
    else
        echo "⚠️ Configurazione completata (warning minori ignorabili)"
    fi
    
    echo ""
    echo "🎯 Per eseguire l'applicazione:"
    echo "   make app"
    echo "   oppure fai doppio click su 'WTF Modpack Launcher.app'"
else
    echo "❌ Compilazione fallita!"
    echo "Controlla i log sopra per individuare il problema."
    exit 1
fi
