# Generated by Django 3.1.7 on 2021-04-05 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0010_auto_20210405_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitekey',
            name='friend_id',
            field=models.IntegerField(null=True),
        ),
    ]
