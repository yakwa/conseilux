@echo off
echo ========================================
echo   Preparation pour deploiement Render
echo ========================================
echo.

REM Vérifier si Git est installé
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Git n'est pas installe ou n'est pas dans le PATH
    echo Installez Git depuis: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1/4] Verification des fichiers...
if not exist "render.yaml" (
    echo [ERREUR] render.yaml manquant!
    pause
    exit /b 1
)
if not exist "requirements.txt" (
    echo [ERREUR] requirements.txt manquant!
    pause
    exit /b 1
)
echo [OK] Tous les fichiers necessaires sont presents

echo.
echo [2/4] Ajout des fichiers au depot Git...
git add .
if errorlevel 1 (
    echo [ERREUR] Impossible d'ajouter les fichiers
    pause
    exit /b 1
)
echo [OK] Fichiers ajoutes

echo.
echo [3/4] Creation du commit...
git commit -m "Configuration Render complete - pret pour deploiement"
if errorlevel 1 (
    echo [INFO] Aucun changement a commiter ou commit deja effectue
)
echo [OK] Commit cree

echo.
echo [4/4] Push vers le depot distant...
git push
if errorlevel 1 (
    echo [ERREUR] Impossible de pusher vers le depot distant
    echo Verifiez que vous avez configure un depot distant (GitHub/GitLab)
    echo.
    echo Pour configurer un depot distant:
    echo   git remote add origin https://github.com/votre-username/conseilux.git
    echo   git push -u origin main
    pause
    exit /b 1
)
echo [OK] Code pousse vers le depot distant

echo.
echo ========================================
echo   Preparation terminee avec succes!
echo ========================================
echo.
echo Prochaines etapes:
echo 1. Allez sur https://dashboard.render.com
echo 2. Cliquez sur "New +" puis "Blueprint"
echo 3. Selectionnez votre depot
echo 4. Render detectera automatiquement render.yaml
echo 5. Configurez les variables d'environnement
echo 6. Cliquez sur "Apply"
echo.
echo Consultez QUICKSTART_RENDER.md pour plus de details
echo.
pause
