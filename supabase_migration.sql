-- ============================================
-- MIGRATION COMPLÈTE VERS SUPABASE
-- Projet: Conseilux
-- ============================================

-- ============================================
-- TABLE 1: ABONNÉS NEWSLETTER
-- ============================================

-- Créer la table abonne_newsletter
CREATE TABLE IF NOT EXISTS abonne_newsletter (
  id BIGSERIAL PRIMARY KEY,
  email VARCHAR(120) UNIQUE NOT NULL,
  date_inscription TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Créer un index sur l'email pour améliorer les performances
CREATE INDEX IF NOT EXISTS idx_newsletter_email ON abonne_newsletter(email);

-- Créer un index sur la date d'inscription
CREATE INDEX IF NOT EXISTS idx_newsletter_date ON abonne_newsletter(date_inscription DESC);

-- Activer Row Level Security (RLS)
ALTER TABLE abonne_newsletter ENABLE ROW LEVEL SECURITY;

-- Politique pour permettre l'insertion d'abonnés (public)
CREATE POLICY "Permettre inscription newsletter"
ON abonne_newsletter
FOR INSERT
WITH CHECK (true);

-- Politique pour permettre la lecture (authentifié uniquement - admin)
CREATE POLICY "Permettre lecture newsletter admin"
ON abonne_newsletter
FOR SELECT
USING (auth.role() = 'authenticated');

-- Politique pour permettre la suppression (authentifié uniquement - admin)
CREATE POLICY "Permettre suppression newsletter admin"
ON abonne_newsletter
FOR DELETE
USING (auth.role() = 'authenticated');


-- ============================================
-- TABLE 2: AVIS CLIENTS
-- ============================================

-- Créer la table avis_clients
CREATE TABLE IF NOT EXISTS avis_clients (
  id BIGSERIAL PRIMARY KEY,
  nom_complet VARCHAR(100) NOT NULL,
  avis TEXT NOT NULL,
  note INTEGER NOT NULL DEFAULT 5 CHECK (note >= 1 AND note <= 5),
  date_creation TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  approuve BOOLEAN NOT NULL DEFAULT TRUE
);

-- Créer un index sur date_creation pour améliorer les performances
CREATE INDEX IF NOT EXISTS idx_avis_date_creation ON avis_clients(date_creation DESC);

-- Créer un index sur approuve pour filtrer rapidement
CREATE INDEX IF NOT EXISTS idx_avis_approuve ON avis_clients(approuve);

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

-- Politique pour permettre la mise à jour (authentifié uniquement - admin)
CREATE POLICY "Permettre mise à jour avis admin"
ON avis_clients
FOR UPDATE
USING (auth.role() = 'authenticated');

-- Politique pour permettre la suppression (authentifié uniquement - admin)
CREATE POLICY "Permettre suppression avis admin"
ON avis_clients
FOR DELETE
USING (auth.role() = 'authenticated');


-- ============================================
-- VUES UTILES (OPTIONNEL)
-- ============================================

-- Vue pour compter les abonnés par mois
CREATE OR REPLACE VIEW stats_newsletter_par_mois AS
SELECT 
  DATE_TRUNC('month', date_inscription) as mois,
  COUNT(*) as nombre_abonnes
FROM abonne_newsletter
GROUP BY DATE_TRUNC('month', date_inscription)
ORDER BY mois DESC;

-- Vue pour les statistiques des avis
CREATE OR REPLACE VIEW stats_avis AS
SELECT 
  COUNT(*) as total_avis,
  AVG(note) as note_moyenne,
  COUNT(CASE WHEN approuve = true THEN 1 END) as avis_approuves,
  COUNT(CASE WHEN approuve = false THEN 1 END) as avis_en_attente
FROM avis_clients;

-- ============================================
-- FONCTIONS UTILES (OPTIONNEL)
-- ============================================

-- Fonction pour vérifier si un email existe déjà
CREATE OR REPLACE FUNCTION email_existe(email_check VARCHAR)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS(SELECT 1 FROM abonne_newsletter WHERE email = email_check);
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- FIN DU SCRIPT DE MIGRATION
-- ============================================
