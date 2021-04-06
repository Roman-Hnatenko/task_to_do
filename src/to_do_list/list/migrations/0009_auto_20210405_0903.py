# Generated by Django 3.1.7 on 2021-04-05 09:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0008_auto_20210405_0814'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='frends',
        ),
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='_user_friends_+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invitekey',
            name='key',
            field=models.CharField(max_length=25, unique=True),
        ),
    ]