# 🔐 Connexion à Vercel - Guide Simple

## 🚨 Problème actuel
La commande `vercel login` attend que vous vous connectiez dans le navigateur.

---

## ✅ Solution en 3 étapes

### **Étape 1 : Ouvrir le lien de connexion**

Ouvrez votre navigateur et allez sur :
```
https://vercel.com/oauth/device?user_code=RCWH-TKMH
```

**OU** créez d'abord un compte sur :
```
https://vercel.com/signup
```

---

### **Étape 2 : Se connecter**

Sur la page Vercel, choisissez une méthode :

1. **GitHub** (recommandé si vous avez un compte)
2. **GitLab**
3. **Bitbucket**
4. **Email** (créer un nouveau compte)

Cliquez sur le bouton et suivez les instructions.

---

### **Étape 3 : Autoriser l'accès**

Une fois connecté, autorisez l'accès à Vercel CLI.

---

## 🔄 Si ça ne marche toujours pas

### **Méthode alternative : Utiliser un token**

1. **Créer un token** :
   - Allez sur https://vercel.com/account/tokens
   - Cliquez sur "Create Token"
   - Nommez-le : `conseilux-deploy`
   - Copiez le token

2. **Utiliser le token** :
   ```bash
   # Windows PowerShell
   $env:VERCEL_TOKEN="votre_token_ici"
   vercel --token $env:VERCEL_TOKEN
   ```

---

## 📞 Besoin d'aide ?

Si vous n'arrivez toujours pas à vous connecter, dites-moi :
1. Avez-vous déjà un compte Vercel ? (Oui/Non)
2. Quel message d'erreur voyez-vous ?
3. Le navigateur s'ouvre-t-il automatiquement ?

Je vous aiderai à résoudre le problème spécifique !
