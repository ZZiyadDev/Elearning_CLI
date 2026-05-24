from django.contrib import admin
from .models import Utilisateur, Course, Lesson, Quiz, Question, Progress

class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('username', 'nom', 'email', 'role', 'is_staff')
    list_filter = ('role',)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher')
    list_filter = ('teacher',)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'lesson_id')

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'quiz_id')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'quiz')

class ProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'course')

admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Progress, ProgressAdmin)
