#!/bin/bash

# Script per convertire l'icona Windows in formato macOS
# Converte icon.ico in icon.icns per l'uso su macOS

echo "🎨 Conversione icona per macOS..."

# Controlla se esiste icon.ico
if [ ! -f "icon.ico" ]; then
    echo "❌ File icon.ico non trovato!"
    exit 1
fi

# Metodo 1: Usando sips (integrato in macOS)
if command -v sips &> /dev/null; then
    echo "📝 Utilizzo sips per la conversione..."
    
    # Crea directory temporanea
    mkdir -p temp_icon.iconset
    
    # Genera diverse dimensioni
    sips -z 16 16     icon.ico --out temp_icon.iconset/icon_16x16.png
    sips -z 32 32     icon.ico --out temp_icon.iconset/icon_16x16@2x.png
    sips -z 32 32     icon.ico --out temp_icon.iconset/icon_32x32.png
    sips -z 64 64     icon.ico --out temp_icon.iconset/icon_32x32@2x.png
    sips -z 128 128   icon.ico --out temp_icon.iconset/icon_128x128.png
    sips -z 256 256   icon.ico --out temp_icon.iconset/icon_128x128@2x.png
    sips -z 256 256   icon.ico --out temp_icon.iconset/icon_256x256.png
    sips -z 512 512   icon.ico --out temp_icon.iconset/icon_256x256@2x.png
    sips -z 512 512   icon.ico --out temp_icon.iconset/icon_512x512.png
    sips -z 1024 1024 icon.ico --out temp_icon.iconset/icon_512x512@2x.png
    
    # Converti in icns
    iconutil -c icns temp_icon.iconset -o icon.icns
    
    # Pulisci file temporanei
    rm -rf temp_icon.iconset
    
    if [ -f "icon.icns" ]; then
        echo "✅ Icona convertita con successo: icon.icns"
    else
        echo "❌ Errore nella conversione!"
        exit 1
    fi
    
# Metodo 2: Usando ImageMagick (se disponibile)
elif command -v convert &> /dev/null; then
    echo "📝 Utilizzo ImageMagick per la conversione..."
    convert icon.ico icon.icns
    
    if [ -f "icon.icns" ]; then
        echo "✅ Icona convertita con successo: icon.icns"
    else
        echo "❌ Errore nella conversione!"
        exit 1
    fi
    
else
    echo "⚠️ Nessun tool di conversione trovato."
    echo "💡 Suggerimenti per l'installazione:"
    echo "   - sips è già incluso in macOS"
    echo "   - ImageMagick: brew install imagemagick"
    echo ""
    echo "🔧 Come alternativa, puoi:"
    echo "   1. Aprire icon.ico in Preview (Anteprima)"
    echo "   2. Esportare come PNG a 512x512 pixel"
    echo "   3. Rinominare il file in icon.icns"
    exit 1
fi
