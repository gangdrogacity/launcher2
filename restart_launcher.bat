@echo off
echo Riavvio del launcher in corso...
timeout /t 2 /nobreak > nul

REM Prova diversi metodi per riavviare il launcher
echo Tentativo 1: start con directory di lavoro
cd /d "C:\Users\sderl\Documents\launcher2"
start "" "C:\Users\sderl\Documents\launcher2\WTF_Modpack_Launcher.exe"
if %errorlevel% equ 0 goto success

echo Tentativo 2: start senza directory
start "" "C:\Users\sderl\Documents\launcher2\WTF_Modpack_Launcher.exe"
if %errorlevel% equ 0 goto success

echo Tentativo 3: esecuzione diretta
"C:\Users\sderl\Documents\launcher2\WTF_Modpack_Launcher.exe"
if %errorlevel% equ 0 goto success

echo Tentativo 4: explorer
explorer "C:\Users\sderl\Documents\launcher2\WTF_Modpack_Launcher.exe"
if %errorlevel% equ 0 goto success

echo ❌ Impossibile riavviare automaticamente
echo 💡 Apri manualmente: C:\Users\sderl\Documents\launcher2\WTF_Modpack_Launcher.exe
pause
goto end

:success
echo ✅ Launcher riavviato con successo!

:end
REM Rimuove questo script
timeout /t 1 /nobreak > nul
del "%~f0" 2>nul
