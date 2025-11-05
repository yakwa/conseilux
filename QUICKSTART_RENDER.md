# Guide Rapide - Déploiement Render

## 🚀 Déploiement en 5 minutes

### 1️⃣ Préparer le code
```bash
git add .
git commit -m "Prêt pour Render"
git push
```

### 2️⃣ Créer le service sur Render

1. Allez sur [render.com](https://render.com) et connectez-vous
2. Cliquez sur **"New +"** → **"Blueprint"**
3. Sélectionnez votre dépôt GitHub/GitLab
4. Render détectera automatiquement `render.yaml`
5. Cliquez sur **"Apply"**

### 3️⃣ Configurer les variables d'environnement

Dans le dashboard Render, allez dans **Environment** et ajoutez :

```
SECRET_KEY=<générez avec: python -c "import secrets; print(secrets.token_hex(32))">
ADMIN_PASSWORD=VotreMotDePasseAdmin123!
MAIL_USERNAME=votre-email@gmail.com
MAIL_PASSWORD=<mot de passe d'application Gmail>
MAIL_DEFAULT_SENDER=contact@conseilux-training.com
SUPABASE_URL=<votre URL Supabase>
SUPABASE_KEY=<votre clé Supabase>
```

### 4️⃣ Obtenir un mot de passe d'application Gmail

1. Allez sur [myaccount.google.com](https://myaccount.google.com)
2. **Sécurité** → **Validation en deux étapes** (activez-la si nécessaire)
3. **Mots de passe des applications** → Créez un nouveau mot de passe
4. Copiez ce mot de passe dans `MAIL_PASSWORD`

### 5️⃣ Déployer !

Render va automatiquement :
- ✅ Installer les dépendances
- ✅ Démarrer l'application avec Gunicorn
- ✅ Vous donner une URL : `https://conseilux.onrender.com`

## ⚠️ Important : Base de données

Par défaut, l'app utilise SQLite en mémoire (les données sont perdues au redémarrage).

**Solution recommandée** : Utilisez Supabase (gratuit)
- Créez un compte sur [supabase.com](https://supabase.com)
- Créez un projet
- Ajoutez `SUPABASE_URL` et `SUPABASE_KEY` dans Render

## 🔄 Mises à jour automatiques

Chaque `git push` redéploiera automatiquement votre site !

## 📝 Fichiers créés pour Render

- ✅ `render.yaml` - Configuration du service
- ✅ `build.sh` - Script de build
- ✅ `main.py` - Modifié pour supporter Render
- ✅ `requirements.txt` - Dépendances Python

## 🆘 Besoin d'aide ?

Consultez `DEPLOY_RENDER.md` pour le guide complet.
