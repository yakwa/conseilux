@echo off
echo ========================================
echo   DEPLOIEMENT GITHUB - CONSEILUX
echo ========================================
echo.

REM Vérifier si Git est installé
git --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Git n'est pas installé!
    echo Téléchargez Git depuis: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1/5] Ajout des fichiers...
git add .

echo [2/5] Création du commit...
git commit -m "Mise a jour du site Conseilux"

echo [3/5] Vérification de la branche...
git branch -M main

echo [4/5] Affichage du statut...
git status

echo.
echo ========================================
echo   PROCHAINES ETAPES
echo ========================================
echo.
echo 1. Allez sur GitHub.com et créez un nouveau repository
echo 2. Nommez-le "conseilux" (ou autre nom)
echo 3. NE PAS initialiser avec README, .gitignore ou licence
echo 4. Copiez l'URL du repository (exemple: https://github.com/USERNAME/conseilux.git)
echo 5. Exécutez ces commandes:
echo.
echo    git remote add origin https://github.com/USERNAME/conseilux.git
echo    git push -u origin main
echo.
echo ========================================
pause
