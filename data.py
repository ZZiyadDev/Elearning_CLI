import os
import django

# Setup Django environment so this can be run directly from CLI
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning_project.settings')
django.setup()

from core.models import Utilisateur, Course, Lesson, Quiz, Question, Progress

def get_next_id(data_list):
    if not data_list:
        return 1
    return max(item.get('id', 0) for item in data_list) + 1

# Validation functions (unchanged)
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

# DB Loaders and Savers

def load_users():
    return [
        {
            "id": u.id,
            "nom": u.nom,
            "email": u.email,
            "username": u.username,
            "password": u.password,
            "role": u.role
        }
        for u in Utilisateur.objects.all()
    ]

def save_users(users):
    existing_ids = set(u.id for u in Utilisateur.objects.all())
    new_ids = set()
    for u in users:
        new_ids.add(u['id'])
        Utilisateur.objects.update_or_create(
            id=u['id'],
            defaults={
                'nom': u['nom'],
                'email': u['email'],
                'username': u['username'],
                'password': u['password'],
                'role': u['role']
            }
        )
    # Delete users that are no longer in the list
    Utilisateur.objects.filter(id__in=existing_ids - new_ids).delete()

def load_courses():
    courses = []
    for c in Course.objects.prefetch_related('lessons', 'quizzes__questions', 'enrolled_students').all():
        course_dict = {
            "id": c.id,
            "title": c.title,
            "teacher_id": c.teacher_id,
            "enrolled_students": [s.id for s in c.enrolled_students.all()],
            "lessons": [
                {
                    "lesson_id": l.lesson_id,
                    "title": l.title,
                    "content": l.content
                } for l in c.lessons.all()
            ],
            "quizzes": [
                {
                    "quiz_id": q.quiz_id,
                    "title": q.title,
                    "questions": [
                        {
                            "question": qn.question,
                            "options": qn.options,
                            "correct_answer": qn.correct_answer
                        } for qn in q.questions.all()
                    ]
                } for q in c.quizzes.all()
            ]
        }
        courses.append(course_dict)
    return courses

def save_courses(courses):
    existing_ids = set(c.id for c in Course.objects.all())
    new_ids = set()
    for c in courses:
        new_ids.add(c['id'])
        teacher = Utilisateur.objects.get(id=c['teacher_id'])
        course, _ = Course.objects.update_or_create(
            id=c['id'],
            defaults={
                'title': c['title'],
                'teacher': teacher
            }
        )
        
        # Update enrolled students
        if 'enrolled_students' in c:
            students = Utilisateur.objects.filter(id__in=c['enrolled_students'])
            course.enrolled_students.set(students)
            
        # Update lessons
        course.lessons.all().delete()
        for l in c.get('lessons', []):
            Lesson.objects.create(
                course=course,
                lesson_id=l['lesson_id'],
                title=l['title'],
                content=l['content']
            )
            
        # Update quizzes
        course.quizzes.all().delete()
        for q in c.get('quizzes', []):
            quiz = Quiz.objects.create(
                course=course,
                quiz_id=q['quiz_id'],
                title=q['title']
            )
            for qn in q.get('questions', []):
                Question.objects.create(
                    quiz=quiz,
                    question=qn['question'],
                    options=qn['options'],
                    correct_answer=qn['correct_answer']
                )
    
    # Delete courses no longer in list
    Course.objects.filter(id__in=existing_ids - new_ids).delete()

def load_progress():
    return [
        {
            "student_id": p.student_id,
            "course_id": p.course_id,
            "completed_lessons": p.completed_lessons,
            "quiz_scores": p.quiz_scores
        }
        for p in Progress.objects.all()
    ]

def save_progress(progress):
    existing = set((p.student.id, p.course.id) for p in Progress.objects.all())
    new = set()
    for p in progress:
        new.add((p['student_id'], p['course_id']))
        student = Utilisateur.objects.get(id=p['student_id'])
        course = Course.objects.get(id=p['course_id'])
        Progress.objects.update_or_create(
            student=student,
            course=course,
            defaults={
                'completed_lessons': p.get('completed_lessons', []),
                'quiz_scores': p.get('quiz_scores', {})
            }
        )
    # Delete removed
    for student_id, course_id in (existing - new):
        Progress.objects.filter(student_id=student_id, course_id=course_id).delete()
