from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Lesson, Comments
from .forms import CommentForm


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
    return render(request, 'lessons/detail.html', {
        'lesson': lesson,
        'comments': comments,
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
    comment = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.lesson_id = lesson_id
            comment.save()
        print(comment)
    return redirect('lesson_detail', lesson_id=lesson_id)
