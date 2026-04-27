from data import load_courses, save_courses, get_next_id, load_users, load_progress
from authentification import change_password

def menu_enseignant(user):
    while True:
        print("\n=== Espace Enseignant ===")
        print("1. Créer un cours")
        print("2. Modifier un cours")
        print("3. Supprimer un cours")
        print("4. Gérer les quiz")
        print("5. Gérer mes élèves")
        print("6. Gérer mon profil")
        print("7. Quitter")
        
        choix = input("Votre choix : ")
        if choix == '1':
            creer_cours(user)
        elif choix == '2':
            modifier_cours(user)
        elif choix == '3':
            supprimer_cours(user)
        elif choix == '4':
            gerer_quiz(user)
        elif choix == '5':
            gerer_eleves(user)
        elif choix == '6':
            gerer_profil(user)
        elif choix == '7':
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
    new_course.setdefault('quizzes', [])  # Initialize quizzes list
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
                
            print("\nOptions de modification :")
            print("1. Ajouter une nouvelle leçon")
            print("2. Modifier une leçon existante")
            print("3. Supprimer une leçon")
            print("4. Ne rien modifier")
            
            option = input("Votre choix : ")
            if option == '1':
                titre_lecon = input("Titre de la leçon : ")
                contenu = input("Contenu de la leçon : ")
                
                lecon = {
                    "lesson_id": len(courses[course_index]['lessons']) + 1,
                    "title": titre_lecon,
                    "content": contenu
                }
                courses[course_index]['lessons'].append(lecon)
            elif option == '2':
                try:
                    lesson_id = int(input("ID de la leçon à modifier : "))
                    lesson = next((l for l in courses[course_index]['lessons'] if l['lesson_id'] == lesson_id), None)
                    if lesson:
                        new_title = input(f"Nouveau titre (actuel: {lesson['title']}) : ")
                        if new_title.strip():
                            lesson['title'] = new_title
                        new_content = input(f"Nouveau contenu (laisser vide pour garder l'actuel) : ")
                        if new_content.strip():
                            lesson['content'] = new_content
                        print("Leçon modifiée.")
                    else:
                        print("Leçon non trouvée.")
                except ValueError:
                    print("ID invalide.")
            elif option == '3':
                try:
                    lesson_id = int(input("ID de la leçon à supprimer : "))
                    lesson = next((l for l in courses[course_index]['lessons'] if l['lesson_id'] == lesson_id), None)
                    if lesson:
                        confirm = input(f"Supprimer '{lesson['title']}' ? (o/n) : ")
                        if confirm.lower() == 'o':
                            courses[course_index]['lessons'] = [l for l in courses[course_index]['lessons'] if l['lesson_id'] != lesson_id]
                            # Reassign lesson_ids
                            for i, l in enumerate(courses[course_index]['lessons'], 1):
                                l['lesson_id'] = i
                            print("Leçon supprimée.")
                        else:
                            print("Suppression annulée.")
                    else:
                        print("Leçon non trouvée.")
                except ValueError:
                    print("ID invalide.")
            elif option == '4':
                pass
            else:
                print("Option invalide.")
                
            save_courses(courses)
            print("Cours modifié avec succès !")
        else:
            print("Choix invalide.")
    except ValueError:
        print("Veuillez entrer un nombre.")

def supprimer_cours(user):
    print("\n--- Suppression d'un cours ---")
    courses = load_courses()
    my_courses = [c for c in courses if c['teacher_id'] == user['id']]
    
    if not my_courses:
        print("Vous n'avez créé aucun cours.")
        return
        
    for idx, c in enumerate(my_courses, 1):
        print(f"{idx}. {c['title']} (ID: {c['id']})")
        
    try:
        choix = int(input("Choisissez le numéro du cours à supprimer : "))
        if 1 <= choix <= len(my_courses):
            selected_course = my_courses[choix - 1]
            
            confirm = input(f"Êtes-vous sûr de vouloir supprimer '{selected_course['title']}' ? (o/n) : ")
            if confirm.lower() == 'o':
                courses = [c for c in courses if c['id'] != selected_course['id']]
                save_courses(courses)
                # Also remove from progress
                from data import save_progress
                progress = load_progress()
                progress = [p for p in progress if p['course_id'] != selected_course['id']]
                save_progress(progress)
                print("Cours supprimé.")
            else:
                print("Suppression annulée.")
        else:
            print("Choix invalide.")
    except ValueError:
        print("Veuillez entrer un nombre.")

