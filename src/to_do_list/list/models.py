from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class User(AbstractUser):
    USERNAME_FIELD = 'username'


class Task(models.Model):
    title = models.CharField(max_length=60, default='')
    description = models.TextField(max_length=200, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    done_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
