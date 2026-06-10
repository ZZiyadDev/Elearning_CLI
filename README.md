# Plateforme E-Learning EMSI (Web)

Une plateforme moderne d'apprentissage en ligne développée avec **Django** et **Tailwind CSS**. Ce projet est l'évolution de l'application CLI initiale vers une architecture web complète.

## 🚀 Installation Rapide

Pour configurer automatiquement le projet (base de données, migrations, compte admin) :

1. Assurez-vous d'avoir Python installé.
2. Ouvrez un terminal dans le dossier du projet.
3. Exécutez le script de configuration :
   ```bash
   python setup_project.py
   ```

## 🛠️ Configuration Manuelle

Si vous préférez configurer étape par étape :

### 1. Environnement Python
```bash
pip install -r requirements.txt
python manage.py makemigrations core
python manage.py migrate
```

### 2. Frontend (Tailwind CSS)
Le projet utilise Node.js pour compiler le CSS.
```bash
npm install
npm run build
```

### 3. Lancement
```bash
python manage.py runserver
```

## 👥 Comptes de Test

Le script `setup_project.py` crée un compte administrateur par défaut :
- **Username :** `admin`
- **Password :** `adminpassword`

## 🏗️ Architecture (MVT)

- **Modèles :** Gérés dans `core/models.py` (Utilisateurs personnalisés, Cours, Leçons, Quiz, Progress).
- **Vues :** Logique métier dans `core/views.py`.
- **Templates :** Interfaces HTML dans `core/templates/core/`.
- **Styles :** Design moderne avec Tailwind CSS (thème rouge minimalist).

## 📄 Documentation

Le rapport technique complet se trouve dans le fichier `Elearning_CLI_Report.tex`.
