import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning_project.settings')
django.setup()

from core.models import Utilisateur, Course, Lesson, Quiz, Question

def create_sample_media_course():
    print("Creating sample course with media and quiz...")
    
    # Use existing teacher 'ahmed'
    teacher = Utilisateur.objects.get(username='ahmed')
    
    # Create Course
    course = Course.objects.create(
        title="Apprentissage du développement Moderne",
        teacher=teacher
    )
    
    # Create Lesson 1: With Video
    Lesson.objects.create(
        course=course,
        lesson_id=1,
        title="Introduction à Django",
        content="Dans cette leçon, nous allons découvrir les bases de Django, un framework web Python puissant.",
        video_url="https://www.youtube.com/watch?v=F5mRW0q-A0E",
        materials_url="https://docs.djangoproject.com/fr/5.0/"
    )
    
    # Create Lesson 2: With Materials only
    Lesson.objects.create(
        course=course,
        lesson_id=2,
        title="Les Modèles et la Base de Données",
        content="Apprenez à définir vos structures de données avec l'ORM de Django.",
        materials_url="https://docs.djangoproject.com/fr/5.0/topics/db/models/"
    )
    
    # Create Quiz
    quiz = Quiz.objects.create(
        course=course,
        quiz_id=1,
        title="Quiz sur les bases de Django"
    )
    
    # Create Questions
    Question.objects.create(
        quiz=quiz,
        question="Quel langage est utilisé par Django ?",
        options=["Java", "Python", "PHP", "JavaScript"],
        correct_answer=1 # Python
    )
    
    Question.objects.create(
        quiz=quiz,
        question="Que signifie ORM ?",
        options=["Object-Relational Mapping", "Object-Real Management", "Optical Resource Module", "Original Record Model"],
        correct_answer=0
    )
    
    print(f"✅ Course '{course.title}' created successfully with 2 lessons and a quiz.")

if __name__ == "__main__":
    create_sample_media_course()
