from data import load_courses, save_courses, load_progress, save_progress

def menu_etudiant(user):
    while True:
        print("\n=== Espace Etudiant ===")
        print("1. Inscription aux cours")
        print("2. Visionnage des leçons")
        print("3. Suivi de progression")
        print("4. Quitter")
        
        choix = input("Votre choix : ")
        if choix == '1':
            inscription_cours(user)
        elif choix == '2':
            visionnage_lecons(user)
        elif choix == '3':
            suivi_progression(user)
        elif choix == '4':
            break
        else:
            print("Choix invalide.")

def inscription_cours(user):
    print("\n--- Inscription aux cours ---")
    courses = load_courses()
    
    available_courses = [c for c in courses if user['id'] not in c.get('enrolled_students', [])]
    
    if not available_courses:
        print("Vous êtes déjà inscrit(e) à tous les cours disponibles.")
        return
        
    for idx, c in enumerate(available_courses, 1):
        print(f"{idx}. {c['title']} ({len(c['lessons'])} leçons)")
        
    try:
        choix = int(input("Choisissez le numéro du cours auquel vous inscrire (0 pour annuler): "))
        if choix == 0:
            return
            
        if 1 <= choix <= len(available_courses):
            selected_course = available_courses[choix - 1]
            course_index = next(i for i, c in enumerate(courses) if c['id'] == selected_course['id'])
            
            courses[course_index].setdefault('enrolled_students', []).append(user['id'])
            save_courses(courses)
            
            # Initialiser la progression
            progress_data = load_progress()
            new_prog = {
                "student_id": user['id'],
                "course_id": selected_course['id'],
                "completed_lessons": []
            }
            progress_data.append(new_prog)
            save_progress(progress_data)
            
            print(f"Inscription au cours '{selected_course['title']}' réussie !")
        else:
            print("Choix invalide.")
    except ValueError:
        print("Veuillez entrer un nombre.")

def visionnage_lecons(user):
    print("\n--- Visionnage des leçons ---")
    courses = load_courses()
    my_courses = [c for c in courses if user['id'] in c.get('enrolled_students', [])]
    
    if not my_courses:
        print("Vous n'êtes inscrit à aucun cours.")
        return
        
    for idx, c in enumerate(my_courses, 1):
        print(f"{idx}. {c['title']}")
        
    try:
        choix = int(input("Choisissez un cours (0 pour annuler): "))
        if choix == 0:
            return
            
        if 1 <= choix <= len(my_courses):
            selected_course = my_courses[choix - 1]
            lessons = selected_course.get('lessons', [])
            
            if not lessons:
                print("Ce cours ne contient aucune leçon pour le moment.")
                return
                
            progress_data = load_progress()
            prog_index = next((i for i, p in enumerate(progress_data) 
                               if p['student_id'] == user['id'] and p['course_id'] == selected_course['id']), None)
                               
            if prog_index is None:
                # Récupère / crée si manquant
                progress_data.append({"student_id": user['id'], "course_id": selected_course['id'], "completed_lessons": []})
                prog_index = len(progress_data) - 1
                
            prog = progress_data[prog_index]
            completed = prog.get('completed_lessons', [])
            
            for idx, lecon in enumerate(lessons, 1):
                status = "[x]" if lecon['lesson_id'] in completed else "[ ]"
                print(f"{idx}. {status} {lecon['title']}")
                
            lecon_choix = int(input("Choisissez une leçon à lire (0 pour annuler): "))
            if lecon_choix == 0:
                return
                
            if 1 <= lecon_choix <= len(lessons):
                selected_lesson = lessons[lecon_choix - 1]
                print(f"\n--- {selected_lesson['title']} ---")
                print(selected_lesson['content'])
                print("-" * 20)
                
                if selected_lesson['lesson_id'] not in completed:
                    completed.append(selected_lesson['lesson_id'])
                    progress_data[prog_index]['completed_lessons'] = completed
                    save_progress(progress_data)
                    print("Leçon marquée comme terminée !")
            else:
                print("Choix de leçon invalide.")
        else:
            print("Choix invalide.")
    except ValueError:
        print("Veuillez entrer un nombre.")

def suivi_progression(user):
    print("\n--- Suivi de progression ---")
    courses = load_courses()
    progress_data = load_progress()
    
    my_courses = [c for c in courses if user['id'] in c.get('enrolled_students', [])]
    
    if not my_courses:
        print("Vous n'êtes inscrit(e) à aucun cours.")
        return
        
    for c in my_courses:
        prog = next((p for p in progress_data if p['student_id'] == user['id'] and p['course_id'] == c['id']), None)
        total_lessons = len(c.get('lessons', []))
        
        if not c.get('lessons'):
            print(f"- {c['title']} : Cours vide (Pas de pourcentage)")
            continue
            
        completed_count = len(prog['completed_lessons']) if prog else 0
        percentage = (completed_count / total_lessons) * 100
        print(f"- {c['title']} : {completed_count}/{total_lessons} leçons terminées ({percentage:.1f}%)")
