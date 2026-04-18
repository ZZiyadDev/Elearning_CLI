from authentification import login, register
from enseignant import menu_enseignant
from etudiant import menu_etudiant

def main():
    while True:
        print("\n=== Application E-Learning ===")
        print("1. Se connecter")
        print("2. S'inscrire")
        print("3. Quitter")
        
        choix = input("Votre choix : ")
        
        if choix == '1':
            user = login()
            if user:
                if user['role'] == 'enseignant':
                    menu_enseignant(user)
                elif user['role'] == 'etudiant':
                    menu_etudiant(user)
                else:
                    print(f"Rôle non reconnu: {user['role']}")
        elif choix == '2':
            register()
        elif choix == '3':
            print("Au revoir !")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()
