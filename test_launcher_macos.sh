#!/bin/bash

# Test rapido del launcher per macOS
echo "🧪 Test WTF Modpack Launcher per macOS"
echo "======================================"

# Verifica che tutti i file necessari esistano
files_to_check=("main.py" "requirements.txt" "main_macos.spec")

for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file trovato"
    else
        echo "❌ $file mancante!"
        exit 1
    fi
done

# Verifica dipendenze Python
echo ""
echo "🔍 Verifica dipendenze Python..."

dependencies=("tkinter" "minecraft_launcher_lib" "ttkbootstrap" "requests" "psutil")

for dep in "${dependencies[@]}"; do
    if python3 -c "import $dep" 2>/dev/null; then
        echo "✅ $dep disponibile"
    else
        echo "❌ $dep mancante!"
        echo "📦 Installa con: pip3 install $dep"
    fi
done

echo ""
echo "🚀 Test avvio launcher (5 secondi)..."

# Avvia il launcher in background e killalo dopo 5 secondi
timeout 5s env TK_SILENCE_DEPRECATION=1 python3 main.py 2>/dev/null || true

echo "✅ Test completato!"
echo ""
echo "💡 Se il launcher si è aperto correttamente, tutto funziona!"
echo "⚙️ Per compilare l'app nativa: ./compile_macos.sh"
