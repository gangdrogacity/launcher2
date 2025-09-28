# WTF Modpack Launcher - Makefile Universale
# Funziona su Windows, macOS e Linux

# Rileva sistema operativo
UNAME_S := $(shell uname -s 2>/dev/null || echo Windows)

# Comando Python
PYTHON := $(shell which python3 2>/dev/null || which python 2>/dev/null || echo python)

.PHONY: all setup build clean test run help

# Target predefinito
all: build

# Help
help:
	@echo "🚀 WTF Modpack Launcher - Build Universale"
	@echo "============================================"
	@echo ""
	@echo "Comandi disponibili:"
	@echo "  setup  - Configura ambiente di sviluppo"
	@echo "  build  - Compila l'applicazione"
	@echo "  clean  - Pulisce i file temporanei"
	@echo "  test   - Esegue l'applicazione in modalità test"
	@echo "  run    - Esegue l'applicazione compilata"
	@echo "  help   - Mostra questo aiuto"

# Setup ambiente (usa lo script Python)
setup:
	@$(PYTHON) build.py setup

# Build completo (usa lo script Python)
build:
	@$(PYTHON) build.py

# Pulizia
clean:
	@echo "🧹 Pulizia in corso..."
	@rm -rf build dist *.spec.bak
	@rm -rf __pycache__ *.pyc
	@echo "✅ Pulizia completata!"

# Test applicazione
test:
	@echo "🧪 Test applicazione..."
ifeq ($(UNAME_S),Windows)
	@launcher_env\Scripts\python main.py
else
	@launcher_env/bin/python main.py
endif

# Esegui applicazione compilata
run:
	@echo "🎯 Esecuzione applicazione..."
ifeq ($(UNAME_S),Darwin)
	@if [ -d "dist/WTF Modpack Launcher.app" ]; then \
		open "dist/WTF Modpack Launcher.app"; \
	else \
		echo "❌ Applicazione non trovata. Esegui 'make build' prima."; \
	fi
else ifeq ($(UNAME_S),Windows)
	@if [ -f "dist/WTF Modpack Launcher.exe" ]; then \
		"dist/WTF Modpack Launcher.exe"; \
	else \
		echo "❌ Eseguibile non trovato. Esegui 'make build' prima."; \
	fi
else
	@if [ -f "dist/WTF Modpack Launcher" ]; then \
		"./dist/WTF Modpack Launcher"; \
	else \
		echo "❌ Eseguibile non trovato. Esegui 'make build' prima."; \
	fi
endif
	rm -rf launcher_env/
	rm -rf *.pyc
	rm -f settings.json
	@echo "✅ Pulizia completata"
