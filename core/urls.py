from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/<int:pk>/enroll/', views.enroll_course, name='enroll_course'),
    path('courses/<int:course_pk>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('courses/<int:course_pk>/quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('courses/create/', views.create_course, name='create_course'),
    path('courses/<int:pk>/add-lesson/', views.add_lesson, name='add_lesson'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('manage-users/<int:user_id>/change-role/', views.change_role, name='change_role'),
]
