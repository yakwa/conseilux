# Déploiement sur Render

## Étapes de déploiement

### 1. Préparer votre dépôt Git

Assurez-vous que tous vos fichiers sont commités dans un dépôt Git (GitHub, GitLab, ou Bitbucket).

```bash
git add .
git commit -m "Configuration pour Render"
git push
```

### 2. Créer un compte Render

1. Allez sur [render.com](https://render.com)
2. Créez un compte gratuit ou connectez-vous

### 3. Déployer l'application

#### Option A: Déploiement automatique avec render.yaml (Recommandé)

1. Dans le dashboard Render, cliquez sur **"New +"** → **"Blueprint"**
2. Connectez votre dépôt Git
3. Render détectera automatiquement le fichier `render.yaml` et configurera tout

#### Option B: Déploiement manuel

1. Dans le dashboard Render, cliquez sur **"New +"** → **"Web Service"**
2. Connectez votre dépôt Git
3. Configurez les paramètres suivants :
   - **Name**: conseilux (ou le nom de votre choix)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app`

### 4. Configurer les variables d'environnement

Dans les paramètres de votre service Render, ajoutez ces variables d'environnement :

**Variables obligatoires :**
- `SECRET_KEY` : Une clé secrète aléatoire (générez-en une avec `python -c "import secrets; print(secrets.token_hex(32))"`)
- `ADMIN_PASSWORD` : Le mot de passe pour accéder à l'interface admin
- `MAIL_USERNAME` : Votre adresse email Gmail
- `MAIL_PASSWORD` : Le mot de passe d'application Gmail (voir ci-dessous)
- `MAIL_DEFAULT_SENDER` : Votre adresse email d'envoi (ex: contact@conseiluxtraining.com)

**Variables optionnelles (avec valeurs par défaut) :**
- `MAIL_SERVER` : smtp.gmail.com (par défaut)
- `MAIL_PORT` : 587 (par défaut)
- `MAIL_USE_TLS` : True (par défaut)
- `MAIL_USE_SSL` : False (par défaut)

**Variables Supabase (si utilisées) :**
- `SUPABASE_URL` : L'URL de votre projet Supabase
- `SUPABASE_KEY` : La clé API de votre projet Supabase

### 5. Configuration Gmail pour l'envoi d'emails

Pour utiliser Gmail avec votre application :

1. Activez la validation en deux étapes sur votre compte Google
2. Générez un "Mot de passe d'application" :
   - Allez dans les paramètres de votre compte Google
   - Sécurité → Validation en deux étapes → Mots de passe des applications
   - Créez un nouveau mot de passe pour "Autre (nom personnalisé)"
   - Utilisez ce mot de passe comme valeur pour `MAIL_PASSWORD`

### 6. Base de données (Important)

**Note importante** : Par défaut, l'application utilise SQLite en mémoire sur Render, ce qui signifie que **les données seront perdues à chaque redémarrage**.

Pour une solution permanente, vous avez deux options :

#### Option 1: Utiliser Supabase (Recommandé - Gratuit)
1. Créez un compte sur [supabase.com](https://supabase.com)
2. Créez un nouveau projet
3. Ajoutez les variables `SUPABASE_URL` et `SUPABASE_KEY` dans Render
4. L'application utilise déjà Supabase (voir le code dans main.py)

#### Option 2: Ajouter PostgreSQL sur Render
1. Dans Render, créez une nouvelle base de données PostgreSQL
2. Ajoutez `psycopg2-binary` à `requirements.txt`
3. Modifiez `main.py` pour utiliser la variable d'environnement `DATABASE_URL`

### 7. Déploiement

Une fois tout configuré :
1. Render va automatiquement construire et déployer votre application
2. Vous recevrez une URL du type : `https://conseilux.onrender.com`
3. Le déploiement prend généralement 2-5 minutes

### 8. Domaine personnalisé (Optionnel)

Pour utiliser votre propre domaine :
1. Allez dans les paramètres de votre service Render
2. Section "Custom Domain"
3. Ajoutez votre domaine et suivez les instructions pour configurer les DNS

## Redéploiement automatique

Render redéploiera automatiquement votre application à chaque push sur la branche principale de votre dépôt Git.

## Dépannage

### L'application ne démarre pas
- Vérifiez les logs dans le dashboard Render
- Assurez-vous que toutes les variables d'environnement sont configurées
- Vérifiez que `requirements.txt` contient toutes les dépendances

### Les emails ne s'envoient pas
- Vérifiez que vous utilisez un mot de passe d'application Gmail
- Vérifiez que les variables `MAIL_USERNAME` et `MAIL_PASSWORD` sont correctes

### Les données disparaissent
- Configurez une base de données permanente (Supabase ou PostgreSQL)

## Support

Pour plus d'informations, consultez la [documentation Render](https://render.com/docs).
