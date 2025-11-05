# 🔧 Dépannage Render - Solutions aux problèmes courants

## ✅ Problème résolu : Erreur Python 3.13

### Symptôme
```
KeyError: '__version__'
Getting requirements to build wheel did not run successfully.
```

### Cause
Render utilisait Python 3.13 par défaut, qui n'est pas encore compatible avec certaines dépendances (notamment Pillow et supabase).

### Solution appliquée ✅
1. Création du fichier `.python-version` avec `3.11.9`
2. Mise à jour de `runtime.txt` vers `python-3.11.9`
3. Mise à jour de `render.yaml` avec `PYTHON_VERSION: 3.11.9`
4. Mise à jour des dépendances :
   - `gunicorn==22.0.0` (au lieu de 21.2.0)
   - `Pillow==10.4.0` (au lieu de 10.2.0)

### Vérification
Render devrait maintenant utiliser Python 3.11.9 et le build devrait réussir.

---

## 🚨 Autres problèmes courants

### 1. Service s'endort après 15 minutes (Plan gratuit)

**Symptôme :** Le site est lent au premier chargement après une période d'inactivité.

**Cause :** Le plan gratuit de Render met le service en veille après 15 minutes d'inactivité.

**Solutions :**
- **Option A (Gratuit)** : Accepter le délai de 30-50 secondes au premier chargement
- **Option B (Gratuit)** : Utiliser un service de ping comme [UptimeRobot](https://uptimerobot.com) ou [cron-job.org](https://cron-job.org)
- **Option C (Payant)** : Passer au plan Starter ($7/mois) pour un service toujours actif

### 2. Erreur "Application failed to respond"

**Symptôme :** Le service démarre mais ne répond pas aux requêtes.

**Causes possibles :**
- Port incorrect
- Gunicorn ne démarre pas correctement
- Variables d'environnement manquantes

**Solutions :**
```bash
# Vérifier que le startCommand est correct
startCommand: gunicorn main:app

# Vérifier que main.py contient bien 'app'
# Dans main.py, vous devez avoir :
app = Flask(__name__)

# Vérifier les logs dans le dashboard Render
```

### 3. Erreur d'envoi d'emails

**Symptôme :** Les formulaires ne fonctionnent pas, erreurs SMTP.

**Causes possibles :**
- Mot de passe Gmail incorrect
- Pas de mot de passe d'application Gmail
- Variables d'environnement mal configurées

**Solutions :**
1. **Créer un mot de passe d'application Gmail :**
   - Allez sur [myaccount.google.com](https://myaccount.google.com)
   - Sécurité → Validation en deux étapes (activez-la)
   - Mots de passe des applications → Créez un nouveau mot de passe
   - Utilisez ce mot de passe dans `MAIL_PASSWORD`

2. **Vérifier les variables d'environnement dans Render :**
   ```
   MAIL_USERNAME=votre-email@gmail.com
   MAIL_PASSWORD=<mot de passe d'application, pas votre mot de passe normal>
   MAIL_DEFAULT_SENDER=contact@conseilux-training.com
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   ```

### 4. Base de données vide après redémarrage

**Symptôme :** Les abonnés newsletter disparaissent après un redémarrage.

**Cause :** SQLite en mémoire (par défaut) ne persiste pas les données.

**Solutions :**

#### Option A : Utiliser Supabase (Recommandé - Gratuit)
1. Créez un compte sur [supabase.com](https://supabase.com)
2. Créez un nouveau projet
3. Ajoutez les variables dans Render :
   ```
   SUPABASE_URL=https://votre-projet.supabase.co
   SUPABASE_KEY=votre-cle-anon-publique
   ```

#### Option B : PostgreSQL sur Render
1. Dans Render : **New +** → **PostgreSQL**
2. Créez une base de données
3. Ajoutez à `requirements.txt` :
   ```
   psycopg2-binary==2.9.9
   ```
4. Modifiez `main.py` pour utiliser `DATABASE_URL`

### 5. Erreur "Build failed" - Dépendances manquantes

**Symptôme :** Le build échoue lors de l'installation des dépendances.

**Solutions :**
1. Vérifiez que `requirements.txt` est à la racine du projet
2. Vérifiez que toutes les versions sont compatibles avec Python 3.11.9
3. Essayez de mettre à jour les versions :
   ```
   pip install --upgrade pip
   pip freeze > requirements.txt
   ```

### 6. Erreur 404 sur les fichiers statiques

**Symptôme :** Les CSS, JS ou images ne se chargent pas.

**Causes possibles :**
- Chemins incorrects dans les templates
- Dossier `static/` mal configuré

**Solutions :**
1. Vérifiez que le dossier `static/` existe à la racine
2. Dans les templates, utilisez :
   ```html
   <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
   <img src="{{ url_for('static', filename='images/logo.png') }}">
   ```

### 7. Variables d'environnement non reconnues

**Symptôme :** L'application ne trouve pas les variables d'environnement.

**Solutions :**
1. Vérifiez dans Render : **Environment** → **Environment Variables**
2. Assurez-vous qu'il n'y a pas d'espaces avant/après les valeurs
3. Redéployez après avoir ajouté/modifié des variables
4. Les variables sont sensibles à la casse

### 8. Erreur "SECRET_KEY must be set"

**Symptôme :** L'application refuse de démarrer sans SECRET_KEY.

**Solutions :**
1. Dans Render, ajoutez la variable `SECRET_KEY`
2. Générez une clé sécurisée :
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
3. Ou laissez Render la générer automatiquement (déjà configuré dans `render.yaml`)

### 9. Timeout lors du déploiement

**Symptôme :** Le build prend trop de temps et échoue.

**Causes possibles :**
- Trop de dépendances
- Installation de packages lourds (comme Pillow)

**Solutions :**
1. Optimisez `requirements.txt` (retirez les dépendances inutiles)
2. Utilisez des versions pré-compilées quand possible
3. Le plan gratuit a des limites de temps de build

### 10. Erreur "Port already in use"

**Symptôme :** Le service ne démarre pas, port occupé.

**Cause :** Render gère automatiquement le port via la variable `PORT`.

**Solution :**
Assurez-vous que `main.py` utilise le port fourni par Render :
```python
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

---

## 📊 Vérifier les logs

Pour diagnostiquer les problèmes :

1. **Dashboard Render** → Votre service → **Logs**
2. Les logs montrent :
   - Les erreurs de build
   - Les erreurs d'exécution
   - Les requêtes HTTP
   - Les erreurs Python

### Commandes utiles dans les logs
```bash
# Voir les dernières lignes
tail -f logs

# Rechercher une erreur spécifique
grep "ERROR" logs

# Voir les requêtes HTTP
grep "GET\|POST" logs
```

---

## 🔍 Checklist de dépannage

Avant de contacter le support :

- [ ] Vérifiez les logs dans le dashboard Render
- [ ] Vérifiez que toutes les variables d'environnement sont définies
- [ ] Vérifiez que le build se termine avec succès
- [ ] Vérifiez que Python 3.11.9 est utilisé (pas 3.13)
- [ ] Vérifiez que `requirements.txt` est à jour
- [ ] Testez localement avec les mêmes variables d'environnement
- [ ] Vérifiez que le dépôt GitHub est à jour

---

## 🆘 Obtenir de l'aide

### Documentation Render
- [Troubleshooting Deploys](https://render.com/docs/troubleshooting-deploys)
- [Python on Render](https://render.com/docs/deploy-flask)
- [Environment Variables](https://render.com/docs/environment-variables)

### Support Render
- [Community Forum](https://community.render.com/)
- [Support Tickets](https://render.com/support)
- Email : support@render.com

### Ressources du projet
- **QUICKSTART_RENDER.md** - Guide de démarrage
- **DEPLOY_RENDER.md** - Guide complet
- **RENDER_CHECKLIST.md** - Checklist de déploiement

---

## 📝 Historique des corrections

### 2025-11-05 : Correction Python 3.13
- ✅ Ajout de `.python-version` avec 3.11.9
- ✅ Mise à jour de `runtime.txt` vers 3.11.9
- ✅ Mise à jour de `render.yaml` avec Python 3.11.9
- ✅ Mise à jour de gunicorn vers 22.0.0
- ✅ Mise à jour de Pillow vers 10.4.0

---

**En cas de problème persistant, consultez les logs et n'hésitez pas à contacter le support Render.** 🚀
