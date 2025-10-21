@echo off
echo ========================================
echo   MISE A JOUR GITHUB - CONSEILUX
echo ========================================
echo.

REM Demander le message de commit
set /p message="Entrez le message de commit: "

echo.
echo [1/3] Ajout des fichiers modifies...
git add .

echo [2/3] Creation du commit...
git commit -m "%message%"

echo [3/3] Envoi vers GitHub...
git push origin main

echo.
echo ========================================
echo   MISE A JOUR TERMINEE !
echo ========================================
echo.
echo Votre code a ete pousse sur GitHub.
echo Si vous utilisez Render, le site se mettra a jour automatiquement.
echo.
pause
