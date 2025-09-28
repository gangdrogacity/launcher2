#!/bin/bash

# WTF Modpack Launcher - Script di Installazione macOS
# Questo script installa automaticamente tutte le dipendenze necessarie

echo "🚀 WTF Modpack Launcher - Installazione macOS"
echo "==============================================="
echo ""

# Funzione per controllare se un comando esiste
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Controlla se siamo su macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Questo script è progettato per macOS!"
    exit 1
fi

echo "🔍 Controllo requisiti di sistema..."

# Controlla Python 3
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    echo "✅ Python 3 trovato: v$PYTHON_VERSION"
else
    echo "❌ Python 3 non trovato!"
    echo "📝 Installazione Python 3..."
    
    if command_exists brew; then
        brew install python3
    else
        echo "💡 Homebrew non trovato. Installa Python 3 manualmente:"
        echo "   https://www.python.org/downloads/"
        exit 1
    fi
fi

# Controlla pip3
if command_exists pip3; then
    echo "✅ pip3 trovato"
else
    echo "❌ pip3 non trovato!"
    echo "📝 pip3 dovrebbe essere installato con Python 3"
    exit 1
fi

# Installa/aggiorna pip
echo "📦 Aggiornamento pip..."
pip3 install --upgrade pip --quiet

# Installa le dipendenze
echo "📦 Installazione dipendenze Python..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt --quiet
    echo "✅ Dipendenze Python installate"
else
    echo "❌ File requirements.txt non trovato!"
    exit 1
fi

# Controlla Java (per Minecraft)
echo "🔍 Controllo Java..."
if command_exists java; then
    JAVA_VERSION=$(java -version 2>&1 | head -n1 | cut -d'"' -f2)
    echo "✅ Java trovato: v$JAVA_VERSION"
else
    echo "⚠️ Java non trovato!"
    echo "💡 Java è necessario per eseguire Minecraft."
    echo "   Installa Java da: https://www.oracle.com/java/technologies/downloads/"
    echo "   Oppure usa Homebrew: brew install openjdk"
fi

# Controlla Homebrew (opzionale ma utile)
if ! command_exists brew; then
    echo "💡 Consiglio: Installa Homebrew per una gestione più facile dei pacchetti:"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
fi

echo ""
echo "🎯 Installazione completata!"
echo ""
echo "🚀 Per avviare il launcher:"
echo "   ./run_launcher_macos.sh"
echo ""
echo "⚙️ Per compilare l'applicazione nativa:"
echo "   ./compile_macos.sh"
echo ""
echo "📖 Per maggiori informazioni:"
echo "   cat README_MACOS.md"
echo ""
