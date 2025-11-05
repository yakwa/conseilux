# 🔧 Commandes Git pour Déploiement Render

## 🚀 Déploiement rapide (3 commandes)

```bash
git add .
git commit -m "Configuration Render complète"
git push
```

**C'est tout !** Render redéploiera automatiquement votre site.

---

## 📋 Guide complet Git

### 1️⃣ Première configuration (une seule fois)

#### Configurer votre identité Git
```bash
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"
```

#### Initialiser le dépôt (si pas déjà fait)
```bash
git init
```

#### Ajouter un dépôt distant (GitHub/GitLab)
```bash
# GitHub
git remote add origin https://github.com/votre-username/conseilux.git

# GitLab
git remote add origin https://gitlab.com/votre-username/conseilux.git

# Bitbucket
git remote add origin https://bitbucket.org/votre-username/conseilux.git
```

#### Vérifier le dépôt distant
```bash
git remote -v
```

### 2️⃣ Workflow quotidien

#### Voir les fichiers modifiés
```bash
git status
```

#### Ajouter tous les fichiers modifiés
```bash
git add .
```

#### Ajouter des fichiers spécifiques
```bash
git add main.py
git add templates/index.html
git add static/css/style.css
```

#### Créer un commit
```bash
git commit -m "Description de vos modifications"
```

**Exemples de messages de commit :**
```bash
git commit -m "Ajout du formulaire de contact"
git commit -m "Correction bug newsletter"
git commit -m "Mise à jour du design"
git commit -m "Configuration Render"
```

#### Pousser vers le dépôt distant
```bash
# Première fois
git push -u origin main

# Ensuite
git push
```

### 3️⃣ Commandes utiles

#### Voir l'historique des commits
```bash
git log
git log --oneline  # Version condensée
```

#### Voir les différences
```bash
git diff  # Changements non stagés
git diff --staged  # Changements stagés
```

#### Annuler des modifications

**Annuler les modifications d'un fichier (avant add)**
```bash
git checkout -- main.py
```

**Retirer un fichier du staging (après add)**
```bash
git reset HEAD main.py
```

**Annuler le dernier commit (garder les modifications)**
```bash
git reset --soft HEAD~1
```

#### Créer une branche
```bash
git branch nouvelle-fonctionnalite
git checkout nouvelle-fonctionnalite

# Ou en une commande
git checkout -b nouvelle-fonctionnalite
```

#### Fusionner une branche
```bash
git checkout main
git merge nouvelle-fonctionnalite
```

#### Mettre à jour depuis le dépôt distant
```bash
git pull
```

### 4️⃣ Résolution de problèmes

#### Problème : "fatal: not a git repository"
**Solution :**
```bash
git init
git remote add origin https://github.com/votre-username/conseilux.git
```

#### Problème : "Updates were rejected"
**Solution :**
```bash
git pull --rebase
git push
```

#### Problème : Conflit de fusion
**Solution :**
1. Ouvrez les fichiers en conflit
2. Résolvez les conflits manuellement
3. Ajoutez les fichiers résolus :
```bash
git add fichier-resolu.py
git commit -m "Résolution des conflits"
git push
```

#### Problème : Mot de passe demandé à chaque push
**Solution (Windows) :**
```bash
git config --global credential.helper wincred
```

**Solution (Linux/Mac) :**
```bash
git config --global credential.helper cache
```

#### Problème : Fichier trop volumineux
**Solution :**
```bash
# Retirer le fichier du commit
git rm --cached fichier-volumineux.zip

# Ajouter au .gitignore
echo "fichier-volumineux.zip" >> .gitignore

# Commit
git commit -m "Retrait fichier volumineux"
git push
```

### 5️⃣ Workflow avec Render

#### Déploiement standard
```bash
# 1. Modifier le code
# 2. Tester localement
python main.py

# 3. Commit et push
git add .
git commit -m "Nouvelle fonctionnalité"
git push

# 4. Render redéploie automatiquement !
```

#### Déploiement avec vérification
```bash
# Voir ce qui va être commité
git status
git diff

# Ajouter sélectivement
git add main.py templates/

# Commit avec message descriptif
git commit -m "Amélioration du formulaire de contact"

# Push
git push

# Surveiller le déploiement sur dashboard.render.com
```

### 6️⃣ Branches pour développement

#### Créer une branche de développement
```bash
git checkout -b dev
```

#### Travailler sur la branche dev
```bash
git add .
git commit -m "Travail en cours"
git push -u origin dev
```

#### Fusionner dev dans main (après tests)
```bash
git checkout main
git merge dev
git push
```

### 7️⃣ Tags pour versions

#### Créer un tag
```bash
git tag -a v1.0.0 -m "Version 1.0.0 - Lancement"
git push origin v1.0.0
```

#### Lister les tags
```bash
git tag
```

### 8️⃣ Nettoyage

#### Supprimer les fichiers non suivis
```bash
git clean -n  # Voir ce qui sera supprimé
git clean -f  # Supprimer
```

#### Supprimer une branche
```bash
git branch -d nom-branche  # Locale
git push origin --delete nom-branche  # Distante
```

---

## 🎯 Commandes essentielles (mémo rapide)

```bash
# Configuration initiale
git config --global user.name "Votre Nom"
git config --global user.email "votre@email.com"
git remote add origin https://github.com/username/repo.git

# Workflow quotidien
git status                    # Voir les modifications
git add .                     # Ajouter tous les fichiers
git commit -m "Message"       # Créer un commit
git push                      # Envoyer vers GitHub/GitLab

# Mise à jour
git pull                      # Récupérer les changements

# Branches
git checkout -b nouvelle      # Créer et basculer
git checkout main             # Revenir à main
git merge nouvelle            # Fusionner

# Annulation
git checkout -- fichier       # Annuler modifications
git reset HEAD fichier        # Retirer du staging
git reset --soft HEAD~1       # Annuler dernier commit
```

---

## 🔗 Ressources

- [Documentation Git officielle](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [GitLab Documentation](https://docs.gitlab.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---

## 💡 Conseils

1. **Commitez souvent** avec des messages clairs
2. **Testez localement** avant de pusher
3. **Utilisez des branches** pour les nouvelles fonctionnalités
4. **Vérifiez le .gitignore** pour ne pas commiter de secrets
5. **Surveillez Render** après chaque push

---

**Avec ces commandes, vous êtes prêt à déployer sur Render !** 🚀
