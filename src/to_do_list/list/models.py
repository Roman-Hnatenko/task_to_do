from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Task(models.Model):
    title = models.CharField(max_length=60, default='')
    description = models.TextField(max_length=200, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    done_date = models.DateTimeField(null=True,  blank=True)

    @property
    def is_done(self) -> bool:
        return bool(self.done_date)

    def __str__(self):
        return str(self.title)
