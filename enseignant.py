from data import load_courses, save_courses, get_next_id, load_users, load_progress

def menu_enseignant(user):
    while True:
        print("\n=== Espace Enseignant ===")
        print("1. Créer un cours")
        print("2. Modifier un cours")
        print("3. Gérer ses élèves (Voir inscriptions et progression)")
        print("4. Quitter")
        
        choix = input("Votre choix : ")
        if choix == '1':
            creer_cours(user)
        elif choix == '2':
            modifier_cours(user)
        elif choix == '3':
            gerer_eleves(user)
        elif choix == '4':
            break
        else:
            print("Choix invalide.")

def creer_cours(user):
    print("\n--- Création d'un cours ---")
    titre = input("Titre du cours : ")
    
    courses = load_courses()
    new_course = {
        "id": get_next_id(courses),
        "title": titre,
        "teacher_id": user['id'],
        "lessons": [],
        "enrolled_students": []
    }
    
    while True:
        ajouter_lecon = input("Voulez-vous ajouter une leçon maintenant ? (o/n) : ")
        if ajouter_lecon.lower() == 'o':
            titre_lecon = input("Titre de la leçon : ")
            contenu = input("Contenu de la leçon : ")
            
            lecon = {
                "lesson_id": len(new_course['lessons']) + 1,
                "title": titre_lecon,
                "content": contenu
            }
            new_course['lessons'].append(lecon)
        else:
            break
            
    courses.append(new_course)
    save_courses(courses)
    print("Cours créé avec succès !")

def modifier_cours(user):
    print("\n--- Modification d'un cours ---")
    courses = load_courses()
    my_courses = [c for c in courses if c['teacher_id'] == user['id']]
    
    if not my_courses:
        print("Vous n'avez créé aucun cours.")
        return
        
    for idx, c in enumerate(my_courses, 1):
        print(f"{idx}. {c['title']} (ID: {c['id']})")
        
    try:
        choix = int(input("Choisissez le numéro du cours à modifier : "))
        if 1 <= choix <= len(my_courses):
            selected_course = my_courses[choix - 1]
            
            # Find the actual index in the main list
            course_index = next(i for i, c in enumerate(courses) if c['id'] == selected_course['id'])
            
            nouveau_titre = input(f"Nouveau titre (laisser vide pour garder '{selected_course['title']}') : ")
            if nouveau_titre.strip():
                courses[course_index]['title'] = nouveau_titre
                
            print("Leçons actuelles :")
            for lecon in courses[course_index]['lessons']:
                print(f" - Leçon {lecon['lesson_id']}: {lecon['title']}")
                
            ajouter = input("Ajouter une nouvelle leçon ? (o/n) : ")
            if ajouter.lower() == 'o':
                titre_lecon = input("Titre de la leçon : ")
                contenu = input("Contenu de la leçon : ")
                
                lecon = {
                    "lesson_id": len(courses[course_index]['lessons']) + 1,
                    "title": titre_lecon,
                    "content": contenu
                }
                courses[course_index]['lessons'].append(lecon)
                
            save_courses(courses)
            print("Cours modifié avec succès !")
        else:
            print("Choix invalide.")
    except ValueError:
        print("Veuillez entrer un nombre.")

def gerer_eleves(user):
    print("\n--- Gestion des élèves ---")
    courses = load_courses()
    users = load_users()
    progress_data = load_progress()
    
    my_courses = [c for c in courses if c['teacher_id'] == user['id']]
    
    if not my_courses:
        print("Vous n'avez créé aucun cours.")
        return
        
    for c in my_courses:
        print(f"\nCours : {c['title']}")
        if not c['enrolled_students']:
            print("  Aucun élève inscrit.")
            continue
            
        total_lessons = len(c['lessons'])
            
        for student_id in c['enrolled_students']:
            # Find student details
            student = next((u for u in users if u['id'] == student_id), None)
            student_name = student['nom'] if student else f"Utilisateur inconnu ({student_id})"
            
            # Find progress
            prog = next((p for p in progress_data if p['student_id'] == student_id and p['course_id'] == c['id']), None)
            completed = len(prog['completed_lessons']) if prog else 0
            
            if total_lessons > 0:
                percentage = (completed / total_lessons) * 100
                print(f"  - {student_name} : {completed}/{total_lessons} leçons terminées ({percentage:.1f}%)")
            else:
                print(f"  - {student_name} : {completed}/{total_lessons} leçons terminées (Cours vide)")
