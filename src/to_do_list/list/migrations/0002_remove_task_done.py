# Generated by Django 3.1.7 on 2021-03-29 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='done',
        ),
    ]