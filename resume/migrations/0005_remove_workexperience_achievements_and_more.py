# Generated by Django 4.2 on 2024-07-17 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0004_workexperience_achievements_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workexperience',
            name='achievements',
        ),
        migrations.RemoveField(
            model_name='workexperience',
            name='responsibilities',
        ),
        migrations.RemoveField(
            model_name='workexperience',
            name='skills_used',
        ),
        migrations.RemoveField(
            model_name='workexperience',
            name='user',
        ),
    ]
