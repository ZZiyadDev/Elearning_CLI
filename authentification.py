import hashlib
from data import load_users, save_users, get_next_id, validate_username, validate_password, get_valid_input

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    """Login with maximum 3 attempts"""
    max_attempts = 3
    attempts = 0
    
    while attempts < max_attempts:
        print(f"\n--- Connexion (Tentative {attempts + 1}/{max_attempts}) ---")
        username = input("Nom d'utilisateur : ")
        password = input("Mot de passe : ")
        hashed_password = hash_password(password)

        users = load_users()
        for user in users:
            if user['username'] == username and user['password'] == hashed_password:
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
    username = get_valid_input("Nom d'utilisateur : ", validate_username)
    
    users = load_users()
    if any(u['username'] == username for u in users):
        print("Ce nom d'utilisateur est déjà pris.")
        return None
    
    if any(u['email'] == email for u in users):
        print("Cet email est déjà associé à un compte.")
        return None
        
    password = get_valid_input("Mot de passe : ", validate_password)
    
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
        "password": hash_password(password),
        "role": role
    }
    
    users.append(new_user)
    save_users(users)
    print("\nInscription réussie ! Vous pouvez maintenant vous connecter.")
    return None

def change_password(user):
    print("\n--- Changer le mot de passe ---")
    current_password = input("Mot de passe actuel : ")
    if hash_password(current_password) != user['password']:
        print("Mot de passe actuel incorrect.")
        return
    
    new_password = get_valid_input("Nouveau mot de passe : ", validate_password)
    confirm_password = input("Confirmer le nouveau mot de passe : ")
    if new_password != confirm_password:
        print("Les mots de passe ne correspondent pas.")
        return
    
    users = load_users()
    for u in users:
        if u['id'] == user['id']:
            u['password'] = hash_password(new_password)
            break
    save_users(users)
    print("Mot de passe changé avec succès !")
