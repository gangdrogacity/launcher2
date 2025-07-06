@echo off
title Compilazione WTF Modpack Launcher
color 0A

echo.
echo ========================================
echo  WTF MODPACK LAUNCHER - BUILD SCRIPT
echo ========================================
echo.

echo 🔍 Verifica dipendenze...
python -c "import pyinstaller" >nul 2>&1
if errorlevel 1 (
    echo ❌ PyInstaller non trovato!
    echo 💡 Installazione in corso...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ Errore durante l'installazione di PyInstaller
        pause
        exit /b 1
    )
)
echo ✅ PyInstaller trovato

echo.
echo 🔨 Avvio compilazione...
echo ⏳ Questo processo può richiedere alcuni minuti...
echo.

pyinstaller --clean wtf_launcher.spec

if errorlevel 1 (
    echo.
    echo ❌ Errore durante la compilazione!
    echo 💡 Controlla i messaggi di errore sopra
    pause
    exit /b 1
)

echo.
echo ✅ Compilazione completata!

if exist "dist\WTF_Modpack_Launcher.exe" (
    echo 📦 Eseguibile creato: dist\WTF_Modpack_Launcher.exe
    
    echo.
    echo 📁 Creazione directory di release...
    if exist "WTF_Modpack_Launcher_Release" rmdir /s /q "WTF_Modpack_Launcher_Release"
    mkdir "WTF_Modpack_Launcher_Release"
    
    echo 📄 Copia file...
    copy "dist\WTF_Modpack_Launcher.exe" "WTF_Modpack_Launcher_Release\" >nul
    if exist "README_WTF.md" copy "README_WTF.md" "WTF_Modpack_Launcher_Release\" >nul
    if exist "requirements_wtf.txt" copy "requirements_wtf.txt" "WTF_Modpack_Launcher_Release\" >nul
    if exist "wtf_modpack_config.json" copy "wtf_modpack_config.json" "WTF_Modpack_Launcher_Release\" >nul
    
    echo 📁 Copia directory...
    if exist "img" xcopy "img" "WTF_Modpack_Launcher_Release\img\" /E /I /Q >nul
    if exist "fonts" xcopy "fonts" "WTF_Modpack_Launcher_Release\fonts\" /E /I /Q >nul
    if exist "config" xcopy "config" "WTF_Modpack_Launcher_Release\config\" /E /I /Q >nul
    
    echo.
    echo 🎉 COMPILAZIONE COMPLETATA CON SUCCESSO!
    echo.
    echo 📦 Il launcher è pronto nella cartella:
    echo    WTF_Modpack_Launcher_Release\
    echo.
    echo 🚀 Per avviare il launcher:
    echo    WTF_Modpack_Launcher_Release\WTF_Modpack_Launcher.exe
    echo.
    
    choice /C YN /M "Vuoi aprire la cartella di release ora? (Y/N)"
    if !errorlevel!==1 start "" "WTF_Modpack_Launcher_Release"
    
) else (
    echo ❌ Eseguibile non trovato!
    echo 💡 Controlla gli errori di compilazione
)

echo.
pause
