from django.db import models
from django.urls import reverse
from datetime import date

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    content = models.TextField()
    difficulty_level = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # topics = models.ManyToManyField(Topic)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'lesson_id': self.id})
    
    
class Comments(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='comments')
    date = models.DateField('Date Posted')
    content = models.CharField('Comment', max_length=255)

    def __str__(self):
        return self.content
    
    class Meta:
        ordering = ['-date']