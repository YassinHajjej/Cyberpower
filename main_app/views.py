from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Lesson, Comments
from .forms import CommentForm
from datetime import date


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def lessons_index(request):
    lessons = Lesson.objects.all()
    return render(request, 'lessons/index.html', {
        'lessons': lessons,
    })


def lesson_detail(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    comments = lesson.comments.all()
    print(comments)
    comment_form = CommentForm()
    return render(request, 'lessons/detail.html', {
        'lesson': lesson,
        'comments': comments,
        'comment_form': comment_form,
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


def add_comment(request, lesson_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.lesson_id = lesson_id
        new_comment.date = date.today()
        new_comment.save()
    return redirect('lesson_detail', lesson_id=lesson_id)
   

   
    
