# Generated by Django 4.2.5 on 2023-11-15 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_remove_post_likedby_post_liked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='liked',
        ),
        migrations.AddField(
            model_name='post',
            name='likedby',
            field=models.ManyToManyField(related_name='liked_posts', to='core.likedby'),
        ),
    ]