from data import load_users, save_users, get_next_id

def menu_admin(user):
    """Admin menu with CRUD operations for users"""
    while True:
        print("\n===== MENU ADMINISTRATEUR =====")
        print("1. Ajouter un utilisateur")
        print("2. Supprimer un utilisateur")
        print("3. Modifier les informations d'un utilisateur")
        print("4. Consulter la liste des utilisateurs")
        print("5. Rechercher un utilisateur")
        print("6. Déconnexion")
        
        choix = input("Votre choix : ")
        
        if choix == '1':
            ajouter_utilisateur()
        elif choix == '2':
            supprimer_utilisateur()
        elif choix == '3':
            modifier_utilisateur()
        elif choix == '4':
            consulter_utilisateurs()
        elif choix == '5':
            rechercher_utilisateur()
        elif choix == '6':
            print("Déconnexion réussie. À bientôt !")
            break
        else:
            print("Choix invalide.")

def ajouter_utilisateur():
    """Add a new user"""
    print("\n--- Ajouter un utilisateur ---")
    
    nom = input("Nom complet : ")
    email = input("Email : ")
    username = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")
    
    users = load_users()
    
    # Check if username already exists
    if any(u['username'] == username for u in users):
        print("❌ Ce nom d'utilisateur est déjà pris.")
        return
    
    # Check if email already exists
    if any(u['email'] == email for u in users):
        print("❌ Cet email est déjà associé à un compte.")
        return
    
    print("\nChoisissez le rôle :") 
    print("1. Administrateur")
    print("2. Enseignant")
    print("3. Etudiant")
    
    choix = input("Votre choix (1, 2 ou 3) : ")
    
    if choix == '1':
        role = 'administrateur'
    elif choix == '2':
        role = 'enseignant'
    elif choix == '3':
        role = 'etudiant'
    else:
        print("❌ Choix invalide.")
        return
    
    new_user = {
        "id": get_next_id(users),
        "nom": nom,
        "email": email,
        "username": username,
        "password": password,
        "role": role
    }
    
    users.append(new_user)
    save_users(users)
    print(f"✅ Utilisateur '{nom}' ({role}) ajouté avec succès ! (ID: {new_user['id']})")

def supprimer_utilisateur():
    """Delete a user"""
    print("\n--- Supprimer un utilisateur ---")
    
    users = load_users()
    
    if not users:
        print("❌ Aucun utilisateur à supprimer.")
        return
    
    # Display users
    for idx, u in enumerate(users, 1):
        print(f"{idx}. {u['nom']} ({u['username']}) - ID: {u['id']} - Rôle: {u['role']}")
    
    try:
        choix = int(input("\nChoisissez le numéro de l'utilisateur à supprimer (0 pour annuler) : "))
        
        if choix == 0:
            return
        
        if 1 <= choix <= len(users):
            user_to_delete = users[choix - 1]
            
            # Confirmation
            confirmation = input(f"Confirmer la suppression de '{user_to_delete['nom']}' ? (o/n) : ")
            if confirmation.lower() == 'o':
                users.pop(choix - 1)
                save_users(users)
                print(f"✅ Utilisateur '{user_to_delete['nom']}' supprimé avec succès.")
            else:
                print("❌ Suppression annulée.")
        else:
            print("❌ Choix invalide.")
    except ValueError:
        print("❌ Veuillez entrer un nombre.")

