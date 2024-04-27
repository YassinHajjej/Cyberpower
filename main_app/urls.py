from django.urls import path
from. import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('lessons/', views.lessons_index, name='index'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='detail'),
    path('lessons/create/', views.LessonCreate.as_view(), name='lessons_create'),
    path('lessons/<int:pk>/update/', views.LessonUpdate.as_view(), name='lesson_update'),
    path('lessons/<int:pk>/delete/', views.LessonDelete.as_view(), name='lesson_delete'),
]