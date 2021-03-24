# Generated by Django 3.1.7 on 2021-03-22 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0003_auto_20210319_0835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='task_text',
        ),
        migrations.AddField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='task',
            name='done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='title',
            field=models.CharField(default=1, max_length=40, unique=True),
            preserve_default=False,
        ),
    ]