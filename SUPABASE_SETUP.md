# Configuration Supabase pour les Avis Clients

## 1. Créer un projet Supabase

1. Allez sur [supabase.com](https://supabase.com)
2. Créez un compte ou connectez-vous
3. Créez un nouveau projet
4. Notez votre **URL du projet** et votre **clé API publique (anon key)**

## 2. Créer la table `avis_clients`

Dans l'éditeur SQL de Supabase, exécutez cette requête :

```sql
-- Créer la table avis_clients
CREATE TABLE avis_clients (
  id BIGSERIAL PRIMARY KEY,
  nom_complet VARCHAR(100) NOT NULL,
  avis TEXT NOT NULL,
  note INTEGER NOT NULL DEFAULT 5 CHECK (note >= 1 AND note <= 5),
  date_creation TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  approuve BOOLEAN NOT NULL DEFAULT TRUE
);

-- Créer un index sur date_creation pour améliorer les performances
CREATE INDEX idx_avis_date_creation ON avis_clients(date_creation DESC);

-- Créer un index sur approuve pour filtrer rapidement
CREATE INDEX idx_avis_approuve ON avis_clients(approuve);

-- Activer Row Level Security (RLS)
ALTER TABLE avis_clients ENABLE ROW LEVEL SECURITY;

-- Politique pour permettre la lecture des avis approuvés (public)
CREATE POLICY "Permettre lecture avis approuvés"
ON avis_clients
FOR SELECT
USING (approuve = true);

-- Politique pour permettre l'insertion d'avis (public)
CREATE POLICY "Permettre insertion avis"
ON avis_clients
FOR INSERT
WITH CHECK (true);

-- Politique pour permettre la mise à jour (authentifié uniquement)
CREATE POLICY "Permettre mise à jour admin"
ON avis_clients
FOR UPDATE
USING (auth.role() = 'authenticated');
```

## 3. Configurer les variables d'environnement

Créez un fichier `.env` à la racine du projet avec :

```env
SUPABASE_URL=https://votre-projet-id.supabase.co
SUPABASE_KEY=votre-cle-anon-publique
```

## 4. Structure de la table

| Colonne         | Type          | Description                                    |
|-----------------|---------------|------------------------------------------------|
| id              | BIGSERIAL     | Identifiant unique (auto-incrémenté)          |
| nom_complet     | VARCHAR(100)  | Nom complet de la personne                     |
| avis            | TEXT          | Contenu de l'avis                              |
| note            | INTEGER       | Note de 1 à 5                                  |
| date_creation   | TIMESTAMPTZ   | Date et heure de création (automatique)        |
| approuve        | BOOLEAN       | Si l'avis est approuvé pour affichage (défaut: true) |

## 5. Fonctionnement

- **Lecture des avis** : L'application récupère automatiquement les avis approuvés depuis Supabase
- **Création d'avis** : Les nouveaux avis sont directement enregistrés dans Supabase
- **Fallback** : Si Supabase n'est pas configuré, l'application utilise SQLite en local

## 6. Tester la connexion

Après avoir configuré les variables d'environnement, redémarrez le serveur Flask.
Vous devriez voir dans la console :
```
✓ Supabase connecté avec succès
```

Si les variables ne sont pas configurées :
```
⚠ Variables Supabase non configurées - les avis utiliseront SQLite
```
