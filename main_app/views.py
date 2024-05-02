from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Lesson, Comments, Photo
from .forms import CommentForm
from datetime import date
import boto3, uuid

# Create your views here.
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

# @login_required
def home(request):
    lessons = Lesson.objects.all().order_by('-created_at')  
    return render(request, 'home.html', {'lessons': lessons})



def about(request):
    return render(request, 'about.html')

@login_required
def lessons_index(request):
    lessons = Lesson.objects.all()
    return render(request, 'lessons/index.html', {
        'lessons': lessons,
    })

@login_required
def lesson_detail(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    comments = lesson.comments.all()
    comment_form = CommentForm()

    # Check if the lesson belongs to the current user
    if lesson.user == request.user:
        # Allow full access if the lesson belongs to the current user
        can_edit_delete = True
    else:
        # Restrict access if the lesson belongs to another user
        can_edit_delete = False
    return render(request, 'lessons/detail.html', {
        'lesson': lesson,
        'comments': comments,
        'comment_form': comment_form,
        'can_edit_delete': can_edit_delete,
    })


class LessonCreate(CreateView):
    model = Lesson
    fields = ['title', 'description', 'content', 'difficulty_level']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

import os  
def add_photo(request, lesson_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # url = f'{os.environ["S3_BASE_URL"]}{os.environ["S3_BUCKET"]}/{key}'
        try:
            url = f'{os.environ["S3_BASE_URL"]}{os.environ["S3_BUCKET"]}/{key}'
            s3.upload_fileobj(photo_file, os.environ['S3_BUCKET'], key)
            Photo.objects.create(url=url, lesson_id=lesson_id)
        except Exception as e:
            print('Error uploading to S3')
            print('Exception message: ', e)
    print(lesson_id)
    return redirect('lesson_detail', lesson_id=lesson_id)

class LessonUpdate(UpdateView):
    model = Lesson 
    fields = ['title', 'description', 'content', 'difficulty_level']

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)

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
      if request.user == comment.user:
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

def search(request):
    query = request.GET.get('q')
    lessons = Lesson.objects.all()
    if query:
        lessons = Lesson.objects.filter(title__icontains=query).order_by('-title')
    return render(request, 'lessons/search_results.html', {'lessons': lessons})