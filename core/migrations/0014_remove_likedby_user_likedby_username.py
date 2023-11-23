# Generated by Django 4.2.5 on 2023-11-14 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_remove_likedby_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likedby',
            name='user',
        ),
        migrations.AddField(
            model_name='likedby',
            name='username',
            field=models.CharField(default='null', max_length=100, unique=True),
        ),
    ]
