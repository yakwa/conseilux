# Guide de connexion domaine OVH → Vercel

## Domaine : conseiluxtraining.com

### ÉTAPE 1 : Configuration Vercel

1. Allez sur : https://vercel.com/dashboard
2. Cliquez sur votre projet "Conseilux"
3. Dans le menu latéral : Settings → Domains
4. Cliquez sur "Add Domain"
5. Tapez : `conseiluxtraining.com` → Add
6. Tapez : `www.conseiluxtraining.com` → Add

### ÉTAPE 2 : Configuration DNS OVH

1. Allez sur : https://www.ovh.com/manager/
2. Connectez-vous avec :
   - Email : agbazahoughislain@gmail.com
   - Mot de passe : Agbanlin1994

3. Menu : Web Cloud → Noms de domaine
4. Cliquez sur : conseiluxtraining.com
5. Onglet : Zone DNS

### ÉTAPE 3 : Modifier les enregistrements DNS

**SUPPRIMER** tous les anciens enregistrements A et CNAME

**AJOUTER** ces 2 enregistrements :

#### Enregistrement 1 (Domaine principal)
- Type : A
- Sous-domaine : @ (ou laissez vide)
- Cible : 76.76.19.61
- TTL : 3600

#### Enregistrement 2 (Sous-domaine www)
- Type : CNAME
- Sous-domaine : www
- Cible : cname.vercel-dns.com
- TTL : 3600

### ÉTAPE 4 : Validation

1. Retournez dans Vercel → Settings → Domains
2. Cliquez sur "Verify" à côté de chaque domaine
3. Attendez 10-30 minutes

### RÉSULTAT ATTENDU

- conseiluxtraining.com → Votre site Conseilux
- www.conseiluxtraining.com → Votre site Conseilux

---

## Aide supplémentaire

Si vous rencontrez des difficultés :
1. Faites une capture d'écran de l'étape problématique
2. Contactez-moi avec l'erreur exacte
3. Je peux vous guider étape par étape

## Vérification finale

Une fois terminé, testez :
- http://conseiluxtraining.com
- https://conseiluxtraining.com
- https://www.conseiluxtraining.com
