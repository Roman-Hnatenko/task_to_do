from django.db import models
from datetime import date


class User(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField(max_length=40, unique=True)
    password = models.CharField(max_length=20)


class Task(models.Model):
    task_text = models.TextField(max_length=120, unique=True)
    date = models.DateField(default=date.today())
    author = models.ForeignKey(User, on_delete=models.CASCADE)
