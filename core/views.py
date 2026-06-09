from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from .models import Utilisateur, Course, Lesson, Quiz, Question, Progress


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')


def register_view(request):
    if request.method == 'POST':
        nom = request.POST['nom']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        try:
            user = Utilisateur.objects.create_user(
                username=username,
                email=email,
                password=password,
                nom=nom,
                role=role,
            )
            login(request, user)
            return redirect('dashboard')
        except IntegrityError:
            return render(request, 'core/register.html', {
                'error': "Ce nom d'utilisateur existe déjà."
            })
    return render(request, 'core/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        return render(request, 'core/login.html', {
            'error': "Identifiants incorrects."
        })
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    user = request.user
    if user.role == 'etudiant':
        courses = Course.objects.filter(enrolled_students=user)
        progress_data = []
        for course in courses:
            progress = Progress.objects.filter(student=user, course=course).first()
            lesson_count = course.lessons.count()
            completed_count = len(progress.completed_lessons) if progress else 0
            percentage = int((completed_count / lesson_count * 100)) if lesson_count > 0 else 0
            progress_data.append({
                'course': course,
                'percentage': percentage,
                'completed_count': completed_count
            })
        return render(request, 'core/etudiant_dashboard.html', {
            'progress_data': progress_data,
        })
    elif user.role == 'enseignant':
        courses = Course.objects.filter(teacher=user)
        return render(request, 'core/enseignant_dashboard.html', {
            'courses': courses,
        })
    elif user.role == 'admin':
        stats = {
            'total_users': Utilisateur.objects.count(),
            'total_courses': Course.objects.count(),
            'total_etudiants': Utilisateur.objects.filter(role='etudiant').count(),
            'total_enseignants': Utilisateur.objects.filter(role='enseignant').count(),
        }
        return render(request, 'core/admin_dashboard.html', {
            'stats': stats,
        })
    return redirect('home')


@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'core/course_list.html', {'courses': courses})


@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    is_enrolled = course.enrolled_students.filter(id=request.user.id).exists()
    return render(request, 'core/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled
    })


@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user.role == 'etudiant':
        course.enrolled_students.add(request.user)
        Progress.objects.get_or_create(student=request.user, course=course)
    return redirect('course_detail', pk=pk)


import re

def get_youtube_embed_url(url):
    if not url:
        return None
    # Support various YouTube URL formats
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    match = re.match(youtube_regex, url)
    if match:
        video_id = match.group(6)
        return f"https://www.youtube.com/embed/{video_id}"
    return None

@login_required
def lesson_detail(request, course_pk, lesson_id):
    course = get_object_or_404(Course, pk=course_pk)
    lesson = get_object_or_404(Lesson, course=course, lesson_id=lesson_id)
    
    # Update progress
    if request.user.role == 'etudiant':
        progress, created = Progress.objects.get_or_create(student=request.user, course=course)
        if lesson_id not in progress.completed_lessons:
            progress.completed_lessons.append(lesson_id)
            progress.save()
            
    next_lesson = Lesson.objects.filter(course=course, lesson_id__gt=lesson_id).order_by('lesson_id').first()
    
    embed_url = get_youtube_embed_url(lesson.video_url)
    
    return render(request, 'core/lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'next_lesson': next_lesson,
        'embed_url': embed_url
    })


@login_required
def quiz_detail(request, course_pk, quiz_id):
    course = get_object_or_404(Course, pk=course_pk)
    quiz = get_object_or_404(Quiz, course=course, quiz_id=quiz_id)
    is_enrolled = course.enrolled_students.filter(id=request.user.id).exists()
    
    if not is_enrolled and request.user.role == 'etudiant':
        return redirect('course_detail', pk=course_pk)

    if request.method == 'POST':
        score = 0
        total = quiz.questions.count()
        for question in quiz.questions.all():
            answer = request.POST.get(f'question_{question.id}')
            if answer is not None and int(answer) == question.correct_answer:
                score += 1
        
        # Save score in progress
        if request.user.role == 'etudiant':
            progress, _ = Progress.objects.get_or_create(student=request.user, course=course)
            progress.quiz_scores[str(quiz_id)] = score
            progress.save()
            
        return render(request, 'core/quiz_result.html', {
            'quiz': quiz,
            'score': score,
            'total': total,
            'course': course
        })

    return render(request, 'core/quiz_detail.html', {
        'quiz': quiz,
        'course': course
    })


@login_required
def create_course(request):
    if request.user.role != 'enseignant' and request.user.role != 'admin':
        return redirect('dashboard')
    
    if request.method == 'POST':
        title = request.POST['title']
        course = Course.objects.create(title=title, teacher=request.user)
        return redirect('course_detail', pk=course.pk)
    
    return render(request, 'core/create_course.html')


@login_required
def add_lesson(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user != course.teacher and request.user.role != 'admin':
        return redirect('dashboard')
    
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        video_url = request.POST.get('video_url', '')
        materials_url = request.POST.get('materials_url', '')
        lesson_id = course.lessons.count() + 1
        Lesson.objects.create(
            course=course, 
            lesson_id=lesson_id, 
            title=title, 
            content=content,
            video_url=video_url,
            materials_url=materials_url
        )
        return redirect('course_detail', pk=course.pk)
    
    return render(request, 'core/add_lesson.html', {'course': course})
