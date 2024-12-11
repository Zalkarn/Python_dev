# courses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('register/', views.register, name='register'),  # Страница регистрации
    path('login/', views.user_login, name='login'),  # Страница входа
    path('courses/', views.course_list, name='course_list'),  # Список курсов
    path('enroll/<int:course_id>/', views.enroll, name='enroll'),  # Запись на курс
    path('success/<int:course_id>/', views.success_page, name='success_page'),  # Новый маршрут
]
