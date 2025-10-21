# 🚀 Guide de Migration vers Supabase - Conseilux

## Vue d'ensemble

Ce guide vous accompagne dans la migration complète de votre base de données SQLite vers Supabase pour le projet Conseilux.

## 📋 Tables migrées

1. **abonne_newsletter** - Gestion des abonnés à la newsletter
2. **avis_clients** - Gestion des avis clients

---

## 🔧 Étape 1 : Configuration Supabase

### 1.1 Créer un projet Supabase

1. Allez sur [supabase.com](https://supabase.com)
2. Connectez-vous ou créez un compte
3. Cliquez sur "New Project"
4. Remplissez les informations :
   - **Name** : Conseilux
   - **Database Password** : Choisissez un mot de passe fort
   - **Region** : Choisissez la région la plus proche de vos utilisateurs
5. Cliquez sur "Create new project"

### 1.2 Récupérer vos credentials

Une fois le projet créé :
1. Allez dans **Settings** > **API**
2. Notez :
   - **Project URL** (ex: `https://xxxxx.supabase.co`)
   - **anon/public key** (clé API publique)

### 1.3 Configurer les variables d'environnement

Vos credentials sont déjà configurés dans le fichier `.env` :
```env
SUPABASE_URL=https://hqixefsccyfsutvdludm.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

✅ **Cette étape est déjà faite !**

---

## 🗄️ Étape 2 : Créer les tables dans Supabase

### 2.1 Ouvrir l'éditeur SQL

1. Dans votre projet Supabase, cliquez sur **SQL Editor** dans le menu de gauche
2. Cliquez sur **New Query**

### 2.2 Exécuter le script de migration

Copiez et collez le contenu du fichier `supabase_migration.sql` dans l'éditeur SQL, puis cliquez sur **RUN**.

Ou copiez directement ce script :

```sql
-- ============================================
-- TABLE 1: ABONNÉS NEWSLETTER
-- ============================================

CREATE TABLE IF NOT EXISTS abonne_newsletter (
  id BIGSERIAL PRIMARY KEY,
  email VARCHAR(120) UNIQUE NOT NULL,
  date_inscription TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_newsletter_email ON abonne_newsletter(email);
CREATE INDEX IF NOT EXISTS idx_newsletter_date ON abonne_newsletter(date_inscription DESC);

ALTER TABLE abonne_newsletter ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Permettre inscription newsletter"
ON abonne_newsletter FOR INSERT WITH CHECK (true);

CREATE POLICY "Permettre lecture newsletter admin"
ON abonne_newsletter FOR SELECT
USING (auth.role() = 'authenticated');

CREATE POLICY "Permettre suppression newsletter admin"
ON abonne_newsletter FOR DELETE
USING (auth.role() = 'authenticated');

-- ============================================
-- TABLE 2: AVIS CLIENTS
-- ============================================

CREATE TABLE IF NOT EXISTS avis_clients (
  id BIGSERIAL PRIMARY KEY,
  nom_complet VARCHAR(100) NOT NULL,
  avis TEXT NOT NULL,
  note INTEGER NOT NULL DEFAULT 5 CHECK (note >= 1 AND note <= 5),
  date_creation TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  approuve BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_avis_date_creation ON avis_clients(date_creation DESC);
CREATE INDEX IF NOT EXISTS idx_avis_approuve ON avis_clients(approuve);

ALTER TABLE avis_clients ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Permettre lecture avis approuvés"
ON avis_clients FOR SELECT USING (approuve = true);

CREATE POLICY "Permettre insertion avis"
ON avis_clients FOR INSERT WITH CHECK (true);

CREATE POLICY "Permettre mise à jour avis admin"
ON avis_clients FOR UPDATE
USING (auth.role() = 'authenticated');

CREATE POLICY "Permettre suppression avis admin"
ON avis_clients FOR DELETE
USING (auth.role() = 'authenticated');
```

### 2.3 Vérifier la création des tables

1. Allez dans **Table Editor** dans le menu de gauche
2. Vous devriez voir les deux tables :
   - `abonne_newsletter`
   - `avis_clients`

---

## 🔄 Étape 3 : Migrer les données existantes (Optionnel)

Si vous avez déjà des données dans SQLite que vous souhaitez migrer :

### 3.1 Exporter depuis SQLite

```python
# Script Python pour exporter les données
import sqlite3
import json

# Connexion à la base SQLite
conn = sqlite3.connect('instance/newsletter.db')
cursor = conn.cursor()

# Exporter les abonnés newsletter
cursor.execute("SELECT email, date_inscription FROM abonne_newsletter")
newsletters = cursor.fetchall()
with open('export_newsletter.json', 'w') as f:
    json.dump([{'email': n[0], 'date_inscription': n[1]} for n in newsletters], f)

# Exporter les avis
cursor.execute("SELECT nom_complet, avis, note, date_creation, approuve FROM avis_client")
avis = cursor.fetchall()
with open('export_avis.json', 'w') as f:
    json.dump([{
        'nom_complet': a[0],
        'avis': a[1],
        'note': a[2],
        'date_creation': a[3],
        'approuve': a[4]
    } for a in avis], f)

conn.close()
print("Export terminé !")
```

### 3.2 Importer dans Supabase

Vous pouvez utiliser l'interface Supabase pour importer les données :
1. Allez dans **Table Editor**
2. Sélectionnez la table
3. Cliquez sur **Insert** > **Import data from CSV**

Ou utilisez l'API Python directement (le code est déjà intégré dans l'application).

---

## ✅ Étape 4 : Tester la migration

### 4.1 Redémarrer le serveur

```bash
python -m flask --app main run --debug
```

### 4.2 Vérifier la connexion

Dans la console, vous devriez voir :
```
✓ Supabase connecté avec succès
```

### 4.3 Tester les fonctionnalités

1. **Newsletter** : Essayez de vous abonner via le formulaire sur la page d'accueil
2. **Avis clients** : Soumettez un avis via la page Contact
3. **Admin** : Connectez-vous à l'admin pour voir les abonnés

---

## 🔍 Vérification dans Supabase

### Voir les données en temps réel

1. Allez dans **Table Editor**
2. Sélectionnez une table
3. Vous verrez toutes les données insérées

### Voir les logs

1. Allez dans **Logs** > **API Logs**
2. Vous verrez toutes les requêtes effectuées

---

## 🎯 Fonctionnalités

### Mode Hybride

L'application fonctionne en mode hybride :
- ✅ **Avec Supabase configuré** : Toutes les données sont stockées dans Supabase
- ✅ **Sans Supabase** : L'application utilise SQLite en fallback

### Sécurité (RLS)

Les politiques Row Level Security sont configurées :
- **Public** : Peut lire les avis approuvés et s'inscrire à la newsletter
- **Authentifié** : Peut gérer tous les avis et abonnés (admin)

---

## 📊 Structure des tables

### Table: abonne_newsletter

| Colonne          | Type         | Description                        |
|------------------|--------------|------------------------------------|
| id               | BIGSERIAL    | ID unique (auto-incrémenté)       |
| email            | VARCHAR(120) | Email de l'abonné (unique)        |
| date_inscription | TIMESTAMPTZ  | Date d'inscription (automatique)  |

### Table: avis_clients

| Colonne        | Type         | Description                           |
|----------------|--------------|---------------------------------------|
| id             | BIGSERIAL    | ID unique (auto-incrémenté)          |
| nom_complet    | VARCHAR(100) | Nom complet de la personne           |
| avis           | TEXT         | Contenu de l'avis                    |
| note           | INTEGER      | Note de 1 à 5                        |
| date_creation  | TIMESTAMPTZ  | Date de création (automatique)       |
| approuve       | BOOLEAN      | Si l'avis est approuvé (défaut: true)|

---

## 🚨 Dépannage

### Erreur "Invalid API key"

- Vérifiez que les credentials dans `.env` sont corrects
- Vérifiez que les tables existent dans Supabase

### Erreur "relation does not exist"

- Les tables n'ont pas été créées dans Supabase
- Exécutez le script SQL de migration

### Les données n'apparaissent pas

- Vérifiez les politiques RLS dans Supabase
- Vérifiez que `approuve = true` pour les avis

---

## 📝 Notes importantes

1. **Backup** : Gardez une copie de votre base SQLite avant la migration
2. **Test** : Testez en environnement de développement avant la production
3. **Monitoring** : Surveillez les logs Supabase après la migration

---

## ✨ Avantages de Supabase

- ✅ Base de données PostgreSQL scalable
- ✅ API REST automatique
- ✅ Sécurité avec Row Level Security
- ✅ Interface d'administration
- ✅ Backups automatiques
- ✅ Temps réel (optionnel)

---

## 🎉 Migration terminée !

Votre application Conseilux utilise maintenant Supabase pour stocker toutes les données !
