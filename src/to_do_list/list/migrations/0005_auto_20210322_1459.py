# Generated by Django 3.1.7 on 2021-03-22 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0004_auto_20210322_1458'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='description',
        ),
        migrations.RemoveField(
            model_name='task',
            name='title',
        ),
    ]