def modifier_utilisateur():
    """Modify user information"""
    print("\n--- Modifier les informations d'un utilisateur ---")
    
    users = load_users()
    
    if not users:
        print("❌ Aucun utilisateur à modifier.")
        return
    
    # Display users
    for idx, u in enumerate(users, 1):
        print(f"{idx}. {u['nom']} ({u['username']}) - ID: {u['id']}")
    
    try:
        choix = int(input("\nChoisissez le numéro de l'utilisateur à modifier (0 pour annuler) : "))
        
        if choix == 0:
            return
        
        if 1 <= choix <= len(users):
            user_to_modify = users[choix - 1]
            
            print(f"\nModification de '{user_to_modify['nom']}'")
            print("Appuyez sur Entrée pour conserver la valeur actuelle.")
            
            # Modify name
            nouveau_nom = input(f"Nom complet (actuel: {user_to_modify['nom']}) : ")
            if nouveau_nom.strip():
                user_to_modify['nom'] = nouveau_nom
            
            # Modify email
            nouveau_email = input(f"Email (actuel: {user_to_modify['email']}) : ")
            if nouveau_email.strip():
                # Check if new email already exists
                if any(u['email'] == nouveau_email and u['id'] != user_to_modify['id'] for u in users):
                    print("⚠️ Cet email est déjà utilisé. Email non modifié.")
                else:
                    user_to_modify['email'] = nouveau_email
            
            # Modify password
            nouveau_password = input(f"Mot de passe (actuel: {'*' * len(user_to_modify['password'])}) : ")
            if nouveau_password.strip():
                user_to_modify['password'] = nouveau_password
            
            # Modify role
            print(f"Rôle actuel: {user_to_modify['role']}")
            print("Modifier le rôle ? (o/n) : ")
            if input().lower() == 'o':
                print("1. Administrateur")
                print("2. Enseignant")
                print("3. Etudiant")
                role_choix = input("Nouveau rôle (1, 2 ou 3) : ")
                
                if role_choix == '1':
                    user_to_modify['role'] = 'administrateur'
                elif role_choix == '2':
                    user_to_modify['role'] = 'enseignant'
                elif role_choix == '3':
                    user_to_modify['role'] = 'etudiant'
            
            save_users(users)
            print(f"✅ Utilisateur '{user_to_modify['nom']}' modifié avec succès.")
        else:
            print("❌ Choix invalide.")
    except ValueError:
        print("❌ Veuillez entrer un nombre.")

def consulter_utilisateurs():
    """View all users"""
    print("\n--- Liste des utilisateurs ---")
    
    users = load_users()
    
    if not users:
        print("❌ Aucun utilisateur enregistré.")
        return
    
    print(f"\nTotal: {len(users)} utilisateur(s)\n")
    
    for u in users:
        print(f"ID: {u['id']}")
        print(f"  Nom: {u['nom']}")
        print(f"  Username: {u['username']}")
        print(f"  Email: {u['email']}")
        print(f"  Rôle: {u['role']}")
        print()

def rechercher_utilisateur():
    """Search for a user"""
    print("\n--- Rechercher un utilisateur ---")
    
    print("1. Rechercher par nom")
    print("2. Rechercher par email")
    print("3. Rechercher par ID")
    print("4. Rechercher par rôle")
    
    choix = input("Votre choix : ")
    
    users = load_users()
    results = []
    
    if choix == '1':
        nom = input("Entrez le nom à rechercher : ")
        results = [u for u in users if nom.lower() in u['nom'].lower()]
    
    elif choix == '2':
        email = input("Entrez l'email à rechercher : ")
        results = [u for u in users if email.lower() in u['email'].lower()]
    
    elif choix == '3':
        try:
            user_id = int(input("Entrez l'ID à rechercher : "))
            results = [u for u in users if u['id'] == user_id]
        except ValueError:
            print("❌ ID invalide.")
            return
    
    elif choix == '4':
        print("1. Administrateur")
        print("2. Enseignant")
        print("3. Etudiant")
        role_choix = input("Choisissez le rôle : ")
        
        if role_choix == '1':
            role = 'administrateur'
        elif role_choix == '2':
            role = 'enseignant'
        elif role_choix == '3':
            role = 'etudiant'
        else:
            print("❌ Choix invalide.")
            return
        
        results = [u for u in users if u['role'] == role]
    
    else:
        print("❌ Choix invalide.")
        return
    
    if results:
        print(f"\n✅ {len(results)} résultat(s) trouvé(s):\n")
        for u in results:
            print(f"ID: {u['id']} | Nom: {u['nom']} | Email: {u['email']} | Rôle: {u['role']}")
    else:
        print("❌ Aucun résultat trouvé.")
