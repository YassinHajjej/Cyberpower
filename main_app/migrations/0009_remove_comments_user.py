# Generated by Django 5.0.4 on 2024-04-30 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_comments_user_alter_comments_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='user',
        ),
    ]
