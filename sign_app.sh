#!/bin/bash

# WTF Modpack Launcher - Script di Firma per macOS
# Questo script firma l'applicazione per bypassare Gatekeeper

echo "🔐 Firma dell'applicazione WTF Modpack Launcher..."

# Directory dell'applicazione
APP_PATH="dist/WTF Modpack Launcher.app"

# Verifica che l'app esista
if [ ! -d "$APP_PATH" ]; then
    echo "❌ Applicazione non trovata in: $APP_PATH"
    echo "💡 Esegui prima: make build"
    exit 1
fi

echo "📱 Applicazione trovata: $APP_PATH"

# Rimuovi gli attributi di quarantena prima della firma
echo "🧹 Rimozione attributi di quarantena..."
xattr -cr "$APP_PATH"

# Firma l'applicazione con firma ad-hoc (self-signed)
echo "✍️ Firma dell'applicazione in corso..."

# Firma tutti i framework e librerie
echo "📚 Firma framework e librerie..."
find "$APP_PATH/Contents/Frameworks" -type f -name "*.dylib" -exec codesign --force --sign - {} \; 2>/dev/null || true
find "$APP_PATH/Contents/Frameworks" -type d -name "*.framework" -exec codesign --force --sign - {} \; 2>/dev/null || true

# Firma l'eseguibile principale
echo "⚙️ Firma eseguibile principale..."
codesign --force --sign - "$APP_PATH/Contents/MacOS/"* 2>/dev/null || true

# Firma l'intera applicazione
echo "🎯 Firma finale dell'applicazione..."
codesign --force --sign - --deep "$APP_PATH"

# Verifica la firma
echo "🔍 Verifica della firma..."
if codesign --verify --deep --strict "$APP_PATH" 2>/dev/null; then
    echo "✅ Applicazione firmata con successo!"
    echo ""
    echo "🎉 L'applicazione ora dovrebbe aprirsi con il doppio click!"
    echo "📱 Percorso: $APP_PATH"
    echo ""
    echo "🚀 Per testare:"
    echo "   open '$APP_PATH'"
    echo "   oppure fai doppio click nell'applicazione dal Finder"
else
    echo "❌ Errore nella verifica della firma"
    echo "⚠️ L'applicazione potrebbe comunque funzionare"
fi

echo ""
echo "ℹ️ Nota: Questa è una firma ad-hoc (self-signed)"
echo "💡 Per la distribuzione pubblica, usa un certificato Apple Developer"
