# Generated by Django 5.0.3 on 2024-03-30 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_profile_last_toxic_comment_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_toxic_comment',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]