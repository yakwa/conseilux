# 📁 Structure du Projet Conseilux

## 🗂️ Organisation des fichiers

```
Conseilux/
├── 📄 Configuration et déploiement
│   ├── render.yaml              # Configuration Render (nouveau)
│   ├── vercel.json              # Configuration Vercel (existant)
│   ├── build.sh                 # Script de build Render (nouveau)
│   ├── requirements.txt         # Dépendances Python
│   ├── runtime.txt              # Version Python (3.11.0)
│   ├── Procfile                 # Configuration Heroku (legacy)
│   ├── .env                     # Variables d'environnement (local, gitignored)
│   ├── .env.example             # Template des variables
│   └── .gitignore               # Fichiers à ignorer par Git
│
├── 🐍 Code Python
│   ├── main.py                  # Application Flask principale
│   ├── app.py                   # Point d'entrée alternatif
│   ├── api/
│   │   └── index.py            # Point d'entrée Vercel serverless
│   └── optimize_images.py      # Script d'optimisation d'images
│
├── 🎨 Frontend
│   ├── index.html              # Page d'accueil (racine)
│   ├── templates/              # Templates Jinja2
│   │   ├── base.html          # Template de base
│   │   ├── index.html         # Page d'accueil (template)
│   │   ├── solutions_fixed.html
│   │   ├── modalites.html
│   │   ├── contact.html
│   │   ├── admin_newsletter.html
│   │   └── ...                # Autres pages
│   └── static/                 # Fichiers statiques
│       ├── css/               # Feuilles de style
│       ├── js/                # Scripts JavaScript
│       └── images/            # Images et logos
│
├── 💾 Base de données
│   ├── instance/              # Dossier SQLite (local)
│   │   └── newsletter.db     # Base de données locale (gitignored)
│   └── supabase_migration.sql # Script de migration Supabase
│
├── 📚 Documentation
│   ├── README.md                      # Documentation principale
│   ├── RENDER_SETUP_COMPLETE.md      # Résumé configuration Render ✨
│   ├── QUICKSTART_RENDER.md          # Guide rapide Render ✨
│   ├── DEPLOY_RENDER.md              # Guide complet Render ✨
│   ├── RENDER_CHECKLIST.md           # Checklist déploiement ✨
│   ├── VERCEL_VS_RENDER.md           # Comparaison plateformes ✨
│   ├── STRUCTURE_PROJET.md           # Ce fichier ✨
│   ├── DEPLOIEMENT_RAPIDE.md         # Guide Vercel
│   ├── GUIDE_GITHUB.md               # Guide GitHub
│   ├── GUIDE_DOMAINE_OVH.md          # Configuration domaine
│   ├── SUPABASE_SETUP.md             # Configuration Supabase
│   ├── MIGRATION_GUIDE.md            # Migration de données
│   ├── OPTIMISATION_GUIDE.md         # Optimisations
│   ├── RESPONSIVITE_GUIDE.md         # Guide responsive
│   └── FAVICON_GUIDE.md              # Configuration favicon
│
└── 🔧 Scripts utilitaires
    ├── deploy_render.bat       # Script déploiement Render (Windows) ✨
    ├── deploy_github.bat       # Script déploiement GitHub
    └── push_github.bat         # Script push Git

✨ = Nouveaux fichiers pour Render
```

## 📝 Fichiers clés

### Configuration Render (Nouveaux)

#### `render.yaml`
Configuration automatique du service Render. Définit :
- Type de service (web)
- Runtime (Python)
- Commandes de build et démarrage
- Variables d'environnement

#### `build.sh`
Script exécuté lors du build sur Render :
- Installation des dépendances
- Création des répertoires nécessaires

### Application Flask

#### `main.py` (Principal)
Fichier principal de l'application Flask :
- Configuration de l'app
- Routes et endpoints
- Gestion de la newsletter
- Envoi d'emails
- Interface admin
- **Modifié pour supporter Render** ✅

#### `app.py`
Point d'entrée alternatif qui importe `main.py`

#### `api/index.py`
Point d'entrée spécifique pour Vercel (serverless)

### Templates et Static

#### `templates/`
Templates Jinja2 pour le rendu HTML :
- `base.html` : Template parent avec navigation
- Pages individuelles qui étendent `base.html`

#### `static/`
Ressources statiques :
- **CSS** : Styles personnalisés
- **JS** : Scripts JavaScript
- **Images** : Logos, photos, icônes

