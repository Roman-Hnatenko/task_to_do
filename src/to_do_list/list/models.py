import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)


class InviteKey(models.Model):
    invitor = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.SlugField(max_length=50, default=uuid.uuid1)
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend', null=True)

    @property
    def is_active(self) -> bool:
        return not bool(self.friend)

    def is_invitor(self, user=None) -> bool:
        return bool(self.invitor == user)


class Task(models.Model):
    title = models.CharField(max_length=60, default='')
    description = models.TextField(max_length=200, blank=True)
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    done_date = models.DateTimeField(null=True, blank=True)

    @property
    def is_done(self) -> bool:
        return bool(self.done_date)

    def __str__(self):
        return str(self.title)
