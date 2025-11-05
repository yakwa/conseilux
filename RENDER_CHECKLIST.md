# ✅ Checklist Déploiement Render

## 📋 Avant de commencer

### Prérequis
- [ ] Compte GitHub/GitLab/Bitbucket créé
- [ ] Code poussé sur un dépôt Git
- [ ] Compte Gmail avec validation en 2 étapes activée
- [ ] Compte Supabase créé (recommandé)

## 🔧 Configuration locale

### 1. Vérifier les fichiers
- [ ] `render.yaml` existe
- [ ] `build.sh` existe
- [ ] `requirements.txt` contient `gunicorn`
- [ ] `runtime.txt` spécifie `python-3.11.0`
- [ ] `.env.example` est à jour

### 2. Tester localement (optionnel)
```bash
# Créer un environnement virtuel
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt

# Créer un fichier .env avec vos variables
copy .env.example .env
# Puis éditez .env avec vos vraies valeurs

# Lancer l'application
python main.py
```

### 3. Pousser le code
```bash
git add .
git commit -m "Configuration Render complète"
git push
```

**OU** utilisez le script automatique :
```bash
deploy_render.bat
```

## 🌐 Sur Render.com

### 1. Créer le compte
- [ ] Allez sur [render.com](https://render.com)
- [ ] Inscrivez-vous (gratuit)
- [ ] Connectez votre compte GitHub/GitLab

### 2. Créer le service

#### Option A : Avec Blueprint (Automatique - Recommandé)
- [ ] Cliquez sur **"New +"** → **"Blueprint"**
- [ ] Sélectionnez votre dépôt `conseilux`
- [ ] Render détecte `render.yaml` automatiquement
- [ ] Cliquez sur **"Apply"**

#### Option B : Manuel
- [ ] Cliquez sur **"New +"** → **"Web Service"**
- [ ] Sélectionnez votre dépôt
- [ ] Configurez :
  - Name: `conseilux`
  - Runtime: `Python 3`
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `gunicorn main:app`

### 3. Variables d'environnement

Dans **Environment** → **Environment Variables**, ajoutez :

#### Variables obligatoires
```
SECRET_KEY=<générez avec la commande ci-dessous>
ADMIN_PASSWORD=VotreMotDePasseAdmin123!
MAIL_USERNAME=votre-email@gmail.com
MAIL_PASSWORD=<mot de passe d'application Gmail>
MAIL_DEFAULT_SENDER=contact@conseilux-training.com
```

#### Variables Supabase (recommandé)
```
SUPABASE_URL=https://votre-projet.supabase.co
SUPABASE_KEY=votre-cle-anon-publique
```

#### Variables optionnelles (avec valeurs par défaut)
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
```

### 4. Générer SECRET_KEY

Sur votre ordinateur, exécutez :
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copiez le résultat dans la variable `SECRET_KEY`.

### 5. Configurer Gmail

- [ ] Allez sur [myaccount.google.com](https://myaccount.google.com)
- [ ] **Sécurité** → **Validation en deux étapes** (activez si nécessaire)
- [ ] **Mots de passe des applications**
- [ ] Créez un nouveau mot de passe pour "Conseilux"
- [ ] Copiez ce mot de passe dans `MAIL_PASSWORD`

### 6. Configurer Supabase (recommandé)

- [ ] Allez sur [supabase.com](https://supabase.com)
- [ ] Créez un nouveau projet
- [ ] Notez l'URL du projet (dans Settings → API)
- [ ] Notez la clé `anon/public` (dans Settings → API)
- [ ] Ajoutez ces valeurs dans Render

## 🚀 Déploiement

### 1. Lancer le déploiement
- [ ] Dans Render, le déploiement démarre automatiquement
- [ ] Attendez 2-5 minutes
- [ ] Surveillez les logs en temps réel

### 2. Vérifier le déploiement
- [ ] Le build se termine avec succès (vert)
- [ ] L'application démarre sans erreur
- [ ] Vous recevez une URL : `https://conseilux.onrender.com`

### 3. Tester l'application
- [ ] Ouvrez l'URL dans votre navigateur
- [ ] Vérifiez que le site s'affiche correctement
- [ ] Testez le formulaire de contact
- [ ] Testez l'inscription newsletter
- [ ] Testez l'accès admin : `/admin/newsletter`

## 🔍 Vérifications post-déploiement

### Fonctionnalités à tester
- [ ] Page d'accueil s'affiche
- [ ] Navigation fonctionne
- [ ] Formulaire de contact envoie des emails
- [ ] Newsletter : inscription fonctionne
- [ ] Admin newsletter : connexion fonctionne
- [ ] Images et CSS chargent correctement
- [ ] Favicon s'affiche

### En cas de problème
1. **Consultez les logs** dans le dashboard Render
2. **Vérifiez les variables d'environnement**
3. **Vérifiez le mot de passe Gmail** (doit être un mot de passe d'application)
4. **Redéployez** si nécessaire (Manual Deploy)

## 🎯 Optimisations (optionnel)

### Éviter que le service s'endorme (plan gratuit)
Le plan gratuit de Render endort le service après 15 min d'inactivité.

**Solutions :**
1. **Passer au plan payant** ($7/mois) - Service toujours actif
2. **Utiliser un service de ping** (UptimeRobot, cron-job.org)
3. **Accepter le délai** de 30s au premier chargement

### Ajouter un domaine personnalisé
- [ ] Dans Render : **Settings** → **Custom Domain**
- [ ] Ajoutez votre domaine (ex: `www.conseilux-training.com`)
- [ ] Configurez les DNS chez votre registrar (OVH, etc.)
- [ ] Attendez la propagation DNS (quelques heures)

### Configurer PostgreSQL (pour données permanentes)
- [ ] Dans Render : **New +** → **PostgreSQL**
- [ ] Créez une base de données
- [ ] Ajoutez `psycopg2-binary` à `requirements.txt`
- [ ] Modifiez `main.py` pour utiliser `DATABASE_URL`

## 📊 Monitoring

### Vérifier la santé du service
- [ ] Dashboard Render → **Metrics**
- [ ] Vérifiez CPU, Mémoire, Requêtes
- [ ] Consultez les logs régulièrement

### Redéploiement automatique
- [ ] Chaque `git push` redéploie automatiquement
- [ ] Surveillez les notifications Render par email

## 🎉 Félicitations !

Votre site Conseilux est maintenant en ligne sur Render !

**URL de votre site :** `https://conseilux.onrender.com`

---

## 📚 Ressources

- [Guide rapide](QUICKSTART_RENDER.md)
- [Guide complet](DEPLOY_RENDER.md)
- [Vercel vs Render](VERCEL_VS_RENDER.md)
- [Documentation Render](https://render.com/docs)
- [Support Render](https://render.com/support)

## 🆘 Besoin d'aide ?

1. Consultez les logs dans Render
2. Vérifiez les variables d'environnement
3. Relisez les guides de déploiement
4. Contactez le support Render (très réactif)