### Configuration

#### `.env` (Local uniquement)
Variables d'environnement locales :
- Identifiants email
- Clés secrètes
- Configuration Supabase
- **Non versionné (gitignored)**

#### `.env.example`
Template des variables d'environnement :
- À copier en `.env` pour le développement local
- Référence pour les variables Render

#### `requirements.txt`
Dépendances Python :
```
Flask==3.0.3
Flask-Mail==0.10.0
Flask-SQLAlchemy==3.1.1
supabase==2.3.4
python-dotenv==1.0.0
gunicorn==21.2.0
Pillow==10.2.0
```

## 🔄 Flux de déploiement

### Développement local
```
1. Modifier le code
2. Tester avec: python main.py
3. Commit: git commit -m "..."
4. Push: git push
```

### Déploiement Render
```
1. Git push déclenche le build
2. Render exécute build.sh
3. Render installe requirements.txt
4. Render démarre avec: gunicorn main:app
5. Application en ligne !
```

### Déploiement Vercel (alternatif)
```
1. Git push déclenche le build
2. Vercel lit vercel.json
3. Vercel build api/index.py
4. Fonctions serverless déployées
```

## 🎯 Points d'entrée

### Pour Render
- **Fichier principal** : `main.py`
- **Commande** : `gunicorn main:app`
- **Port** : Automatique (variable `PORT`)

### Pour Vercel
- **Fichier principal** : `api/index.py`
- **Type** : Serverless function
- **Configuration** : `vercel.json`

### Pour développement local
- **Fichier** : `main.py`
- **Commande** : `python main.py`
- **Port** : 5000 (par défaut Flask)

## 📊 Base de données

### Développement local
- **Type** : SQLite
- **Fichier** : `instance/newsletter.db`
- **Création** : Automatique au premier lancement

### Production Render (par défaut)
- **Type** : SQLite en mémoire
- **Persistance** : ❌ Non (données perdues au redémarrage)
- **Solution** : Utiliser Supabase ou PostgreSQL

### Production avec Supabase (recommandé)
- **Type** : PostgreSQL distant
- **Persistance** : ✅ Oui
- **Configuration** : Variables `SUPABASE_URL` et `SUPABASE_KEY`

## 🔐 Sécurité

### Fichiers sensibles (gitignored)
- `.env` - Variables locales
- `instance/*.db` - Base de données locale
- `__pycache__/` - Cache Python
- `.vercel/` - Cache Vercel

### Variables sécurisées (Render)
- `SECRET_KEY` - Clé de session Flask
- `ADMIN_PASSWORD` - Mot de passe admin
- `MAIL_PASSWORD` - Mot de passe email
- `SUPABASE_KEY` - Clé API Supabase

## 🚀 Commandes utiles

### Développement
```bash
# Créer environnement virtuel
python -m venv venv
venv\Scripts\activate  # Windows

# Installer dépendances
pip install -r requirements.txt

# Lancer l'app
python main.py
```

### Déploiement
```bash
# Déploiement automatique Render
deploy_render.bat

# Ou manuellement
git add .
git commit -m "Update"
git push
```

### Maintenance
```bash
# Optimiser les images
python optimize_images.py

# Générer SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
```

## 📖 Documentation

### Guides de déploiement
1. **QUICKSTART_RENDER.md** - Démarrage rapide (5 min)
2. **DEPLOY_RENDER.md** - Guide complet et détaillé
3. **RENDER_CHECKLIST.md** - Checklist étape par étape

### Guides techniques
- **VERCEL_VS_RENDER.md** - Comparaison des plateformes
- **SUPABASE_SETUP.md** - Configuration base de données
- **MIGRATION_GUIDE.md** - Migration de données

### Guides de configuration
- **GUIDE_DOMAINE_OVH.md** - Domaine personnalisé
- **FAVICON_GUIDE.md** - Configuration favicon
- **OPTIMISATION_GUIDE.md** - Optimisations performance

## 🎓 Prochaines étapes

1. ✅ Configuration Render complète
2. 📤 Pousser le code sur Git
3. 🌐 Déployer sur Render
4. 🔧 Configurer les variables d'environnement
5. 🧪 Tester l'application en ligne
6. 🎯 (Optionnel) Ajouter un domaine personnalisé

---

**Votre projet est maintenant prêt pour Render !** 🎉
