from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Lesson, Comments
from .forms import CommentForm
from datetime import date

# Create your views here.
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

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

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
def add_photo(request, lesson_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{key}"
            Photo.objects.create(url=url, lesson_id=lesson_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('lesson_detail', lesson_id=lesson_id)

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
   

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)
    if request.method == 'POST':
        comment.delete()
    return redirect('lesson_detail', lesson_id=comment.lesson.id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html' , context)