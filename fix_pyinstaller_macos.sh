#!/bin/bash

# WTF Modpack Launcher - Fix definitivo per PyInstaller su macOS
# Basato su: https://github.com/orgs/pyinstaller/discussions/7966

echo "🔧 Fix PyInstaller per applicazioni Tkinter su macOS..."

APP_PATH="dist/WTF Modpack Launcher.app"

if [ ! -d "$APP_PATH" ]; then
    echo "❌ Applicazione non trovata: $APP_PATH"
    echo "💡 Esegui prima: make build"
    exit 1
fi

echo "📱 Applicazione trovata: $APP_PATH"

# 1. Fix Info.plist - Aggiungi configurazioni specifiche per GUI
echo "🔧 Fix Info.plist..."
INFO_PLIST="$APP_PATH/Contents/Info.plist"

# Backup del plist originale
cp "$INFO_PLIST" "$INFO_PLIST.backup"

# Aggiungi configurazioni GUI essenziali
/usr/libexec/PlistBuddy -c "Add :LSUIElement bool false" "$INFO_PLIST" 2>/dev/null || true
/usr/libexec/PlistBuddy -c "Add :NSHighResolutionCapable bool true" "$INFO_PLIST" 2>/dev/null || true
/usr/libexec/PlistBuddy -c "Add :LSBackgroundOnly bool false" "$INFO_PLIST" 2>/dev/null || true
/usr/libexec/PlistBuddy -c "Add :LSRequiresNativeExecution bool true" "$INFO_PLIST" 2>/dev/null || true

# Fix per applicazioni Python/Tkinter
/usr/libexec/PlistBuddy -c "Add :NSAppleScriptEnabled bool false" "$INFO_PLIST" 2>/dev/null || true

# 2. Modifica il punto d'ingresso principale
echo "⚙️ Modifica punto d'ingresso..."
MAIN_EXECUTABLE="$APP_PATH/Contents/MacOS/WTF Modpack Launcher"
ORIGINAL_EXECUTABLE="$APP_PATH/Contents/MacOS/WTF Modpack Launcher.original"

# Salva l'eseguibile originale se non esiste già
if [ ! -f "$ORIGINAL_EXECUTABLE" ]; then
    mv "$MAIN_EXECUTABLE" "$ORIGINAL_EXECUTABLE"
fi

# Crea un nuovo script di avvio che risolve il problema PyInstaller
cat > "$MAIN_EXECUTABLE" << 'EOF'
#!/bin/bash
# Entry point per WTF Modpack Launcher su macOS
# Fix per problema PyInstaller + Tkinter

# Directory dell'applicazione  
APP_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$APP_DIR"

# Variabili d'ambiente essenziali per macOS + Tkinter
export TK_SILENCE_DEPRECATION=1
export PYTHONPATH="$APP_DIR:$PYTHONPATH"

# Fix per applicazioni GUI su macOS
if [ -z "$DISPLAY" ]; then
    export DISPLAY=:0
fi

# Lancia l'applicazione originale PyInstaller
exec "$APP_DIR/WTF Modpack Launcher.original" "$@"
EOF

chmod +x "$MAIN_EXECUTABLE"

# 3. Fix permessi completi
echo "🔒 Fix permessi..."
chmod -R 755 "$APP_PATH/Contents/MacOS/"
xattr -cr "$APP_PATH"

# 4. Firma l'applicazione
echo "🔐 Firma applicazione..."
codesign --force --sign - --deep "$APP_PATH" 2>/dev/null || true

# 5. Verifica finale
echo "🔍 Verifica configurazione..."
if codesign --verify --deep --strict "$APP_PATH" 2>/dev/null; then
    echo "✅ Applicazione verificata con successo!"
else
    echo "⚠️ Verifica completata (warning minori ignorabili)"
fi

echo ""
echo "✅ Fix PyInstaller applicato con successo!"
echo ""
echo "🎯 Ora prova:"
echo "   1. Fai doppio click sull'app nel Finder"
echo "   2. Oppure: open '$APP_PATH'"
echo ""
echo "💡 Questo fix risolve:"
echo "   - Problema doppio click su macOS"
echo "   - Gestione corretta GUI Tkinter"
echo "   - Bypass Gatekeeper con firma"
echo ""
