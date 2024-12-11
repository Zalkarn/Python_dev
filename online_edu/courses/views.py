from django.shortcuts import render, redirect
from .models import Course, Enrollment
from django.contrib.auth.models import User
from .models import Student
from django.contrib.auth import login, authenticate
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Главная страница с курсами
def index(request):
    courses = Course.objects.all()  # Получаем все курсы
    return render(request, 'courses/index.html', {'courses': courses})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Авторизация пользователя после регистрации
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('index')  # Перенаправление на главную страницу после регистрации
    else:
        form = RegisterForm()
    return render(request, 'courses/register.html', {'form': form})


# Представление для входа
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли!')
            return redirect('index')  # Перенаправление на главную страницу
        else:
            messages.error(request, 'Ошибка входа. Проверьте логин и пароль.')
    else:
        form = AuthenticationForm()
    return render(request, 'courses/login.html', {'form': form})

# Запись на курс (доступно только для авторизованных пользователей)
@login_required
def enroll(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        messages.error(request, 'Курс не найден.')
        return redirect('course_list')
    
    student, created = Student.objects.get_or_create(user=request.user)
    Enrollment.objects.create(student=student, course=course)
    messages.success(request, f'Вы успешно записаны на курс {course.title}')
    
    # Перенаправляем на страницу с успешной записью
    return redirect('success_page', course_id=course.id)

# Представление для успешной записи на курс
@login_required
def success_page(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'courses/success_page.html', {'course': course})