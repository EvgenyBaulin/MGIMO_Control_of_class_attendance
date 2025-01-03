from django.db import models
from django.contrib.auth.models import AbstractUser


class Group(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    )
    email = models.EmailField(unique = True)
    role = models.CharField(max_length = 10, choices = ROLE_CHOICES, default = 'student')
    group = models.ForeignKey(Group, null = True, blank = True, on_delete = models.SET_NULL)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.role})"


class Auditorium(models.Model):
    name = models.CharField(max_length = 100)
    nfc_code = models.CharField(max_length = 255, blank = True, null = True)
    nfc_link = models.URLField(max_length = 255, blank = True, null = True)

    def __str__(self):
        return self.name


class Lecture(models.Model):
    title = models.CharField(max_length = 200)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    auditorium = models.ForeignKey(Auditorium, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.title} on {self.date} at {self.start_time}"


class Attendance(models.Model):
    student = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.student} - {self.lecture} - {self.timestamp}"
