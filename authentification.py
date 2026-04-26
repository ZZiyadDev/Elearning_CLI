from data import load_users, save_users, get_next_id

def login():
    """Login with maximum 3 attempts"""
    max_attempts = 3
    attempts = 0
    
    while attempts < max_attempts:
        print(f"\n--- Connexion (Tentative {attempts + 1}/{max_attempts}) ---")
        username = input("Nom d'utilisateur : ")
        password = input("Mot de passe : ")

        users = load_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                print(f"\nBienvenue {user['nom']} ! (Rôle: {user['role']})")
                return user
        
        attempts += 1
        remaining = max_attempts - attempts
        if remaining > 0:
            print(f"\nNom d'utilisateur ou mot de passe incorrect. {remaining} tentative(s) restante(s).")
        else:
            print("\nNombre maximum de tentatives dépassé. Accès refusé.")
    
    return None

def register():
    """Register a new user with full details"""
    print("\n--- Inscription ---")
    nom = input("Nom complet : ")
    email = input("Email : ")
    username = input("Nom d'utilisateur : ")
    
    users = load_users()
    if any(u['username'] == username for u in users):
        print("Ce nom d'utilisateur est déjà pris.")
        return None
    
    if any(u['email'] == email for u in users):
        print("Cet email est déjà associé à un compte.")
        return None
        
    password = input("Mot de passe : ")
    
    print("\nChoisissez votre rôle :")
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
        "nom": nom,
        "email": email,
        "username": username,
        "password": password,
        "role": role
    }
    
    users.append(new_user)
    save_users(users)
    print("\nInscription réussie ! Vous pouvez maintenant vous connecter.")
    return None
