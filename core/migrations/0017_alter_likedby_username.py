# Generated by Django 4.2.5 on 2023-11-15 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_remove_post_liked_post_likedby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likedby',
            name='username',
            field=models.CharField(max_length=100),
        ),
    ]
