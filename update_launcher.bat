@echo off
echo ========================================
echo WTF Modpack Launcher Auto-Update
echo ========================================
echo Aggiornamento in corso...
echo Data: %DATE% %TIME%
echo.

timeout /t 2 /nobreak > nul

echo Terminando processi del launcher...
REM Termina eventuali processi del launcher
taskkill /f /im "WTF_Modpack_Launcher.exe" 2>nul
taskkill /f /im "WTF_Modpack_Launcher.exe" 2>nul
taskkill /f /im "main.exe" 2>nul
taskkill /f /im "python.exe" 2>nul

echo Attendo chiusura processi...
timeout /t 5 /nobreak > nul

echo Creando backup dell'eseguibile corrente...
REM Crea backup dell'eseguibile corrente
if exist "C:\Users\sderl\Documents\launcher2\WTF_Modpack_Launcher.exe" (
    copy "C:\Users\sderl\Documents\launcher2\WTF_Modpack_Launcher.exe" "C:\Users\sderl\Documents\launcher2\WTF_Modpack_Launcher.exe.backup" >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Backup creato: C:\Users\sderl\Documents\launcher2\WTF_Modpack_Launcher.exe.backup
    ) else (
        echo ⚠️ Errore nella creazione del backup
    )
) else (
    echo ⚠️ File corrente non trovato: C:\Users\sderl\Documents\launcher2\WTF_Modpack_Launcher.exe
)

echo Sostituendo l'eseguibile...
REM Sostituisce l'eseguibile
copy "C:\Users\sderl\Documents\launcher2\WTF_Modpack_Launcher.exe" "C:\Users\sderl\Documents\launcher2\WTF_Modpack_Launcher.exe" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Errore nella sostituzione del file!
    echo Tentativo di ripristino backup...
    if exist "C:\Users\sderl\Documents\launcher2\WTF_Modpack_Launcher.exe.backup" (
        copy "C:\Users\sderl\Documents\launcher2\WTF_Modpack_Launcher.exe.backup" "C:\Users\sderl\Documents\launcher2\WTF_Modpack_Launcher.exe" >nul 2>&1
        if %errorlevel% equ 0 (
            echo ✅ Backup ripristinato
        ) else (
            echo ❌ Errore nel ripristino backup
        )
    )
    echo.
    echo Premere un tasto per continuare...
    pause
    exit /b 1
) else (
    echo ✅ Eseguibile aggiornato con successo
)

REM Aggiorna il file di versione
echo Aggiornando file di versione...
echo 1.0.1-custom> "C:\Users\sderl\Documents\launcher2\launcher_version.txt"
if %errorlevel% equ 0 (
    echo ✅ File versione aggiornato
) else (
    echo ⚠️ Errore nell'aggiornamento del file versione
)

echo.
echo ========================================
echo Aggiornamento completato con successo!
echo ========================================
echo.

echo Riavviando il launcher...
REM Usa lo script di riavvio separato se disponibile
start "" "C:\Users\sderl\Documents\launcher2\restart_launcher.bat"
if %errorlevel% equ 0 (
    echo ✅ Script di riavvio avviato
    goto cleanup
)

:cleanup
echo Pulizia file temporanei...
timeout /t 3 /nobreak > nul

REM Pulisce i file temporanei
if exist "C:\Users\sderl\Documents\launcher2\WTF_Modpack_Launcher.exe.backup" (
    del "C:\Users\sderl\Documents\launcher2\WTF_Modpack_Launcher.exe.backup" >nul 2>&1
    echo ✅ Backup rimosso
)

REM Rimuove il file di aggiornamento nella cartella del launcher
if exist "C:\Users\sderl\Documents\launcher2\WTF_Modpack_Launcher.exe" (
    del "C:\Users\sderl\Documents\launcher2\WTF_Modpack_Launcher.exe" >nul 2>&1
    echo ✅ File di aggiornamento rimosso
)

REM Rimuove lo script di riavvio dopo un breve ritardo
timeout /t 5 /nobreak > nul
if exist "C:\Users\sderl\Documents\launcher2\restart_launcher.bat" (
    del "C:\Users\sderl\Documents\launcher2\restart_launcher.bat" >nul 2>&1
)

echo.
echo Aggiornamento completato!
echo Il launcher dovrebbe essere riavviato.
echo.
timeout /t 2 /nobreak > nul

REM Rimuove lo script stesso
del "%~f0" >nul 2>&1