def gerer_quiz(user):
    """Manage quizzes for courses"""
    print("\n--- Gestion des quiz ---")
    courses = load_courses()
    my_courses = [c for c in courses if c['teacher_id'] == user['id']]
    
    if not my_courses:
        print("Vous n'avez créé aucun cours.")
        return
        
    for idx, c in enumerate(my_courses, 1):
        quiz_count = len(c.get('quizzes', []))
        print(f"{idx}. {c['title']} ({quiz_count} quiz)")
        
    try:
        choix = int(input("Choisissez le numéro du cours (0 pour annuler) : "))
        if choix == 0:
            return
            
        if 1 <= choix <= len(my_courses):
            selected_course = my_courses[choix - 1]
            course_index = next(i for i, c in enumerate(courses) if c['id'] == selected_course['id'])
            
            while True:
                print(f"\n--- Quiz du cours '{selected_course['title']}' ---")
                quizzes = courses[course_index].setdefault('quizzes', [])
                
                if quizzes:
                    for idx, q in enumerate(quizzes, 1):
                        print(f"{idx}. {q['title']} ({len(q['questions'])} questions)")
                else:
                    print("Aucun quiz pour ce cours.")
                
                print("\nOptions:")
                print("1. Ajouter un quiz")
                print("2. Modifier un quiz")
                print("3. Supprimer un quiz")
                print("4. Retour")
                
                option = input("Votre choix : ")
                
                if option == '1':
                    titre_quiz = input("Titre du quiz : ")
                    quiz = {
                        "quiz_id": len(quizzes) + 1,
                        "title": titre_quiz,
                        "questions": []
                    }
                    
                    while True:
                        ajouter_q = input("Ajouter une question ? (o/n) : ")
                        if ajouter_q.lower() == 'o':
                            question_text = input("Question : ")
                            options = []
                            print("Entrez les 4 options de réponse:")
                            for i in range(4):
                                option_text = input(f"Option {i+1} : ")
                                options.append(option_text)
                            
                            try:
                                correct = int(input("Numéro de la bonne réponse (1-4) : ")) - 1
                                if 0 <= correct < 4:
                                    quiz['questions'].append({
                                        "question": question_text,
                                        "options": options,
                                        "correct_answer": correct
                                    })
                                    print("✅ Question ajoutée.")
                                else:
                                    print("❌ Numéro invalide.")
                            except ValueError:
                                print("❌ Veuillez entrer un nombre.")
                        else:
                            break
                    
                    if quiz['questions']:
                        quizzes.append(quiz)
                        save_courses(courses)
                        print(f"✅ Quiz '{titre_quiz}' créé avec {len(quiz['questions'])} questions.")
                    else:
                        print("❌ Le quiz doit avoir au moins une question.")
                
                elif option == '2':
                    if not quizzes:
                        print("❌ Aucun quiz à modifier.")
                        continue
                    
                    try:
                        quiz_idx = int(input("Numéro du quiz à modifier : ")) - 1
                        if 0 <= quiz_idx < len(quizzes):
                            quiz = quizzes[quiz_idx]
                            new_title = input(f"Nouveau titre (actuel: {quiz['title']}) : ")
                            if new_title.strip():
                                quiz['title'] = new_title
                            
                            print("Questions actuelles:")
                            for i, q in enumerate(quiz['questions'], 1):
                                print(f"{i}. {q['question']}")
                            
                            save_courses(courses)
                            print("✅ Quiz modifié.")
                        else:
                            print("❌ Numéro invalide.")
                    except ValueError:
                        print("❌ Veuillez entrer un nombre.")
                
                elif option == '3':
                    if not quizzes:
                        print("❌ Aucun quiz à supprimer.")
                        continue
                    
                    try:
                        quiz_idx = int(input("Numéro du quiz à supprimer : ")) - 1
                        if 0 <= quiz_idx < len(quizzes):
                            confirm = input(f"Supprimer '{quizzes[quiz_idx]['title']}' ? (o/n) : ")
                            if confirm.lower() == 'o':
                                quizzes.pop(quiz_idx)
                                # Reassign quiz IDs
                                for i, q in enumerate(quizzes, 1):
                                    q['quiz_id'] = i
                                save_courses(courses)
                                print("✅ Quiz supprimé.")
                        else:
                            print("❌ Numéro invalide.")
                    except ValueError:
                        print("❌ Veuillez entrer un nombre.")
                
                elif option == '4':
                    break
                else:
                    print("❌ Option invalide.")
        else:
            print("❌ Choix invalide.")
    except ValueError:
        print("❌ Veuillez entrer un nombre.")

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

def gerer_profil(user):
    while True:
        print("\n--- Gestion du profil ---")
        print("1. Changer le mot de passe")
        print("2. Voir mes informations")
        print("3. Retour")
        
        choix = input("Votre choix : ")
        if choix == '1':
            change_password(user)
        elif choix == '2':
            print(f"\nNom d'utilisateur: {user['username']}")
            print(f"Rôle: {user['role']}")
            print(f"ID: {user['id']}")
            courses = load_courses()
            my_courses = [c for c in courses if c['teacher_id'] == user['id']]
            print(f"Cours créés: {len(my_courses)}")
        elif choix == '3':
            break
        else:
            print("Choix invalide.")
