# 📚 Guide Complet - Hébergement sur GitHub

## 🎯 Objectif
Héberger le code source de Conseilux sur GitHub et le déployer en ligne.

---

## 📋 Prérequis

### 1. Créer un compte GitHub
- Allez sur [github.com](https://github.com)
- Cliquez sur "Sign up"
- Suivez les instructions

### 2. Installer Git (si pas déjà fait)
- Téléchargez depuis [git-scm.com](https://git-scm.com/download/win)
- Installez avec les options par défaut
- Redémarrez votre terminal

---

## 🚀 Étapes de Déploiement

### Étape 1 : Créer un Repository sur GitHub

1. **Connectez-vous** à GitHub
2. **Cliquez** sur le bouton vert "New" ou "+" en haut à droite
3. **Remplissez** les informations :
   - **Repository name** : `conseilux` (ou autre nom)
   - **Description** : "Site web Conseilux Training & Developpement"
   - **Visibilité** : Public ou Private (selon votre choix)
   - ⚠️ **NE PAS** cocher "Add a README file"
   - ⚠️ **NE PAS** ajouter .gitignore
   - ⚠️ **NE PAS** choisir de licence
4. **Cliquez** sur "Create repository"

### Étape 2 : Configurer Git localement

Ouvrez PowerShell dans le dossier Conseilux et exécutez :

```powershell
# Configurer votre nom (première fois seulement)
git config --global user.name "Votre Nom"

# Configurer votre email (première fois seulement)
git config --global user.email "votre.email@example.com"
```

### Étape 3 : Pousser le code sur GitHub

**Option A : Utiliser le script automatique**

Double-cliquez sur `deploy_github.bat` et suivez les instructions.

**Option B : Commandes manuelles**

```powershell
# 1. Ajouter tous les fichiers
git add .

# 2. Créer un commit
git commit -m "Premier commit - Site Conseilux"

# 3. Renommer la branche en main
git branch -M main

# 4. Ajouter le repository distant (remplacez USERNAME par votre nom d'utilisateur)
git remote add origin https://github.com/USERNAME/conseilux.git

# 5. Pousser le code
git push -u origin main
```

### Étape 4 : Vérifier sur GitHub

1. Allez sur votre repository : `https://github.com/USERNAME/conseilux`
2. Vous devriez voir tous vos fichiers !

---

## 🌐 Déployer le Site en Ligne

### Option 1 : Render.com (Recommandé - Gratuit)

#### Avantages :
- ✅ Gratuit
- ✅ Facile à configurer
- ✅ Support Python/Flask
- ✅ Base de données PostgreSQL gratuite
- ✅ HTTPS automatique

#### Étapes :

1. **Créer un compte** sur [render.com](https://render.com)

2. **Connecter GitHub** :
   - Cliquez sur "New +"
   - Sélectionnez "Web Service"
   - Connectez votre compte GitHub
   - Sélectionnez le repository "conseilux"

3. **Configurer le service** :
   - **Name** : `conseilux`
   - **Environment** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn main:app`
   - **Instance Type** : `Free`

4. **Ajouter les variables d'environnement** :
   - Cliquez sur "Environment"
   - Ajoutez :
     - `SUPABASE_URL` = votre URL Supabase
     - `SUPABASE_KEY` = votre clé Supabase
     - `SECRET_KEY` = une clé secrète aléatoire

5. **Déployer** :
   - Cliquez sur "Create Web Service"
   - Attendez 5-10 minutes
   - Votre site sera disponible à : `https://conseilux.onrender.com`

---

### Option 2 : Vercel (Gratuit)

#### Avantages :
- ✅ Gratuit
- ✅ Très rapide
- ✅ Déploiement automatique à chaque push

#### Étapes :

1. Allez sur [vercel.com](https://vercel.com)
2. Connectez votre compte GitHub
3. Importez le repository "conseilux"
4. Configurez les variables d'environnement
5. Déployez !

---

### Option 3 : Heroku (Payant après essai)

#### Étapes :

1. Créez un compte sur [heroku.com](https://heroku.com)
2. Installez Heroku CLI
3. Exécutez :

```bash
heroku login
heroku create conseilux
heroku config:set SUPABASE_URL=votre_url
heroku config:set SUPABASE_KEY=votre_cle
heroku config:set SECRET_KEY=votre_secret
git push heroku main
```

---

## 🔄 Mettre à Jour le Site

Après avoir fait des modifications :

```powershell
# 1. Ajouter les modifications
git add .

# 2. Créer un commit
git commit -m "Description des modifications"

# 3. Pousser sur GitHub
git push origin main
```

Le site se mettra à jour automatiquement sur Render/Vercel !

---

## 📝 Fichiers Importants Créés

- ✅ `.gitignore` - Fichiers à ignorer (comme .env)
- ✅ `README.md` - Documentation du projet
- ✅ `requirements.txt` - Dépendances Python
- ✅ `runtime.txt` - Version de Python
- ✅ `Procfile` - Configuration pour Heroku

---

## ⚠️ IMPORTANT - Sécurité

### Ne JAMAIS pousser sur GitHub :
- ❌ Le fichier `.env` (contient vos secrets)
- ❌ Les mots de passe
- ❌ Les clés API
- ❌ Les tokens d'accès

Le fichier `.gitignore` empêche automatiquement cela !

---

## 🆘 Résolution de Problèmes

### Problème : "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/USERNAME/conseilux.git
```

### Problème : "Permission denied"
- Vérifiez que vous êtes connecté à GitHub
- Utilisez un Personal Access Token au lieu du mot de passe

### Problème : Le site ne démarre pas sur Render
- Vérifiez les logs dans le dashboard Render
- Assurez-vous que toutes les variables d'environnement sont définies
- Vérifiez que `requirements.txt` contient toutes les dépendances

---

## 📞 Besoin d'Aide ?

Si vous rencontrez des problèmes :
1. Vérifiez les logs d'erreur
2. Consultez la documentation GitHub
3. Contactez le support de la plateforme de déploiement

---

## ✅ Checklist Finale

- [ ] Code poussé sur GitHub
- [ ] Variables d'environnement configurées
- [ ] Site déployé et accessible
- [ ] Base de données Supabase connectée
- [ ] Formulaires de contact fonctionnels
- [ ] Favicon visible
- [ ] Site responsive (mobile/tablette/desktop)

---

## 🎉 Félicitations !

Votre site Conseilux est maintenant hébergé et accessible en ligne ! 🚀

**URL GitHub** : `https://github.com/USERNAME/conseilux`
**URL du site** : `https://conseilux.onrender.com` (ou autre selon la plateforme)
