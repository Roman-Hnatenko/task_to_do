# Generated by Django 3.1.7 on 2021-04-05 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0009_auto_20210405_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitekey',
            name='key',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
