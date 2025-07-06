@echo off
title WTF Modpack Launcher - Compilazione
echo 🚀 Compilazione WTF Modpack Launcher...
echo.

REM Verifica che PyInstaller sia installato
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo ❌ PyInstaller non trovato!
    echo 💡 Installa con: pip install pyinstaller
    pause
    exit /b 1
)

echo ✅ PyInstaller trovato
echo.

REM Pulisci directory precedenti
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo 🧹 Directory pulite
echo.

REM Compila il launcher
echo ⚙️ Avvio compilazione...
pyinstaller main.spec

if errorlevel 1 (
    echo.
    echo ❌ Errore durante la compilazione!
    pause
    exit /b 1
)

echo.
echo 🎉 Compilazione completata!
echo 📦 Eseguibile disponibile in: dist\WTF_Modpack_Launcher.exe
echo.
pause
