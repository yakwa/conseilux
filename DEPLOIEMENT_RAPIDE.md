# 🚀 Déploiement Rapide - 5 Minutes !

## Étape 1 : GitHub (2 minutes)

### A. Créer le repository
1. Allez sur **github.com**
2. Cliquez sur **"New"** (bouton vert en haut)
3. Nom : **conseilux**
4. Cliquez sur **"Create repository"**

### B. Pousser le code
Ouvrez PowerShell dans le dossier Conseilux :

```powershell
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/conseilux.git
git push -u origin main
```

✅ **Votre code est maintenant sur GitHub !**

---

## Étape 2 : Render.com (3 minutes)

### A. Créer un compte
1. Allez sur **render.com**
2. Cliquez sur **"Get Started"**
3. Connectez-vous avec **GitHub**

### B. Déployer
1. Cliquez sur **"New +"** → **"Web Service"**
2. Sélectionnez votre repository **conseilux**
3. Remplissez :
   - **Name** : `conseilux`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn main:app`
4. Cliquez sur **"Advanced"** → **"Add Environment Variable"**
5. Ajoutez :
   ```
   SUPABASE_URL = votre_url_supabase
   SUPABASE_KEY = votre_cle_supabase
   SECRET_KEY = une_cle_secrete_aleatoire
   ```
6. Cliquez sur **"Create Web Service"**

### C. Attendez
- Le déploiement prend 5-10 minutes
- Vous verrez les logs en temps réel
- Une fois terminé, votre site sera à : **https://conseilux.onrender.com**

✅ **Votre site est en ligne !**

---

## 🎯 C'est Tout !

Votre site Conseilux est maintenant accessible sur Internet ! 🎉

### Prochaines étapes (optionnel) :
- [ ] Acheter un nom de domaine (ex: conseilux.com)
- [ ] Configurer le domaine personnalisé sur Render
- [ ] Activer les sauvegardes automatiques
- [ ] Configurer les emails de notification

---

## 🔄 Pour Mettre à Jour

Quand vous modifiez le code :

```powershell
git add .
git commit -m "Description des modifications"
git push
```

Render détectera automatiquement les changements et redéploiera ! 🚀

---

## 📞 Besoin d'Aide ?

Consultez le fichier **GUIDE_GITHUB.md** pour plus de détails.
