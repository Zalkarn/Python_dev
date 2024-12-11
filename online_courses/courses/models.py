from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title

    # Валидация: дата начала не может быть позже даты окончания
    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Start date cannot be later than end date.")

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.user.username

    # Метод для получения всех курсов студента
    def get_enrolled_courses(self):
        return self.enrollment_set.all()

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.title}"
