import os
import sys
import django

def setup():
    print("--- Configuration de la plateforme E-Learning ---")
    
    # 1. Installation des dépendances Python
    print("\n[1/4] Vérification des dépendances...")
    os.system(f"{sys.executable} -m pip install -r requirements.txt")

    # 2. Migrations de la base de données
    print("\n[2/4] Configuration de la base de données...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning_project.settings')
    django.setup()
    
    from django.core.management import call_command
    call_command('makemigrations', 'core')
    call_command('migrate')

    # 3. Création d'un compte administrateur par défaut
    print("\n[3/4] Création du compte administrateur...")
    from core.models import Utilisateur
    if not Utilisateur.objects.filter(username='admin').exists():
        Utilisateur.objects.create_superuser(
            username='admin',
            email='admin@emsi.ma',
            password='adminpassword',
            nom='Administrateur Système',
            role='admin'
        )
        print(">> Compte créé : admin / adminpassword")
    else:
        print(">> Le compte admin existe déjà.")

    # 4. Finalisation
    print("\n[4/4] Installation terminée !")
    print("\nPour lancer le serveur :")
    print("python manage.py runserver")
    print("\nPour compiler le CSS (Tailwind) :")
    print("npm install")
    print("npm run build")

if __name__ == "__main__":
    setup()
