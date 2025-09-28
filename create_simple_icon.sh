#!/bin/bash

# Script semplificato per creare un'icona per macOS

echo "🎨 Creazione icona semplificata per macOS..."

# Controlla se esiste icon.ico
if [ ! -f "icon.ico" ]; then
    echo "❌ File icon.ico non trovato!"
    exit 1
fi

# Prova prima con sips in modo più semplice
echo "📝 Tentativo conversione diretta..."

# Converti direttamente in PNG ad alta risoluzione
sips -s format png icon.ico --out icon_temp.png 2>/dev/null

if [ -f "icon_temp.png" ]; then
    # Ridimensiona a 512x512 (dimensione standard per icone macOS)
    sips -Z 512 icon_temp.png --out icon_512.png 2>/dev/null
    
    if [ -f "icon_512.png" ]; then
        # Rinomina come icns (molti bundler accettano PNG con estensione icns)
        cp icon_512.png icon.icns
        rm icon_temp.png icon_512.png
        
        echo "✅ Icona creata: icon.icns"
        echo "📏 Dimensione: 512x512 pixel"
    else
        echo "❌ Errore nel ridimensionamento"
        rm -f icon_temp.png
        exit 1
    fi
else
    echo "❌ Impossibile convertire icon.ico"
    echo "💡 Prova ad aprire icon.ico in Preview e salvarlo come PNG a 512x512"
    exit 1
fi
