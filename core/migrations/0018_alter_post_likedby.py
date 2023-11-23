# Generated by Django 4.2.5 on 2023-11-15 18:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0017_alter_likedby_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likedby',
            field=models.ManyToManyField(related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]