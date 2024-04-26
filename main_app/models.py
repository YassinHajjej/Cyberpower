from django.db import models

# Create your models here.
class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    content = models.TextField()
    duration = models.DurationField()
    difficulty_level = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title