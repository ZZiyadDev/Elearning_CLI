import os
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning_project.settings')
django.setup()

from core.models import Utilisateur, Course, Lesson, Quiz, Question, Progress

def load_json(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def migrate_users():
    users_data = load_json('users.json')
    for u_data in users_data:
        Utilisateur.objects.get_or_create(
            id=u_data['id'],
            defaults={
                'nom': u_data['nom'],
                'email': u_data['email'],
                'username': u_data['username'],
                'password': u_data['password'],
                'role': u_data['role']
            }
        )
    print(f"Migrated {len(users_data)} users.")

def migrate_courses():
    courses_data = load_json('courses.json')
    for c_data in courses_data:
        teacher = Utilisateur.objects.get(id=c_data['teacher_id'])
        course, created = Course.objects.get_or_create(
            id=c_data['id'],
            defaults={
                'title': c_data['title'],
                'teacher': teacher
            }
        )
        
        if created or course:
            # Enrolled students
            if 'enrolled_students' in c_data:
                students = Utilisateur.objects.filter(id__in=c_data['enrolled_students'])
                course.enrolled_students.set(students)
            
            # Lessons
            for l_data in c_data.get('lessons', []):
                Lesson.objects.get_or_create(
                    course=course,
                    lesson_id=l_data['lesson_id'],
                    defaults={
                        'title': l_data['title'],
                        'content': l_data['content']
                    }
                )
                
            # Quizzes
            for q_data in c_data.get('quizzes', []):
                quiz, q_created = Quiz.objects.get_or_create(
                    course=course,
                    quiz_id=q_data['quiz_id'],
                    defaults={
                        'title': q_data['title']
                    }
                )
                
                # Questions
                for q_index, qn_data in enumerate(q_data.get('questions', [])):
                    Question.objects.get_or_create(
                        quiz=quiz,
                        question=qn_data['question'],
                        defaults={
                            'options': qn_data['options'],
                            'correct_answer': qn_data['correct_answer']
                        }
                    )
    print(f"Migrated {len(courses_data)} courses with lessons, quizzes, and questions.")

def migrate_progress():
    progress_data = load_json('progress.json')
    for p_data in progress_data:
        student = Utilisateur.objects.get(id=p_data['student_id'])
        course = Course.objects.get(id=p_data['course_id'])
        
        Progress.objects.get_or_create(
            student=student,
            course=course,
            defaults={
                'completed_lessons': p_data.get('completed_lessons', []),
                'quiz_scores': p_data.get('quiz_scores', {})
            }
        )
    print(f"Migrated {len(progress_data)} progress records.")

if __name__ == '__main__':
    print("Starting data migration...")
    migrate_users()
    migrate_courses()
    migrate_progress()
    print("Migration complete!")
