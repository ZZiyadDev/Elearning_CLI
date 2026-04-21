from data import load_users, save_courses, save_users, load_courses, load_progress

def menu_admin(user):
    while True:
        print("\n=== Espace Administrateur ===")
        print("1. Gérer les utilisateurs")
        print("2. Gérer les cours")
        print("3. Voir les statistiques")
        print("4. Quitter")

        choix = input("Votre choix : ")
        if choix == '1':
            gerer_utilisateurs()
        elif choix == '2':
            gerer_cours()
        elif choix == '3':
            voir_statistiques()
        elif choix == '4':
            break
        else:
            print("Choix invalide.")

def gerer_utilisateurs():
    while True:
        print("\n--- Gestion des Utilisateurs ---")
        print("1. Lister tous les utilisateurs")
        print("2. Supprimer un utilisateur")
        print("3. Changer le rôle d'un utilisateur")
        print("4. Retour")

        choix = input("Votre choix : ")
        if choix == '1':
            lister_utilisateurs()
        elif choix == '2':
            supprimer_utilisateur()
        elif choix == '3':
            changer_role_utilisateur()
        elif choix == '4':
            break
        else:
            print("Choix invalide.")

def lister_utilisateurs():
    users = load_users()
    if not users:
        print("Aucun utilisateur trouvé.")
        return

    print("\nListe des utilisateurs :")
    for user in users:
        print(f"ID: {user['id']}, Nom: {user['username']}, Rôle: {user['role']}")

def supprimer_utilisateur():
    users = load_users()
    lister_utilisateurs()

    try:
        user_id = int(input("Entrez l'ID de l'utilisateur à supprimer : "))
        user = next((u for u in users if u['id'] == user_id), None)
        if not user:
            print("Utilisateur non trouvé.")
            return

        confirm = input(f"Êtes-vous sûr de vouloir supprimer {user['username']} ? (o/n) : ")
        if confirm.lower() == 'o':
            users = [u for u in users if u['id'] != user_id]
            save_users(users)
            print("Utilisateur supprimé.")
        else:
            print("Suppression annulée.")
    except ValueError:
        print("ID invalide.")

def changer_role_utilisateur():
    users = load_users()
    lister_utilisateurs()

    try:
        user_id = int(input("Entrez l'ID de l'utilisateur : "))
        user = next((u for u in users if u['id'] == user_id), None)
        if not user:
            print("Utilisateur non trouvé.")
            return

        print("Rôles disponibles : enseignant, etudiant, admin")
        new_role = input(f"Nouveau rôle pour {user['username']} (actuel: {user['role']}) : ").lower()
        if new_role in ['enseignant', 'etudiant', 'admin']:
            user['role'] = new_role
            save_users(users)
            print("Rôle mis à jour.")
        else:
            print("Rôle invalide.")
    except ValueError:
        print("ID invalide.")

def gerer_cours():
    while True:
        print("\n--- Gestion des Cours ---")
        print("1. Lister tous les cours")
        print("2. Supprimer un cours")
        print("3. Voir les détails d'un cours")
        print("4. Retour")

        choix = input("Votre choix : ")
        if choix == '1':
            lister_cours()
        elif choix == '2':
            supprimer_cours()
        elif choix == '3':
            details_cours()
        elif choix == '4':
            break
        else:
            print("Choix invalide.")

def lister_cours():
    courses = load_courses()
    if not courses:
        print("Aucun cours trouvé.")
        return

    print("\nListe des cours :")
    for course in courses:
        print(f"ID: {course['id']}, Titre: {course['title']}, Enseignant ID: {course['teacher_id']}, Élèves inscrits: {len(course.get('enrolled_students', []))}")

def supprimer_cours():
    courses = load_courses()
    lister_cours()

    try:
        course_id = int(input("Entrez l'ID du cours à supprimer : "))
        course = next((c for c in courses if c['id'] == course_id), None)
        if not course:
            print("Cours non trouvé.")
            return

        confirm = input(f"Êtes-vous sûr de vouloir supprimer '{course['title']}' ? (o/n) : ")
        if confirm.lower() == 'o':
            courses = [c for c in courses if c['id'] != course_id]
            save_courses(courses)
            # Also remove from progress
            progress = load_progress()
            progress = [p for p in progress if p['course_id'] != course_id]
            from data import save_progress
            save_progress(progress)
            print("Cours supprimé.")
        else:
            print("Suppression annulée.")
    except ValueError:
        print("ID invalide.")

def details_cours():
    courses = load_courses()
    lister_cours()

    try:
        course_id = int(input("Entrez l'ID du cours : "))
        course = next((c for c in courses if c['id'] == course_id), None)
        if not course:
            print("Cours non trouvé.")
            return

        print(f"\nDétails du cours '{course['title']}' :")
        print(f"Enseignant ID: {course['teacher_id']}")
        print(f"Élèves inscrits: {len(course.get('enrolled_students', []))}")
        print(f"Leçons: {len(course.get('lessons', []))}")
        for lesson in course.get('lessons', []):
            print(f"  - {lesson['lesson_id']}: {lesson['title']}")
    except ValueError:
        print("ID invalide.")

def voir_statistiques():
    users = load_users()
    courses = load_courses()
    progress = load_progress()

    print("\n--- Statistiques Système ---")
    print(f"Nombre total d'utilisateurs: {len(users)}")
    print(f"  - Enseignants: {len([u for u in users if u['role'] == 'enseignant'])}")
    print(f"  - Étudiants: {len([u for u in users if u['role'] == 'etudiant'])}")
    print(f"  - Admins: {len([u for u in users if u['role'] == 'admin'])}")

    print(f"Nombre total de cours: {len(courses)}")
    total_enrollments = sum(len(c.get('enrolled_students', [])) for c in courses)
    print(f"Total des inscriptions: {total_enrollments}")

    total_lessons = sum(len(c.get('lessons', [])) for c in courses)
    total_completed = sum(len(p.get('completed_lessons', [])) for p in progress)
    print(f"Leçons totales: {total_lessons}")
    print(f"Leçons terminées: {total_completed}")
    if total_lessons > 0:
        completion_rate = (total_completed / total_lessons) * 100
        print(f"Taux de complétion global: {completion_rate:.1f}%")