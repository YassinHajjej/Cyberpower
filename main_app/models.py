from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

# Create your models here.



class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    content = models.TextField()
    difficulty_level = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    # photo = models.ForeignKey(Photo , on_delete=models.CASCADE, null=True)
    # topics = models.ManyToManyField(Topic)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('lesson_detail', kwargs={'lesson_id': self.id})
    
# class Comment(models.Model):  
class Comments(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='comments')
    date = models.DateField('Date Posted', auto_now_add=True)
    content = models.CharField('Comment', max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.content
    
    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for lesson_id: {self.lesson_id} @{self.url}"

