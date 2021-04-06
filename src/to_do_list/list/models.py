from datetime import datetime
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)


class InviteKey(models.Model):
    invitor = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.SlugField(max_length=50, unique=True)
    friend = models.OneToOneField(User, on_delete=models.CASCADE, related_name='friend', null=True)

    def is_active(self) -> bool:
        return not bool(self.friend)


class Task(models.Model):
    title = models.CharField(max_length=60, default='')
    description = models.TextField(max_length=200, blank=True)
    date = models.DateTimeField(default=datetime.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    done_date = models.DateTimeField(null=True,  blank=True)

    @property
    def is_done(self) -> bool:
        return bool(self.done_date)

    def __str__(self):
        return str(self.title)
