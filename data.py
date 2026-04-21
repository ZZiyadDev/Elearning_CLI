import json
import os

def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_next_id(data_list):
    if not data_list:
        return 1
    return max(item.get('id', 0) for item in data_list) + 1

# Validation functions
def validate_username(username):
    if not username or not isinstance(username, str):
        return False, "Nom d'utilisateur requis."
    if len(username) < 3 or len(username) > 20:
        return False, "Le nom d'utilisateur doit contenir entre 3 et 20 caractères."
    if not username.replace('_', '').replace('-', '').isalnum():
        return False, "Le nom d'utilisateur ne peut contenir que des lettres, chiffres, _ et -."
    return True, ""

def validate_password(password):
    if not password or len(password) < 6:
        return False, "Le mot de passe doit contenir au moins 6 caractères."
    return True, ""

def validate_choice(choice, valid_options):
    if choice not in valid_options:
        return False, f"Choix invalide. Options valides: {', '.join(valid_options)}"
    return True, ""

def get_valid_input(prompt, validator_func, *args):
    while True:
        user_input = input(prompt).strip()
        valid, message = validator_func(user_input, *args)
        if valid:
            return user_input
        print(f"Erreur: {message}")

# Specific helpers

def load_users():
    return load_data('users.json')

def save_users(users):
    save_data('users.json', users)

def load_courses():
    return load_data('courses.json')

def save_courses(courses):
    save_data('courses.json', courses)

def load_progress():
    return load_data('progress.json')

def save_progress(progress):
    save_data('progress.json', progress)
