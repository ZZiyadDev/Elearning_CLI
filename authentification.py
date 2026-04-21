import hashlib
from data import load_users, save_users, get_next_id, validate_username, validate_password, get_valid_input

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    print("\n--- Connexion ---")
    username = get_valid_input("Nom d'utilisateur : ", validate_username)
    password = input("Mot de passe : ")
    hashed_password = hash_password(password)

    users = load_users()
    for user in users:
        if user['username'] == username and user['password'] == hashed_password:
            print(f"Bienvenue {username} ! (Rôle: {user['role']})")
            return user
    
    print("Nom d'utilisateur ou mot de passe incorrect.")
    return None

def register():
    print("\n--- Inscription ---")
    username = get_valid_input("Nom d'utilisateur : ", validate_username)
    
    users = load_users()
    if any(u['username'] == username for u in users):
        print("Ce nom d'utilisateur est déjà pris.")
        return None
        
    password = get_valid_input("Mot de passe : ", validate_password)
    
    print("Choisissez votre rôle :")
    print("1. Enseignant")
    print("2. Etudiant")
    print("3. Administrateur")
    
    choix = get_valid_input("Votre choix (1, 2 ou 3) : ", lambda x: (x in ['1','2','3'], "Choix invalide."))
    if choix == '1':
        role = 'enseignant'
    elif choix == '2':
        role = 'etudiant'
    elif choix == '3':
        role = 'admin'
        
    new_user = {
        "id": get_next_id(users),
        "username": username,
        "password": hash_password(password),
        "role": role
    }
    
    users.append(new_user)
    save_users(users)
    print("Inscription réussie ! Vous pouvez maintenant vous connecter.")
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
