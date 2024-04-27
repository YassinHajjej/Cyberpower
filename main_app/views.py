from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Lesson


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def lessons_index(request):
    lessons = Lesson.objects.all()
    return render(request, 'lessons/index.html', {
        'lessons': lessons
    })

def lesson_detail(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    return render(request, 'lessons/detail.html', {
        'lesson': lesson 
    })

class LessonCreate(CreateView):
    model = Lesson
    fields = '__all__'

class LessonUpdate(UpdateView):
    model = Lesson 
    fields = '__all__'

class LessonDelete(DeleteView):
    model = Lesson
    success_url = '/lessons/'