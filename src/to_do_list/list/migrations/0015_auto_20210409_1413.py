# Generated by Django 3.2 on 2021-04-09 14:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0014_auto_20210406_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitekey',
            name='friend',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='friend', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invitekey',
            name='key',
            field=models.SlugField(default=uuid.uuid1),
        ),
        migrations.AlterField(
            model_name='task',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
