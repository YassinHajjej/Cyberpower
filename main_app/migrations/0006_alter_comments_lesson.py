# Generated by Django 5.0.4 on 2024-04-29 22:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_comments_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.lesson'),
        ),
    ]
