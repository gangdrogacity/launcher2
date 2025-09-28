# WTF Modpack Launcher - Makefile per macOS
# Comandi semplificati con fix PyInstaller integrato

.PHONY: help install run build fix app clean

# Mostra aiuto
help:
	@echo "WTF Modpack Launcher - Comandi Disponibili:"
	@echo "==========================================="
	@echo ""
	@echo "  make install    - Installa dipendenze"
	@echo "  make run        - Avvia il launcher (Python)"
	@echo "  make build      - Compila l'applicazione (con fix auto)"
	@echo "  make fix        - Applica fix PyInstaller a app esistente"
	@echo "  make app        - Avvia l'applicazione compilata"
	@echo "  make clean      - Pulisce i file temporanei"
	@echo ""

# Installazione completa
install:
	@echo "📦 Installazione dipendenze..."
	./install_macos.sh

# Avvio del launcher Python
run:
	@echo "🚀 Avvio launcher..."
	./run_launcher_macos.sh

# Compilazione dell'applicazione (include fix automatico)
build:
	@echo "⚙️ Compilazione applicazione..."
	./compile_macos_simple.sh

# Fix PyInstaller per applicazione esistente
fix:
	@echo "🔧 Fix PyInstaller..."
	./fix_pyinstaller_macos.sh

# Avvio applicazione compilata
app:
	@echo "🚀 Avvio applicazione..."
	./launch_app.sh

# Pulizia file temporanei
clean:
	@echo "🧹 Pulizia file temporanei..."
	rm -rf build/
	rm -rf dist/
	rm -rf __pycache__/
	rm -rf launcher_env/
	rm -rf *.pyc
	rm -f settings.json
	@echo "✅ Pulizia completata"
