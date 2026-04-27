from data import load_courses, save_courses, load_progress, save_progress
from authentification import change_password

def menu_etudiant(user):
    while True:
        print("\n=== Espace Etudiant ===")
        print("1. Inscription aux cours")
        print("2. Visionnage des leçons")
        print("3. Suivi de progression")
        print("4. Passer des quiz")
        print("5. Gérer mon profil")
        print("6. Quitter")
        
        choix = input("Votre choix : ")
        if choix == '1':
            inscription_cours(user)
        elif choix == '2':
            visionnage_lecons(user)
        elif choix == '3':
            suivi_progression(user)
        elif choix == '4':
            passer_quiz(user)
        elif choix == '5':
            gerer_profil(user)
        elif choix == '6':
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
        
    page_size = 5
    page = 0
    while True:
        start = page * page_size
        end = start + page_size
        current_courses = available_courses[start:end]
        
        if not current_courses:
            print("Plus de cours disponibles.")
            break
            
        print(f"\nPage {page + 1} (cours {start + 1} à {min(end, len(available_courses))} sur {len(available_courses)})")
        for idx, c in enumerate(current_courses, start + 1):
            print(f"{idx}. {c['title']} ({len(c['lessons'])} leçons)")
            
        print("\nOptions:")
        print("0. Annuler")
        if end < len(available_courses):
            print("n. Page suivante")
        if page > 0:
            print("p. Page précédente")
        
        choix = input("Votre choix : ")
        
        if choix == '0':
            return
        elif choix == 'n' and end < len(available_courses):
            page += 1
        elif choix == 'p' and page > 0:
            page -= 1
        else:
            try:
                choix_num = int(choix)
                if start + 1 <= choix_num <= min(end, len(available_courses)):
                    selected_course = available_courses[choix_num - 1]
                    course_index = next(i for i, c in enumerate(courses) if c['id'] == selected_course['id'])
                    
                    courses[course_index].setdefault('enrolled_students', []).append(user['id'])
                    save_courses(courses)
                    
                    # Initialiser la progression
                    progress_data = load_progress()
                    new_prog = {
                        "student_id": user['id'],
                        "course_id": selected_course['id'],
                        "completed_lessons": [],
                        "quiz_scores": {}
                    }
                    progress_data.append(new_prog)
                    save_progress(progress_data)
                    
                    print(f"Inscription au cours '{selected_course['title']}' réussie !")
                    return
                else:
                    print("Choix invalide.")
            except ValueError:
                print("Choix invalide.")

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
        
        # Show quiz scores
        quiz_scores = prog.get('quiz_scores', {}) if prog else {}
        if quiz_scores:
            print("  Scores de quiz:")
            for quiz_id, score in quiz_scores.items():
                quiz_title = next((q['title'] for q in c.get('quizzes', []) if str(q['quiz_id']) == quiz_id), f"Quiz {quiz_id}")
                print(f"    - {quiz_title}: {score}%")

def passer_quiz(user):
    print("\n--- Passer des quiz ---")
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
            quizzes = selected_course.get('quizzes', [])
            
            if not quizzes:
                print("Ce cours ne contient aucun quiz pour le moment.")
                return
                
            for idx, q in enumerate(quizzes, 1):
                print(f"{idx}. {q['title']}")
                
            quiz_choix = int(input("Choisissez un quiz (0 pour annuler): "))
            if quiz_choix == 0:
                return
                
            if 1 <= quiz_choix <= len(quizzes):
                selected_quiz = quizzes[quiz_choix - 1]
                prendre_quiz(user, selected_course['id'], selected_quiz)
            else:
                print("Choix de quiz invalide.")
        else:
            print("Choix invalide.")
    except ValueError:
        print("Veuillez entrer un nombre.")

def prendre_quiz(user, course_id, quiz):
    print(f"\n--- {quiz['title']} ---")
    progress_data = load_progress()
    prog_index = next((i for i, p in enumerate(progress_data) 
                       if p['student_id'] == user['id'] and p['course_id'] == course_id), None)
    
    if prog_index is None:
        progress_data.append({"student_id": user['id'], "course_id": course_id, "completed_lessons": [], "quiz_scores": {}})
        prog_index = len(progress_data) - 1
        
    prog = progress_data[prog_index]
    quiz_scores = prog.setdefault('quiz_scores', {})
    
    if str(quiz['quiz_id']) in quiz_scores:
        print(f"Vous avez déjà passé ce quiz avec un score de {quiz_scores[str(quiz['quiz_id'])]}%.")
        return
    
    score = 0
    total_questions = len(quiz['questions'])
    
    for question in quiz['questions']:
        print(f"\n{question['question']}")
        for i, option in enumerate(question['options']):
            print(f"{i+1}. {option}")
        
        try:
            answer = int(input("Votre réponse (numéro): ")) - 1
            if answer == question['correct_answer']:
                score += 1
                print("Correct !")
            else:
                print(f"Incorrect. La bonne réponse était: {question['options'][question['correct_answer']]}")
        except (ValueError, IndexError):
            print("Réponse invalide. Considérée comme incorrecte.")
    
    percentage = (score / total_questions) * 100
    quiz_scores[str(quiz['quiz_id'])] = round(percentage, 1)
    progress_data[prog_index]['quiz_scores'] = quiz_scores
    save_progress(progress_data)
    
    print(f"\nQuiz terminé ! Votre score: {score}/{total_questions} ({percentage:.1f}%)")

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
            print(f"Nom complet: {user['nom']}")
            print(f"Email: {user['email']}")
            print(f"Rôle: {user['role']}")
            print(f"ID: {user['id']}")
            courses = load_courses()
            my_courses = [c for c in courses if user['id'] in c.get('enrolled_students', [])]
            print(f"Cours inscrits: {len(my_courses)}")
        elif choix == '3':
            break
        else:
            print("Choix invalide.")
