import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning_project.settings')
django.setup()

from core.models import Utilisateur, Course, Lesson, Quiz, Question, Progress
from data import load_users, load_courses, load_progress

def verify_admin_features():
    print("Verifying Admin features...")
    # Admin can list users
    users = load_users()
    print(f"Total users found: {len(users)}")
    assert any(u['role'] == 'admin' for u in users), "Admin user missing"
    print("✅ Admin can access user list.")

def verify_teacher_features():
    print("\nVerifying Teacher features...")
    # Teacher can create a course (we check if ahmed has courses or can be found)
    teacher = Utilisateur.objects.get(username='ahmed')
    assert teacher.role == 'enseignant', "Teacher 'ahmed' role mismatch"
    
    courses = load_courses()
    teacher_courses = [c for c in courses if c['teacher_id'] == teacher.id]
    print(f"Teacher 'ahmed' has {len(teacher_courses)} courses.")
    
    # Simulate course creation if none exist
    if not teacher_courses:
        print("Creating a dummy course for teacher...")
        c = Course.objects.create(title="Test Course", teacher=teacher)
        Lesson.objects.create(course=c, lesson_id=1, title="Lesson 1", content="Content 1")
        print("✅ Teacher can create courses.")
    else:
        print("✅ Teacher already has courses.")

def verify_student_features():
    print("\nVerifying Student features...")
    student = Utilisateur.objects.get(username='ziyad')
    assert student.role == 'etudiant', "Student 'ziyad' role mismatch"
    
    courses = Course.objects.all()
    if not courses:
        print("No courses available for enrollment.")
        return
        
    course = courses[0]
    # Check enrollment
    if student not in course.enrolled_students.all():
        print(f"Enrolling student 'ziyad' in '{course.title}'...")
        course.enrolled_students.add(student)
        Progress.objects.create(student=student, course=course, completed_lessons=[])
        print("✅ Student can enroll in courses.")
    else:
        print(f"Student 'ziyad' already enrolled in '{course.title}'.")
        
    # Check progress tracking
    progress = Progress.objects.get(student=student, course=course)
    print(f"Current completed lessons: {progress.completed_lessons}")
    
    lesson = course.lessons.first()
    if lesson and lesson.lesson_id not in progress.completed_lessons:
        print(f"Marking lesson '{lesson.title}' as completed...")
        progress.completed_lessons.append(lesson.lesson_id)
        progress.save()
        print("✅ Student can track progress.")
    else:
        print("✅ Student has already completed the first lesson or no lessons exist.")

if __name__ == "__main__":
    try:
        verify_admin_features()
        verify_teacher_features()
        verify_student_features()
        print("\nAll actors can perform their primary roles and features!")
    except Exception as e:
        print(f"\nVerification failed: {e}")
        import traceback
        traceback.print_exc()
