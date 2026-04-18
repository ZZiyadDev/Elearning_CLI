from data import load_users, save_users, get_next_id

def login():
    print("\n--- Connexion ---")
    username = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")

    users = load_users()
    for user in users:
        if user['username'] == username and user['password'] == password:
            print(f"Bienvenue {username} ! (Rôle: {user['role']})")
            return user
    
    print("Nom d'utilisateur ou mot de passe incorrect.")
    return None

def register():
    print("\n--- Inscription ---")
    username = input("Nom d'utilisateur : ")
    
    users = load_users()
    if any(u['username'] == username for u in users):
        print("Ce nom d'utilisateur est déjà pris.")
        return None
        
    password = input("Mot de passe : ")
    
    print("Choisissez votre rôle :")
    print("1. Enseignant")
    print("2. Etudiant")
    
    choix = input("Votre choix (1 ou 2) : ")
    if choix == '1':
        role = 'enseignant'
    elif choix == '2':
        role = 'etudiant'
    else:
        print("Choix invalide.")
        return None
        
    new_user = {
        "id": get_next_id(users),
        "username": username,
        "password": password,
        "role": role
    }
    
    users.append(new_user)
    save_users(users)
    print("Inscription réussie ! Vous pouvez maintenant vous connecter.")
    return None
