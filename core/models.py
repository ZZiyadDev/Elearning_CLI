from django.contrib.auth.models import AbstractUser
from django.db import models


class Utilisateur(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('enseignant', 'Enseignant'),
        ('etudiant', 'Etudiant'),
    )
    nom = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='etudiant')

    def __str__(self):
        return f"{self.nom} ({self.username})"


class Course(models.Model):
    title = models.CharField(max_length=255)
    teacher = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='courses_taught')
    enrolled_students = models.ManyToManyField(Utilisateur, related_name='enrolled_courses', blank=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    lesson_id = models.IntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_url = models.URLField(max_length=500, blank=True, null=True)
    materials_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    quiz_id = models.IntegerField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    options = models.JSONField(default=list)
    correct_answer = models.IntegerField()

    def __str__(self):
        return self.question


class Progress(models.Model):
    student = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='progress_records')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progress_records')
    completed_lessons = models.JSONField(default=list)
    quiz_scores = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"
